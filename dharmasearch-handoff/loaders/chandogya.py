# loaders/chandogya.py
"""Chandogya Upanishad: 627 marked passages in 8 prapathakas.

Devanagari is parsed only at the source's leading danda + three-part marker
(``॥ p.k.v``).  The page currently has two bare number-like strings in 5.17
without that delimiter; they are deliberately not treated as verse markers.

Muller's SBE translation sometimes combines the final two Sanskrit passages of
a khanda, or splits one Sanskrit passage into two numbered paragraphs.  Those
small, explicit segmentation differences are reconciled within that khanda.
The Sanskrit 6.6 markers also jump from 4 to 6; as with Katha valli 3, its five
segments are aligned positionally so no later passage is displaced.
"""
import html
import re

import requests

from loaders._wikisource import rendered_text


DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/chhaandogya.html"
WS_API = "https://en.wikisource.org/w/api.php"
EN_TITLES = [
    f"Sacred Books of the East/Volume 1/Khândogya-upanishad/{word} Prapâthaka"
    for word in ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")
]
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
WS_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}
DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = str.maketrans(DEVA_DIGITS, "0123456789")

# Counts produced by the required leading-marker grammar.  5.17 has no such
# markers on the source page, so it contributes no rows to the 627-row edition.
KHANDA_SIZES = {
    1: [10,14,12,5,5,8,9,8,4,11,9,5,4],
    2: [4,3,2,2,2,2,2,3,8,6,2,2,2,2,2,2,2,2,2,2,4,5,3,16],
    3: [4,3,3,3,4,4,4,4,4,4,6,9,8,4,7,7,7,6,4],
    4: [8,5,8,5,3,4,4,4,3,5,2,2,2,3,5,5,10],
    5: [15,8,7,2,2,2,2,2,2,10,7,2,2,2,2,2,0,2,2,2,2,2,2,5],
    6: [7,4,4,7,4,5,6,7,4,3,3,3,3,3,3,3],
    7: [5,2,2,3,3,2,2,2,2,2,2,2,2,2,4,1,1,1,1,1,1,1,1,2,2,2],
    8: [6,10,5,3,4,6,4,5,3,4,3,6,1,1,1],
}


def _clean_dev(chunk):
    # Drop a completed-khanda label between the preceding marker and this verse.
    chunk = re.sub(r"^.*॥\s*इति[^॥]*खण्डः\s*॥", "", chunk, flags=re.S)
    chunk = re.sub(r"^.*॥\s*प्रथमोऽध्यायः\s*॥", "", chunk, flags=re.S)
    return re.sub(r"\s+", " ", chunk).strip().lstrip("।॥ ").rstrip("।॥ ") + " ॥"


def _fetch_devanagari():
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=45)
    response.raise_for_status()
    text = html.unescape(re.sub(r"<[^>]+>", " ", response.text))
    marker = re.compile(
        r"॥\s*([" + DEVA_DIGITS + r"]+)\.([" + DEVA_DIGITS + r"]+)\.([" + DEVA_DIGITS + r"]+)"
    )
    matches = list(marker.finditer(text))
    if len(matches) != 627:
        raise RuntimeError(f"Chandogya: expected 627 leading triplet markers, found {len(matches)}")
    out = {}
    previous = 0
    for match in matches:
        p, k, printed = (int(value.translate(DEVA_MAP)) for value in match.groups())
        key = (p, k)
        position = 1 + sum(1 for pp, kk, _ in out if (pp, kk) == key)
        out[(p, k, position)] = _clean_dev(text[previous:match.start()])
        previous = match.end()
    expected = {(p, k): size for p, sizes in KHANDA_SIZES.items() for k, size in enumerate(sizes, 1)}
    actual = {(p, k): sum(1 for pp, kk, _ in out if (pp, kk) == (p, k)) for p, k in expected}
    if actual != expected:
        raise RuntimeError(f"Chandogya: unexpected Devanagari khanda counts: {actual}")
    return out


def _segments(body):
    matches = list(re.finditer(r"(?m)^(\d+(?:,\s*\d+)?)\.\s+", body))
    out = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        text = " ".join(body[match.end():end].split())
        numbers = [int(n) for n in re.findall(r"\d+", match.group(1))]
        out.extend([text] * len(numbers))
    return out


def _fit_segments(items, wanted, p, k):
    if wanted == 0:
        return []
    if len(items) == wanted:
        return items
    note = " [Müller's edition combines this translation with the adjacent Sanskrit passage.]"
    if len(items) == wanted - 1:
        # In every such khanda the final Müller paragraph covers its final two
        # Sanskrit markers (confirmed against both source texts).
        items[-1] += note
        return items + [items[-1]]
    if len(items) == wanted + 1:
        # Here the Sanskrit source has one marker for Müller's first two
        # numbered paragraphs; retain both English paragraphs in that row.
        return [items[0] + " " + items[1]] + items[2:]
    raise RuntimeError(f"Chandogya {p}.{k}: cannot align {len(items)} English segments to {wanted}")


def _fetch_english():
    out = {}
    for p, title in enumerate(EN_TITLES, 1):
        response = requests.get(
            WS_API,
            params={"action": "parse", "page": title, "prop": "text", "format": "json", "formatversion": 2},
            headers=WS_HEADERS, timeout=45,
        )
        response.raise_for_status()
        source_html = re.sub(r"^\s*<style\b.*?</style>", "", response.json()["parse"]["text"], flags=re.S | re.I)
        text = rendered_text(source_html).split("↑", 1)[0]
        text = re.split(r"\bFootnotes\b", text, maxsplit=1, flags=re.I)[0]
        heads = list(re.finditer(r"(?im)^[A-Za-z-]+\s+Khanda\.\s*$", text))
        if len(heads) != len(KHANDA_SIZES[p]):
            raise RuntimeError(f"Chandogya prapathaka {p}: expected {len(KHANDA_SIZES[p])} khanda headings, found {len(heads)}")
        for index, head in enumerate(heads):
            k = index + 1
            end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
            items = _segments(text[head.end():end])
            # The unmarked Sanskrit 5.17 material is outside this 627-marker
            # edition, so omit the corresponding Müller khanda too.
            items = _fit_segments(items, KHANDA_SIZES[p][index], p, k)
            for position, translation in enumerate(items, 1):
                out[(p, k, position)] = translation
    if len(out) != 627:
        raise RuntimeError(f"Chandogya: expected 627 English rows, got {len(out)}")
    return out


def load():
    dev = _fetch_devanagari()
    english = _fetch_english()
    if dev.keys() != english.keys():
        raise RuntimeError("Chandogya: source identities do not align")
    return [
        {
            "devanagari": dev[key], "translation": english[key],
            "chapter": key[0] * 100 + key[1], "verse": key[2],
        }
        for key in sorted(dev)
    ]
