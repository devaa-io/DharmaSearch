# loaders/isha.py
#
# Isha (Ishavasya) Upanishad - 18 mantras, Shukla Yajurveda.
#
# SOURCES (both live-fetched from the open network; the chat sandbox could not reach
# either, which is why this ran from Claude Code with open access):
#
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/iisha.html)
#                Real Unicode Devanagari, NOT the romanised .itx - the hard rule
#                forbids transliterating from lossy ASCII, so we take the Devanagari
#                page and let the pipeline generate ml/ta/te/kn from it.
#
#   English    : Max Muller, "The Upanishads, Part I", Sacred Books of the East Vol. 1
#                (Oxford, 1879), the "Vagasaneyi-samhita-upanishad" chapter, via
#                English Wikisource.
#                LICENSING: Muller died 1900 -> the translation is in the public
#                domain worldwide (author's life + far more than 70 years). The
#                Wikisource transcription is likewise public domain. Safe to bundle.
#
# The two sources are aligned by mantra number 1..18.
import re
import html
import requests
from loaders._wikisource import rendered_text

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/iisha.html"
EN_TITLE = "Sacred Books of the East/Volume 1/Vâgasaneyi-samhitâ-upanishad"
WS_API = "https://en.wikisource.org/w/api.php"

# sanskritdocuments filters the default python-requests User-Agent (returns HTTP 406),
# so present a browser UA. Wikisource is happy with a descriptive UA.
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
END_MARKER = re.compile(r"॥\s*[" + DEVA_DIGITS + r"]+\s*॥")   # e.g. "॥ १८॥"


def _fetch_devanagari():
    """Return the 18 Isha mantras as clean Devanagari strings (index 0 = mantra 1)."""
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    raw = response.text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    # The page opens with the "purnam adah" shanti (no number) and closes with another
    # shanti. The 18 numbered mantras run from "ईशा" (mantra 1) to the "॥ १८॥" marker.
    start = txt.find("ईशा")
    end = txt.find("॥ १८॥")
    if start < 0 or end < 0:
        raise RuntimeError("Isha: could not locate mantra span in source page")
    span = txt[start:end + len("॥ १८॥")]
    parts = [p for p in END_MARKER.split(span) if p.strip()]
    verses = []
    for p in parts:
        v = re.sub(r"\s+", " ", p).strip().rstrip("।॥").strip() + " ॥"
        verses.append(v)
    if len(verses) != 18:
        raise RuntimeError(f"Isha: expected 18 mantras, parsed {len(verses)}")
    return verses


def _fetch_english():
    """Return {mantra_number: Muller English} for mantras 1..18."""
    response = requests.get(
        WS_API,
        params={"action": "parse", "page": EN_TITLE, "prop": "text",
                "format": "json", "formatversion": 2},
        headers=WS_HEADERS, timeout=40,
    )
    response.raise_for_status()
    j = response.json()
    ht = j["parse"]["text"]
    txt = rendered_text(ht)
    txt = txt.split("↑")[0]                               # cut the trailing footnotes block
    txt = txt.split("This Upanishad, though apparently")[0]  # cut Muller's following commentary
    txt = re.split(r"\bFootnotes\b", txt, maxsplit=1, flags=re.I)[0]
    en = {}
    for m in re.finditer(r"(?:^|\s)(\d{1,2})\.\s+(.+?)(?=\s\d{1,2}\.\s|\Z)", txt, re.S):
        n = int(m.group(1))
        if 1 <= n <= 18 and n not in en:
            en[n] = " ".join(m.group(2).split())
    if sorted(en) != list(range(1, 19)):
        raise RuntimeError(f"Isha: English mantras incomplete: got {sorted(en)}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_english()
    rows = []
    for i in range(1, 19):
        rows.append({
            "devanagari": dev[i - 1],
            "translation": en[i],
            "verse": i,
        })
    return rows
