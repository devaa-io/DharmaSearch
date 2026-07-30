# loaders/lalita_sahasranama.py
#
# Sri Lalita Sahasranama Stotram - the 1000 names of Lalita Tripurasundari,
# from the Brahmanda Purana (Hayagriva-Agastya dialogue).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org (doc_devii/lalita1000.html) - a
#     name-by-name page (numbered 1-1000), each with the site's own brief
#     English gloss. We take only the Devanagari name from here; IAST is
#     derived from it by the pipeline (script-to-script, lossless).
#
#   English : P. R. Ramachander, hosted at celextel.org's Vedanta Spiritual
#     Library - same source/site already accepted for Vishnu Sahasranama and
#     Soundarya Lahari on 2026-07-30. Also numbered 1-1000, name by name.
#
#   The two sources are independently numbered 1-1000 with zero gaps each
#   (verified before writing this loader), so they align by number without
#   needing to match wording or line-splitting.
import re

import requests

DEV_URL = "https://sanskritdocuments.org/doc_devii/lalita1000.html"
EN_URL = "https://www.celextel.org/devi-stotras/lalita-sahasra-namam/"
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
EN_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
# The name ends at " -" (space then hyphen) marking the start of either the
# site's own gloss or a parenthetical annotation on the same line (e.g. name
# 75: "...तोषिता - (विशुक्रवधतोषिता) (See a note below)"). Matching up to
# " -" rather than any hyphen is required because some names contain an
# internal, unspaced hyphen of their own (name 391: "नित्या-षोडशिकारूपा").
NAME_MARKER = re.compile(r"^([०-९]+)\.\s*(.+?)\s-.*$", re.MULTILINE)


def _deva_to_int(digits: str) -> int:
    return int("".join(str(DEVA_DIGITS.index(c)) for c in digits))


def _fetch_devanagari() -> dict:
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    text = response.text

    names = {}
    for m in NAME_MARKER.finditer(text):
        n = _deva_to_int(m.group(1))
        if n > 1000:
            continue
        names[n] = re.sub(r"\s+", " ", m.group(2)).strip()
    return names


def _fetch_translation() -> dict:
    response = requests.get(EN_URL, headers=EN_HEADERS, timeout=30)
    response.raise_for_status()
    html = response.text

    start = html.find("Sahasra Namam")
    end = html.find("</p>", start)
    span = html[start:end]

    markers = list(re.finditer(r"(?:^|<br>)\s*(\d+)\.\s", span))
    out = {}
    for i, m in enumerate(markers):
        n = int(m.group(1))
        if n > 1000:
            continue
        chunk_end = markers[i + 1].start() if i + 1 < len(markers) else len(span)
        chunk = span[m.end():chunk_end]
        chunk = re.sub(r"<br\s*/?>", " ", chunk)
        chunk = re.sub(r"\s+", " ", chunk).strip()
        out[n] = chunk
    return out


def load():
    dev = _fetch_devanagari()
    en = _fetch_translation()

    missing_dev = sorted(set(range(1, 1001)) - set(dev))
    missing_en = sorted(set(range(1, 1001)) - set(en))
    if missing_dev:
        raise RuntimeError(f"Lalita Sahasranama: missing Devanagari for names {missing_dev}")
    if missing_en:
        raise RuntimeError(f"Lalita Sahasranama: missing translation for names {missing_en}")

    rows = []
    for n in range(1, 1001):
        rows.append({
            "devanagari": dev[n],
            "english": en[n],
            "verse": n,
        })
    return rows
