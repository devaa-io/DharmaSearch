# loaders/mundaka.py
#
# Mundaka Upanishad - 64 verses across 3 mundakas x 2 khandas each
# (sizes 9/13, 10/11, 10/11), Atharva Veda. "Two birds on one tree" - the
# higher and lower knowledge, and the path to the imperishable Brahman.
#
# SOURCES:
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/mundaka.html)
#                Real Unicode Devanagari, section-headed
#                "<mundaka> मुण्डके <khanda> खण्डः" (e.g. "प्रथममुण्डके प्रथमः खण्डः").
#
#   English    : Max Muller, "The Upanishads, Part II", Sacred Books of the East
#                Vol. 15 (Oxford, 1884), the "Mundaka-upanishad" chapter, via
#                English Wikisource. LICENSING: Muller died 1900 -> public domain
#                worldwide, same pattern already used for Isha/Kena/Katha.
#
# Rows are keyed by (mundaka 1-3, khanda 1-2, verse). Unlike Katha, this
# edition's verse numbers ARE contiguous within each khanda on both sides, so
# no positional-alignment workaround is needed here.
import re
import html
import requests
from loaders._wikisource import rendered_text

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/mundaka.html"
EN_TITLE = "Sacred Books of the East/Volume 15/Mundaka-upanishad"
WS_API = "https://en.wikisource.org/w/api.php"

DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}
KHANDA_SIZES = {(1, 1): 9, (1, 2): 13, (2, 1): 10, (2, 2): 11, (3, 1): 10, (3, 2): 11}
MUNDAKA_WORDS = {"प्रथम": 1, "द्वितीय": 2, "तृतीय": 3}
KHANDA_WORDS = {"प्रथमः": 1, "द्वितीयः": 2}


def _deva2int(s: str) -> int:
    return int("".join(DEVA_MAP.get(ch, ch) for ch in s))


def _fetch_devanagari():
    """Return {(mundaka, khanda, verse): devanagari_text} for all 64 verses."""
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    raw = response.text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))

    heads = list(re.finditer(
        r"॥\s*(प्रथम|द्वितीय|तृतीय)\s*मुण्डके\s*(प्रथमः|द्वितीयः)\s*खण्डः\s*॥", txt))
    if len(heads) != 6:
        raise RuntimeError(f"Mundaka: expected 6 section headers, found {len(heads)}")
    end = txt.rfind("॥ इति मुण्डकोपनिषत् ॥")
    if end < 0:
        end = len(txt)

    dev = {}
    for idx, m in enumerate(heads):
        s = m.end()
        e = heads[idx + 1].start() if idx + 1 < len(heads) else end
        mund, kh = MUNDAKA_WORDS[m.group(1)], KHANDA_WORDS[m.group(2)]
        body = txt[s:e]
        parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", body)
        for i in range(1, len(parts), 2):
            vn = _deva2int(parts[i])
            v = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip() + " ॥"
            dev[(mund, kh, vn)] = v

    if len(dev) != 64:
        raise RuntimeError(f"Mundaka: expected 64 verses, parsed {len(dev)}")
    return dev


def _fetch_english():
    """Return {(mundaka, khanda, verse): Muller English} for all 64 verses."""
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
    txt = txt.split("↑")[0]
    txt = re.split(r"\bFootnotes\b", txt, maxsplit=1, flags=re.I)[0]

    mheads = list(re.finditer(r"(First|Second|Third)\s+Mu\s*nd\s*aka", txt, re.I))
    if len(mheads) != 3:
        raise RuntimeError(f"Mundaka: expected 3 Mundaka headers, found {len(mheads)}")
    mund_words = {"first": 1, "second": 2, "third": 3}

    en = {}
    for midx, mm in enumerate(mheads):
        ms = mm.end()
        me = mheads[midx + 1].start() if midx + 1 < len(mheads) else len(txt)
        mund_body = txt[ms:me]
        mund = mund_words[mm.group(1).lower()]

        kheads = list(re.finditer(r"(First|Second)\s+Kh\s*anda", mund_body, re.I))
        if len(kheads) != 2:
            raise RuntimeError(f"Mundaka {mund}: expected 2 Khanda headers, found {len(kheads)}")
        kh_words = {"first": 1, "second": 2}
        for kidx, km in enumerate(kheads):
            ks = km.end()
            ke = kheads[kidx + 1].start() if kidx + 1 < len(kheads) else len(mund_body)
            kh = kh_words[km.group(1).lower()]
            kbody = mund_body[ks:ke]
            for vm in re.finditer(r"(?:^|\s)(\d{1,2})\.\s+(.+?)(?=\s\d{1,2}\.\s|\Z)", kbody, re.S):
                vn = int(vm.group(1))
                if (mund, kh, vn) not in en:
                    en[(mund, kh, vn)] = " ".join(vm.group(2).split())

    if len(en) != 64:
        raise RuntimeError(f"Mundaka: expected 64 English verses, got {len(en)}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_english()
    rows = []
    for (mund, kh), size in sorted(KHANDA_SIZES.items()):
        for vn in range(1, size + 1):
            key = (mund, kh, vn)
            rows.append({
                "devanagari": dev[key],
                "translation": en[key],
                "chapter": (mund - 1) * 2 + kh,   # 1..6 global section index
                "verse": vn,
            })
    return rows
