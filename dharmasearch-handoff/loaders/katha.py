# loaders/katha.py
#
# Katha Upanishad - 120 verses across 6 vallis (Adhyaya I: valli 1-3,
# Adhyaya II: valli 4-6), Krishna Yajurveda. The Naciketas / Yama dialogue on
# death and the Self.
#
# SOURCES:
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/katha.html)
#                Real Unicode Devanagari, headed "Part <adhyaya> Canto <valli>".
#
#   English    : Max Muller, "The Upanishads, Part II", Sacred Books of the East
#                Vol. 15 (Oxford, 1884), the "Katha-upanishad" chapter, via
#                English Wikisource. LICENSING: Muller died 1900 -> public domain
#                worldwide, same pattern already used for Isha and Kena.
#
# Both sources number verses 1..N within each of 6 vallis (valli sizes
# 29/25/17/15/15/19 = 120, matching the traditional Katha valli division).
# Rows are keyed by a global valli index 1-6 (spanning both adhyayas) + verse.
import re
import html
import requests

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/katha.html"
EN_TITLE = "Sacred Books of the East/Volume 15/Katha-upanishad"
WS_API = "https://en.wikisource.org/w/api.php"

DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}
VALLI_SIZES = {1: 29, 2: 25, 3: 17, 4: 15, 5: 15, 6: 19}


def _deva2int(s: str) -> int:
    return int("".join(DEVA_MAP.get(ch, ch) for ch in s))


def _fetch_devanagari():
    """Return {(valli, verse): devanagari_text} for all 120 Katha verses."""
    raw = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30).text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    heads = list(re.finditer(r"Part\s+[IVX]+\s+Canto\s+[IVX]+", txt))
    if len(heads) != 6:
        raise RuntimeError(f"Katha: expected 6 Part/Canto headers, found {len(heads)}")
    end = txt.rfind("ॐ शान्तिः शान्तिः शान्तिः ॥")

    dev = {}
    for vidx, m in enumerate(heads, 1):
        s = m.end()
        e = heads[vidx].start() if vidx < len(heads) else end
        body = txt[s:e]
        parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", body)
        for i in range(1, len(parts), 2):
            num = _deva2int(parts[i])
            v = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip() + " ॥"
            dev[(vidx, num)] = v

    if len(dev) != 120 or {k: sum(1 for kk, _ in dev if kk == k) for k in range(1, 7)} != VALLI_SIZES:
        raise RuntimeError(f"Katha: expected 120 verses across 6 vallis, parsed {len(dev)}")
    return dev


def _fetch_english():
    """Return {(valli, verse): Muller English} for all 120 Katha verses."""
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

    matches = list(re.finditer(r"(First|Second|Third|Fourth|Fifth|Sixth)\s+Vall[iî]\.?", txt, re.I))
    if len(matches) != 6:
        raise RuntimeError(f"Katha: expected 6 Valli headers, found {len(matches)}")

    # Muller's printed verse numbers are not always contiguous within a valli
    # (e.g. valli 3 runs 1-14 then jumps to 18-20 for the same 17 verses - a
    # numbering quirk of this edition, not a missing verse). Both sources
    # segment into the same verse count in the same reading order, so align
    # positionally within each valli rather than trusting the printed number.
    en = {}
    for vidx, m in enumerate(matches, 1):
        s = m.end()
        e = matches[vidx].start() if vidx < len(matches) else len(txt)
        body = txt[s:e]
        segments = list(re.finditer(r"(?:^|\s)(\d{1,2})\.\s+(.+?)(?=\s\d{1,2}\.\s|\Z)", body, re.S))
        for pos, vm in enumerate(segments, 1):
            en[(vidx, pos)] = " ".join(vm.group(2).split())

    if len(en) != 120 or {k: sum(1 for kk, _ in en if kk == k) for k in range(1, 7)} != VALLI_SIZES:
        raise RuntimeError(f"Katha: English verses incomplete/misaligned: {sorted(en)}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_english()
    rows = []
    for valli in range(1, 7):
        for vn in range(1, VALLI_SIZES[valli] + 1):
            rows.append({
                "devanagari": dev[(valli, vn)],
                "translation": en[(valli, vn)],
                "chapter": valli,
                "verse": vn,
            })
    return rows
