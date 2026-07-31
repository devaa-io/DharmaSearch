# loaders/soundarya_lahari.py
#
# Saundaryalahari (Soundarya Lahari) - 100 verses attributed to Adi
# Shankaracharya, in praise of the Divine Mother.
#
# SOURCES:
#   Devanagari : sanskritdocuments.org (doc_devii/saundaryalahari.html).
#     Real Unicode Devanagari, cross-checked by the site's own editors
#     against ten printed editions.
#
#   IAST + English : P. R. Ramachander, hosted at celextel.org's Vedanta
#     Spiritual Library - a long-running, non-commercial Vedanta text
#     repository with an explicit free-distribution ethos and no
#     restrictive-use clause found on the site. Same acceptability bar the
#     owner approved for the Vishnu Sahasranama source on 2026-07-30.
#
#   Verse count: the source text is traditionally 100 verses (Anandalahari
#   1-41, Saundaryalahari 42-100). sanskritdocuments.org's own scholarly
#   notes list 103 verses in some printed editions but explicitly flag
#   101-103 as later interpolations; celextel's translation covers exactly
#   the traditional 100, so only verses 1-100 are used from each source -
#   not a shortcut, the two sources already agree on the canonical scope.
import re
import requests

DEV_URL = "https://sanskritdocuments.org/doc_devii/saundaryalahari.html"
EN_URL = "https://www.celextel.org/adi-sankara/soundarya-lahari/"
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
EN_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}

DEVA_DIGITS = "०१२३४५६७८९"
VERSE_END = re.compile(r"॥\s*([०-९]+)\s*॥")


def _deva_to_int(digits: str) -> int:
    return int("".join(str(DEVA_DIGITS.index(c)) for c in digits))


def _fetch_devanagari() -> dict:
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    text = response.text
    start = text.find("शिवः शक्त्या")
    if start < 0:
        raise RuntimeError("Saundaryalahari: could not locate verse 1 in source page")
    end_marker = text.find("॥ १०३॥")  # the scholarly notes begin right after
    span = text[start:end_marker if end_marker > 0 else start + 40000]

    verses = {}
    cursor = 0
    for m in VERSE_END.finditer(span):
        n = _deva_to_int(m.group(1))
        if n > 100:
            break
        chunk = span[cursor:m.end()]
        chunk = re.sub(r"^\s*आनन्दलहरी[^\n]*\n", "", chunk)  # section headers
        chunk = re.sub(r"^\s*सौन्दर्यलहरी[^\n]*\n", "", chunk)
        verses[n] = re.sub(r"\n+", " ", chunk).strip()
        cursor = m.end()
    return verses


def _fetch_translation() -> dict:
    response = requests.get(EN_URL, headers=EN_HEADERS, timeout=30)
    response.raise_for_status()
    html = response.text

    markers = list(re.finditer(r"<b>(\d+)</b>", html))
    out = {}
    for i, m in enumerate(markers):
        n = int(m.group(1))
        if n > 100:
            continue
        chunk_end = markers[i + 1].start() if i + 1 < len(markers) else len(html)
        # The last verse has no following <b>N</b> to bound it, so without
        # this it swallows the rest of the page (footer, nav menu, ...).
        # Every verse's own content ends at "</p>" regardless; capping there
        # when it comes first handles the last verse without a special case.
        closing_p = html.find("</p>", m.end())
        if closing_p != -1 and closing_p < chunk_end:
            chunk_end = closing_p
        chunk = html[m.end():chunk_end]
        raw_lines = chunk.split("<br>")
        cleaned = [re.sub(r"<[^>]+>", "", ln).strip() for ln in raw_lines]
        # Drop leading blanks and any [bracketed title] line before looking
        # for the real IAST/English separator, or that leading blank gets
        # mistaken for the gap and IAST comes out empty.
        start = next((i for i, ln in enumerate(cleaned) if ln and not ln.startswith("[")), len(cleaned))
        cleaned = cleaned[start:]
        first_blank = next((i for i, ln in enumerate(cleaned) if ln == ""), len(cleaned))
        iast_lines = [ln for ln in cleaned[:first_blank] if ln]
        rest = cleaned[first_blank:]
        second_blank = next((i for i, ln in enumerate(rest) if ln != ""), 0)
        english_lines = [ln for ln in rest[second_blank:] if ln and not ln.startswith("*")]
        if not iast_lines or not english_lines:
            raise RuntimeError(f"Saundaryalahari: could not split verse {n} into iast/english")
        out[n] = {
            "iast": " ".join(iast_lines),
            "english": " ".join(english_lines),
        }
    return out


def load():
    dev = _fetch_devanagari()
    en = _fetch_translation()

    missing_dev = sorted(set(range(1, 101)) - set(dev))
    missing_en = sorted(set(range(1, 101)) - set(en))
    if missing_dev:
        raise RuntimeError(f"Saundaryalahari: missing Devanagari for verses {missing_dev}")
    if missing_en:
        raise RuntimeError(f"Saundaryalahari: missing translation for verses {missing_en}")

    rows = []
    for n in range(1, 101):
        rows.append({
            "devanagari": dev[n],
            "iast": en[n]["iast"],
            "translation": en[n]["english"],
            "verse": n,
        })
    return rows
