"""Load Patanjali's 195 Yoga Sutras from reproducible public sources.

Devanagari comes from the unaccented recension published by
sanskritdocuments.org. English is Charles Johnston's 1912 interpretation,
served by Project Gutenberg (ebook 2526). Johnston's first paragraph for each
numbered sutra is the translation; the following paragraphs are commentary and
are deliberately not merged into the verse field.
"""

from __future__ import annotations

import html
import re

import requests


DEV_URL = "https://sanskritdocuments.org/doc_yoga/yogasuutra.html"
EN_URL = "https://www.gutenberg.org/cache/epub/2526/pg2526-images.html"
HEADERS = {
    "User-Agent": "DharmaSearch/1.0 (scripture ingest; non-commercial research use)",
}
EXPECTED = {1: 51, 2: 55, 3: 55, 4: 34}
DEVA_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
VERSE_END = re.compile(r"॥\s*([१२३४])\.([०-९]+)\s*॥")
PARAGRAPH = re.compile(r'<p\s+class="p1"[^>]*>(.*?)</p>', re.I | re.S)


def _plain(markup: str) -> str:
    text = re.sub(r"<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _get(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    return response.text


def _fetch_devanagari() -> dict[tuple[int, int], str]:
    source = _get(DEV_URL)
    # The page first prints a Vedic-accented edition and then the unaccented
    # reading used by the app. This exact heading only occurs in the latter.
    marker = "॥ प्रथमोऽध्यायः ॥  ॥ समाधि-पादः ॥"
    start = source.rfind(marker)
    if start < 0:
        raise RuntimeError("Yoga Sutras: unaccented source heading not found")
    source = html.unescape(re.sub(r"<[^>]+>", "", source[start:]))

    verses: dict[tuple[int, int], str] = {}
    cursor = 0
    for match in VERSE_END.finditer(source):
        chapter = int(match.group(1).translate(DEVA_DIGITS))
        verse = int(match.group(2).translate(DEVA_DIGITS))
        segment = source[cursor:match.start()]
        # Sutras are separated by blank lines. Taking the last block avoids
        # chapter headings and parenthetical variants printed after the
        # preceding verse number.
        body = re.split(r"\n\s*\n", segment)[-1]
        body = re.sub(r"\s+", " ", body).strip()
        body = re.sub(
            r"^॥\s*[^॥]*ध्यायः\s*॥\s*॥\s*[^॥]*पादः\s*॥\s*",
            "",
            body,
        )
        key = (chapter, verse)
        if key in verses:
            raise RuntimeError(f"Yoga Sutras: duplicate Sanskrit sutra {chapter}.{verse}")
        verses[key] = body
        cursor = match.end()

    _assert_sequence(verses, "Devanagari")
    return verses


def _fetch_english() -> dict[tuple[int, int], str]:
    source = _get(EN_URL)
    anchors = {chapter: f'<h2><a id="chap{chapter * 2:02d}"></a>BOOK {roman}</h2>'
               for chapter, roman in enumerate(("", "I", "II", "III", "IV")) if chapter}
    verses: dict[tuple[int, int], str] = {}
    for chapter in range(1, 5):
        start = source.find(anchors[chapter])
        if start < 0:
            raise RuntimeError(f"Yoga Sutras: English Book {chapter} heading not found")
        next_heading = f'<h2><a id="chap{chapter * 2 + 1:02d}"></a>'
        end = source.find(next_heading, start)
        if end < 0:
            end = len(source)
        paragraphs = PARAGRAPH.findall(source[start:end])
        for expected_number, paragraph in enumerate(paragraphs, 1):
            text = _plain(paragraph)
            # Gutenberg's transcription omits the full stop after Book II.5.
            # The sequence assertion still makes the number unambiguous.
            match = re.match(r"(\d+)\.?\s+(.+)", text, re.S)
            if not match:
                raise RuntimeError(
                    f"Yoga Sutras: Book {chapter} translation paragraph has no number"
                )
            number = int(match.group(1))
            if number != expected_number:
                raise RuntimeError(
                    f"Yoga Sutras: Book {chapter} English sequence jumps from "
                    f"{expected_number - 1} to {number}"
                )
            verses[(chapter, number)] = match.group(2).strip()

    _assert_sequence(verses, "English")
    return verses


def _assert_sequence(rows: dict[tuple[int, int], str], label: str) -> None:
    expected = {
        (chapter, verse)
        for chapter, count in EXPECTED.items()
        for verse in range(1, count + 1)
    }
    actual = set(rows)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise RuntimeError(
            f"Yoga Sutras: {label} sequence mismatch; missing={missing}, extra={extra}"
        )
    empty = sorted(key for key, value in rows.items() if not value.strip())
    if empty:
        raise RuntimeError(f"Yoga Sutras: empty {label} rows {empty}")


def load() -> list[dict]:
    devanagari = _fetch_devanagari()
    english = _fetch_english()
    return [
        {
            "devanagari": devanagari[(chapter, verse)],
            "translation": english[(chapter, verse)],
            "chapter": chapter,
            "verse": verse,
        }
        for chapter, count in EXPECTED.items()
        for verse in range(1, count + 1)
    ]
