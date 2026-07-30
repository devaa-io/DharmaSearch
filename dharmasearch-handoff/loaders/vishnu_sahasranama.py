# loaders/vishnu_sahasranama.py
#
# Sri Vishnu Sahasranama Stotram - 108 slokas carrying the 1000 names of
# Vishnu, from the Anushasana Parva of the Mahabharata.
#
# SOURCES:
#   Devanagari + IAST + English : Swami Krishnananda (The Divine Life Society),
#     www.swami-krishnananda.org - a disciple of Swami Sivananda, whose Gita
#     translation this same project already carries. Published by DLS as a
#     free teaching resource; no formal CC/public-domain statement, treated
#     as acceptable per the owner's explicit call on 2026-07-30 (official
#     publisher, explicit free-distribution intent - see project ledger).
#
#   Structure: three pages (slokas 1-36, 37-72, 73-108), each sloka rendered
#   as <p class="nirmalaVishnu"> (Devanagari, ending "..N.."), <p class=
#   "VishnuT"> (IAST, ending "(N)"), then <ol class="VishnuName"> whose <li>
#   items are the individual names in that sloka with their meaning.
#
#   English here is per-name ("Name - meaning."), not flowing prose like the
#   Gita's translation; joined name by name so nothing is lost or invented.
import html
import re
import requests

PAGES = [
    "https://www.swami-krishnananda.org/vishnu/vishnu_1.html",
    "https://www.swami-krishnananda.org/vishnu/vishnu_2.html",
    "https://www.swami-krishnananda.org/vishnu/vishnu_3.html",
]
HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

SLOKA_RE = re.compile(
    r'<p class="nirmalaVishnu">(?P<dev>.*?)</p>\s*'
    r'<p class="VishnuT">(?P<iast>.*?)</p>\s*'
    # The site spells this class two ways across its own pages: "VishnuName"
    # on page 1, "VishnuNames" on pages 2-3.
    r'<ol class="VishnuNames?"[^>]*>(?P<names>.*?)</ol>',
    re.S,
)
LI_RE = re.compile(r"<li>(.*?)</li>", re.S)
DEVA_NUM = re.compile(r"॥\s*([०-९]+)\s*॥")
DEVA_DIGITS = "०१२३४५६७८९"

# Sloka 108 is a closing benediction, not a fresh batch of names: the source
# renders it as Devanagari + IAST followed by a *second* <p class="VishnuT">
# holding a prose translation, with no <ol> at all. One-off pattern for it.
#
# "(?:(?!<p).)*?" instead of a plain ".*?": a lazy dot alone will happily
# cross dozens of intervening <p class="nirmalaVishnu"> paragraphs to reach
# the single "108" marker on the page, capturing everything from the FIRST
# such paragraph rather than the one that actually contains it. The lookahead
# keeps the match inside one paragraph.
_NOT_INTO_NEXT_P = r"(?:(?!<p).)*?"
CLOSING_SLOKA_RE = re.compile(
    r'<p class="nirmalaVishnu">(?P<dev>' + _NOT_INTO_NEXT_P + r'॥१०८॥' + _NOT_INTO_NEXT_P + r')</p>\s*'
    r'<p class="VishnuT">(?P<iast>' + _NOT_INTO_NEXT_P + r')</p>\s*'
    r'<p class="VishnuT">(?P<english>' + _NOT_INTO_NEXT_P + r')</p>',
    re.S,
)


def _clean(s: str) -> str:
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    # Pages 2-3 encode diacritics as numeric character references
    # (e.g. &#347; for s-acute) instead of raw UTF-8, unlike page 1.
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def _deva_to_int(digits: str) -> int:
    return int("".join(str(DEVA_DIGITS.index(c)) for c in digits))


def _drop_verse_marker_and_after(iast: str) -> str:
    """Strip the "(N)" verse-number marker and anything after it.

    Most slokas end exactly at "(N)". The last two (107, 108) carry an
    additional liturgical closing formula ("... oM nama iti.") on a further
    line inside the same paragraph, which isn't part of the verse itself.
    """
    return re.sub(r"\.\s*\(\d+\).*$", ".", iast, flags=re.S).strip()


def _fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding  # server misreports as ISO-8859-1
    return response.text


def load():
    rows = []
    for url in PAGES:
        page = _fetch_page(url)
        matches = list(SLOKA_RE.finditer(page))
        if not matches and "१०८" not in page:
            raise RuntimeError(f"Vishnu Sahasranama: no slokas parsed from {url}")
        for m in matches:
            dev = _clean(m.group("dev"))
            iast = _drop_verse_marker_and_after(_clean(m.group("iast")))

            deva_num = DEVA_NUM.search(dev)
            if not deva_num:
                raise RuntimeError(f"Vishnu Sahasranama: no sloka number in {dev[:60]!r}")
            verse_no = _deva_to_int(deva_num.group(1))

            names = [_clean(li) for li in LI_RE.findall(m.group("names"))]
            names = [n for n in names if n]
            if not names:
                raise RuntimeError(f"Vishnu Sahasranama: sloka {verse_no} has no names")
            english = " ".join(f"{n}." if not n.endswith((".", "?", "!")) else n for n in names)

            rows.append({
                "devanagari": dev,
                "iast": iast,
                "translation": english,
                "verse": verse_no,
            })

        if "१०८" in page and not any(r["verse"] == 108 for r in rows):
            closing = CLOSING_SLOKA_RE.search(page)
            if not closing:
                raise RuntimeError("Vishnu Sahasranama: could not parse closing sloka 108")
            iast = _drop_verse_marker_and_after(_clean(closing.group("iast")))
            rows.append({
                "devanagari": _clean(closing.group("dev")),
                "iast": iast,
                "translation": _clean(closing.group("english")),
                "verse": 108,
            })

    if len(rows) != 108:
        raise RuntimeError(f"Vishnu Sahasranama: expected 108 slokas, got {len(rows)}")
    seen = {r["verse"] for r in rows}
    if seen != set(range(1, 109)):
        missing = sorted(set(range(1, 109)) - seen)
        raise RuntimeError(f"Vishnu Sahasranama: missing sloka numbers {missing}")
    return rows
