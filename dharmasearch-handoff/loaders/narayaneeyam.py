# loaders/narayaneeyam.py
#
# Narayaneeyam (Sriman Narayaniyam) - Melpathur Narayana Bhattatiri's 100-canto
# devotional condensation of the Bhagavata Purana, in praise of Krishna at
# Guruvayoor. 1033 verses in this edition, across 100 cantos (dashakas).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org (doc_vishhnu/nArAyaNIyam.html) - the
#     general document collection, not the "For private circulation only"
#     dedicated project site. Clean chapter-verse numbering (e.g. "..1-1..").
#
#   English   : P. R. Ramachander, hosted at celextel.org's Vedanta Spiritual
#     Library (same source already trusted for Vishnu Sahasranama, Soundarya
#     Lahari, Lalita Sahasranama, Hanuman Chalisa), paginated across 6 pages
#     (dasakams 1-19, 20-38, 39-62, 63-82, 83-97, 98-100). The translator's
#     own introduction calls it "simple free verse and not a word-for-word
#     translation" - spot-checked against the Devanagari at verses 1.1, 25.5,
#     50.1 and 100.11 before committing to the full text (owner-approved,
#     2026-07-30): all four matched the correct story content at the right
#     canto/verse number, so the looseness is prose style, not misalignment.
#
#   An earlier CC0-licensed OCR scan (Swami Tapasyananda, archive.org) was
#   rejected for corrupted Sanskrit and interleaved page headers making
#   canto-boundary detection unreliable - not a concern with celextel, which
#   is clean HTML with an explicit dasakam.verse numbering scheme.
#
#   Coverage: celextel's own markup has three quirks worked around below -
#   a chapter-transition boundary marked only by a stray `<br>` (not the
#   double-`<br>` blank line used elsewhere) that swallows each dasakam's
#   final verse into the next dasakam's heading unless `</p><p>` and
#   `</font><font>` tag boundaries are also treated as verse separators;
#   asterisked footnotes appended after a verse's own number; and the
#   pagination footer HTML at the end of each page, which must be cropped
#   before parsing or it defeats the end-of-verse marker match entirely.
#   Two entries (45.11, 45.12) are explicitly flagged by the translator as
#   not present in "the authorized Vanamala version" (i.e. not canonical),
#   and one (84.11) has no counterpart in the Devanagari - all three are
#   dropped by filtering English to only the (chapter, verse) pairs the
#   Devanagari parse already verified exist.
import html
import re
import requests

DEV_URL = "https://sanskritdocuments.org/doc_vishhnu/nArAyaNIyam.html"
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}

DEVA_DIGITS = "०१२३४५६७८९"
VERSE_MARKER = re.compile(r"॥\s*([०-९]+)-([०-९]+)॥")


def _deva_to_int(digits: str) -> int:
    return int("".join(str(DEVA_DIGITS.index(c)) for c in digits))


EN_BASE = "https://www.celextel.org/vishnu-stotras/narayaneeyam/"
EN_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}
EN_VERSE_END = re.compile(r"(\d{1,3})\.(\d{1,2})\s*((?:\*[^*]*)*)$")


def _fetch_english_page(page: int) -> dict:
    url = EN_BASE if page == 1 else f"{EN_BASE}{page}/"
    response = requests.get(url, headers=EN_HEADERS, timeout=30)
    response.raise_for_status()
    text = response.text

    start = text.find("<article")
    paging = text.find('<div class="paging"')
    end = text.find("</article>")
    if paging != -1 and paging < end:
        end = paging
    body = text[start:end]

    segments = re.split(r"(?:<br>\s*){2,}|</p>\s*<p[^>]*>|</font>\s*<font[^>]*>", body)
    out = {}
    for seg in segments:
        seg = re.sub(r"^\s*(?:<[^>]+>|\s)*\[[^\]]*\]\s*(?:<br>\s*)+", "", seg)
        clean = re.sub(r"<[^>]+>", " ", seg)
        clean = html.unescape(clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        m = EN_VERSE_END.search(clean)
        if not m:
            continue
        dasakam, verse = int(m.group(1)), int(m.group(2))
        verse_text = clean[:m.start()].strip()
        if not verse_text or "Dasakam" in clean[:30]:
            continue
        out[(dasakam, verse)] = verse_text
    return out


def _fetch_english() -> dict:
    en = {}
    for page in range(1, 7):
        en.update(_fetch_english_page(page))
    return en


def load():
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    text = response.text

    start = text.find("सान्द्रानन्दावबोधात्मक")  # opening word of verse 1-1
    if start < 0:
        raise RuntimeError("Narayaneeyam: could not locate verse 1-1 in source page")
    all_markers = list(VERSE_MARKER.finditer(text))
    last = all_markers[-1]
    span = text[start:last.end()]

    rows = []
    cursor = 0
    seen = set()
    prev_chapter, prev_verse = 1, 0
    for m in VERSE_MARKER.finditer(span):
        chapter = _deva_to_int(m.group(1))
        verse = _deva_to_int(m.group(2))

        # The source has at least one single-digit transcription slip (a verse
        # immediately following "..35-5.." is itself marked "..34-6.." instead
        # of "35-6"). Detect a marker that doesn't continue the sequence but
        # would if only the chapter digit matched the running chapter, and
        # correct it - the verse text itself is untouched, only its label.
        expected_same = (chapter == prev_chapter and verse == prev_verse + 1)
        expected_next = (chapter == prev_chapter + 1 and verse == 1)
        if not (expected_same or expected_next) and verse == prev_verse + 1:
            chapter = prev_chapter

        chunk = span[cursor:m.end()]
        if "<h2" in chunk[:400]:
            # Canto headings are one or more blank-line-separated blocks
            # (the <h2> tag + Devanagari title, then an English gloss line
            # that itself sometimes wraps onto a second line) before the
            # real verse begins. Their exact shape varies too much to match
            # block-by-block (title/gloss punctuation, line wrapping, and
            # blank-line placement all differ across cantos - confirmed on
            # chapters 2-11, 38, 39, 50, 51). Verse poetry itself never
            # contains a blank line, so instead strip everything through the
            # LAST blank line in the chunk (greedy match) - whatever
            # heading content precedes it, the real verse always starts
            # right after.
            chunk = re.sub(r"^.*\n\s*\n(?=\S)", "", chunk, flags=re.S)
        dev = re.sub(r"\s+", " ", chunk).strip()
        key = (chapter, verse)
        if key in seen:
            raise ValueError(f"Narayaneeyam: duplicate verse {chapter}-{verse}")
        seen.add(key)
        rows.append({"devanagari": dev, "chapter": chapter, "verse": verse})
        cursor = m.end()
        prev_chapter, prev_verse = chapter, verse

    chapters = sorted({r["chapter"] for r in rows})
    if chapters != list(range(1, 101)):
        missing = sorted(set(range(1, 101)) - set(chapters))
        raise RuntimeError(f"Narayaneeyam: missing canto(s) {missing}")

    english = _fetch_english()
    missing_en = [
        (r["chapter"], r["verse"]) for r in rows
        if (r["chapter"], r["verse"]) not in english
    ]
    if missing_en:
        raise RuntimeError(f"Narayaneeyam: missing English for {missing_en}")
    for r in rows:
        r["english"] = english[(r["chapter"], r["verse"])]

    return rows
