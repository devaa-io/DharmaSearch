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
#   English   : DEFERRED. A CC0-licensed scan of Swami Tapasyananda's Sri
#     Ramakrishna Math translation exists (archive.org), and reads legibly as
#     prose - a real, usable source. But its embedded Sanskrit is badly
#     OCR-corrupted (confirmed: "CANTO 1" renders as "CANTO |", digit-to-pipe
#     corruption, inconsistent across cantos) and running headers/page
#     numbers interleave mid-verse throughout the 1033-verse book. Reliably
#     detecting all 100 canto boundaries from this OCR would need dozens of
#     special cases, most as yet undiscovered - a materially higher
#     misalignment risk than any other text sourced today, where even a
#     single verse landing under the wrong number ships a wrong translation
#     silently. Same treatment as Hanuman Chalisa and Lalita Sahasranama:
#     ship the verifiably correct Devanagari now, defer English until it can
#     be aligned with confidence (owner decision, 2026-07-30).
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
    return rows
