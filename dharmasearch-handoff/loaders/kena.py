# loaders/kena.py
#
# Kena (Talavakara) Upanishad - 35 mantras across 4 khandas, Sama Veda.
#
# SOURCES:
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/kena.html)
#                Real Unicode Devanagari (not the romanised .itx), per the hard rule.
#
#   English    : Max Muller, "The Upanishads, Part I", Sacred Books of the East
#                Vol. 1 (Oxford, 1879), the "Talavakara-upanishad" chapter, via
#                English Wikisource.
#                LICENSING: Muller died 1900 -> public domain worldwide. Same
#                volume/source pattern already used for the Isha Upanishad.
#
# Unlike Isha's flat 1-18 numbering, Kena's mantra numbers RESET each khanda
# (Kh.1 = 1-9, Kh.2 = 1-5, Kh.3 = 1-12, Kh.4 = 1-9 = 35 total). Both sources use
# this same khanda/verse scheme, so rows are aligned on (khanda, verse), not a
# flat index.
import re
import html
import requests

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/kena.html"
EN_TITLE = "Sacred Books of the East/Volume 1/Talavakâra-upanishad"
WS_API = "https://en.wikisource.org/w/api.php"

DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}
KHANDA_SIZES = {1: 9, 2: 5, 3: 12, 4: 9}


def _deva2int(s: str) -> int:
    return int("".join(DEVA_MAP.get(ch, ch) for ch in s))


def _fetch_devanagari():
    """Return {(khanda, verse): devanagari_text} for all 35 Kena mantras."""
    raw = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30).text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    start = txt.find("केनेषितं")
    end = txt.rfind("॥ ९॥")
    if start < 0 or end < 0:
        raise RuntimeError("Kena: could not locate mantra span in source page")
    span = txt[start:end + len("॥ ९॥")]

    parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", span)
    kh, prev_n = 1, 0
    dev = {}
    for i in range(1, len(parts), 2):
        num = _deva2int(parts[i])
        if num <= prev_n:
            kh += 1
        body = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip() + " ॥"
        dev[(kh, num)] = body
        prev_n = num

    if len(dev) != 35 or sorted(set(k for k, _ in dev)) != [1, 2, 3, 4]:
        raise RuntimeError(f"Kena: expected 35 mantras in 4 khandas, parsed {len(dev)}")
    return dev


def _fetch_english():
    """Return {(khanda, verse): Muller English} for all 35 Kena mantras."""
    j = requests.get(
        WS_API,
        params={"action": "parse", "page": EN_TITLE, "prop": "text",
                "format": "json", "formatversion": 2},
        headers=WS_HEADERS, timeout=40,
    ).json()
    ht = j["parse"]["text"]
    ht = re.sub(r"<sup[^>]*>.*?</sup>", "", ht)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", ht))
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = txt.split("↑")[0]
    # Wikisource's rendered HTML breaks "Khanda" across a line as "Kha nd a"
    txt = re.sub(r"Kha\s*nd\s*a", "Khanda", txt)

    chunks = re.split(r"(?i)(first|second|third|fourth)\s+khanda", txt)
    kh_labels = {"first": 1, "second": 2, "third": 3, "fourth": 4}
    en = {}
    for i in range(1, len(chunks), 2):
        kh = kh_labels[chunks[i].lower()]
        body = chunks[i + 1]
        for m in re.finditer(r"(?:^|\s)(\d{1,2})\.\s+(.+?)(?=\s\d{1,2}\.\s|\Z)", body, re.S):
            vn = int(m.group(1))
            if (kh, vn) not in en:
                en[(kh, vn)] = " ".join(m.group(2).split())

    if len(en) != 35 or {k: sum(1 for kk, _ in en if kk == k) for k in (1, 2, 3, 4)} != KHANDA_SIZES:
        raise RuntimeError(f"Kena: English mantras incomplete/misaligned: {sorted(en)}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_english()
    rows = []
    for kh in (1, 2, 3, 4):
        for vn in range(1, KHANDA_SIZES[kh] + 1):
            rows.append({
                "devanagari": dev[(kh, vn)],
                "translation": en[(kh, vn)],
                "chapter": kh,
                "verse": vn,
            })
    return rows
