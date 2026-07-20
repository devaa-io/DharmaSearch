# loaders/prashna.py
#
# Prashna Upanishad - 67 verses across 6 prashnas (questions) asked by six
# seekers of the sage Pippalada, Atharva Veda (sizes 16/13/12/11/7/8).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/prashna.html)
#                Real Unicode Devanagari. Section markers are "<ordinal> प्रश्नः"
#                (opening and closing use the SAME ordinal word for a given
#                prashna - e.g. both the header and the "iti ... prathamah
#                prasnah" close say "प्रथमः"), so headers appear as adjacent
#                pairs in document order. Verse markers combine prashna+verse
#                as "<n>.<verse>" in Devanagari digits, e.g. "॥ १.१॥".
#
#   English    : Max Muller, "The Upanishads, Part II", Sacred Books of the East
#                Vol. 15 (Oxford, 1884), the "Prasna-upanishad" chapter, via
#                English Wikisource. LICENSING: Muller died 1900 -> public
#                domain worldwide, same pattern already used for the other
#                principal Upanishads in this project.
import re
import html
import requests

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/prashna.html"
EN_TITLE = "Sacred Books of the East/Volume 15/Prasña-upanishad"
WS_API = "https://en.wikisource.org/w/api.php"

DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}
PRASHNA_SIZES = {1: 16, 2: 13, 3: 12, 4: 11, 5: 7, 6: 8}
ORDINALS = ["प्रथमः", "द्वितीयः", "तृतीयः", "चतुर्थः", "पञ्चमः", "षष्ठः"]


def _deva2int(s: str) -> int:
    return int("".join(DEVA_MAP.get(ch, ch) for ch in s))


def _fetch_devanagari():
    """Return {(prashna, verse): devanagari_text} for all 67 verses."""
    raw = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30).text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))

    ordinal_pat = "|".join(ORDINALS)
    heads = list(re.finditer(ordinal_pat + r"\s*प्रश्नः", txt))
    if len(heads) != 12:
        raise RuntimeError(f"Prashna: expected 12 header/close markers, found {len(heads)}")

    dev = {}
    for n in range(1, 7):
        op, cl = heads[2 * (n - 1)], heads[2 * (n - 1) + 1]
        body = txt[op.end():cl.start()]
        parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+\.[" + DEVA_DIGITS + r"]+)\s*॥", body)
        for i in range(1, len(parts), 2):
            vn = _deva2int(parts[i].split(".")[1])
            v = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip() + " ॥"
            dev[(n, vn)] = v

    if len(dev) != 67 or {k: sum(1 for kk, _ in dev if kk == k) for k in range(1, 7)} != PRASHNA_SIZES:
        raise RuntimeError(f"Prashna: expected 67 verses across 6 prashnas, parsed {len(dev)}")
    return dev


def _fetch_english():
    """Return {(prashna, verse): Muller English} for all 67 verses."""
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

    matches = list(re.finditer(r"(First|Second|Third|Fourth|Fifth|Sixth)\s+Qu\s*es\s*tion", txt, re.I))
    if len(matches) != 6:
        raise RuntimeError(f"Prashna: expected 6 Question headers, found {len(matches)}")
    words = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6}

    en = {}
    for idx, m in enumerate(matches):
        n = words[m.group(1).lower()]
        s = m.end()
        e = matches[idx + 1].start() if idx + 1 < len(matches) else len(txt)
        body = txt[s:e]
        for vm in re.finditer(r"(?:^|\s)(\d{1,2})\.\s+(.+?)(?=\s\d{1,2}\.\s|\Z)", body, re.S):
            vn = int(vm.group(1))
            if (n, vn) not in en:
                en[(n, vn)] = " ".join(vm.group(2).split())

    if len(en) != 67 or {k: sum(1 for kk, _ in en if kk == k) for k in range(1, 7)} != PRASHNA_SIZES:
        raise RuntimeError(f"Prashna: English verses incomplete/misaligned: {sorted(en)}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_english()
    rows = []
    for n in range(1, 7):
        for vn in range(1, PRASHNA_SIZES[n] + 1):
            rows.append({
                "devanagari": dev[(n, vn)],
                "translation": en[(n, vn)],
                "chapter": n,
                "verse": vn,
            })
    return rows
