# loaders/hanuman_chalisa.py
#
# Hanuman Chalisa - Tulsidas's 40 chaupais (quatrains) in praise of Hanuman,
# framed by two opening dohas (couplets).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org (doc_hanumaana/hanuman40.html) - the
#     original Awadhi/Hindi text (NOT the separate Sanskrit-translation page
#     on the same site, doc_hanumaana/hanumAnachAlisAsaMskRRita.html, which
#     is a different, modern derivative work by Ravindra Kumar Markandeya).
#
#   English : P. R. Ramachander, hosted at celextel.org's Vedanta Spiritual
#     Library - same source/site already accepted for Vishnu Sahasranama,
#     Soundarya Lahari and Lalita Sahasranama.
#
#   Scope: this edition is shipped as 40 verses (2 opening dohas + 38
#   chaupai units), not the traditional 43 (or even 42). The
#   sanskritdocuments.org page also carries a closing doha ("pavana-tanaya
#   sankata harana...") and a separate Aarti, which celextel does not
#   translate, so both are excluded. Separately, celextel's own translation
#   silently combines two pairs of chaupais under one shared English
#   paragraph each - chaupais 14+15 ("Sanakadhika brahmadhi muneesa... /
#   Yama, Kubhera dikapala...") and 33+34 ("Thumhare bhajan ram ko pavai... /
#   Antha kala Raghupati pura jayee...") - confirmed by reading the raw page:
#   each pair's two romanised couplets run together with no blank line
#   between them, under one English block that covers both. Rather than
#   inventing a translation split or duplicating one translation across two
#   Devanagari couplets, those two Devanagari couplet-pairs are merged into
#   one verse each here too, so every shipped verse has an honest 1:1
#   Devanagari-to-English correspondence.
import html
import re

import requests

DEV_URL = "https://sanskritdocuments.org/doc_hanumaana/hanuman40.html"
EN_URL = "https://www.celextel.org/hanuman-stotras/hanuman-chalisa/"
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
EN_HEADERS = {"User-Agent": "DharmaSearch/1.0 (scripture ingest; research use)"}


def _fetch_devanagari() -> dict:
    response = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    text = response.text

    pre_start = text.find("<PRE")
    tag_end = text.find(">", pre_start) + 1
    pre_end = text.find("</PRE>")
    pre = text[tag_end:pre_end]
    pre = re.sub(r"<h2[^>]*>.*?</h2>", "", pre, flags=re.S)
    pre = html.unescape(pre)

    doha_start = pre.find("दोहा")
    chaupai_start = pre.find("चौपाई")
    aarti_start = pre.find("आरती")

    doha_block = pre[doha_start + len("दोहा"):chaupai_start]
    chaupai_block = pre[chaupai_start + len("चौपाई"):aarti_start]
    closing_doha_idx = chaupai_block.rfind("दोहा")
    chaupai_block = chaupai_block[:closing_doha_idx]

    doha_lines = [l.strip() for l in doha_block.split("\n") if l.strip()]
    chaupai_lines = [l.strip() for l in chaupai_block.split("\n") if l.strip()]

    if len(doha_lines) != 4:
        raise RuntimeError(f"Hanuman Chalisa: expected 4 opening doha lines, got {len(doha_lines)}")
    if len(chaupai_lines) != 80:
        raise RuntimeError(f"Hanuman Chalisa: expected 80 chaupai lines, got {len(chaupai_lines)}")

    chaupai_couplets = [
        " ".join(chaupai_lines[2 * i:2 * i + 2]) for i in range(40)
    ]
    # 0-indexed chaupai numbers 13,14 (=14th,15th) and 32,33 (=33rd,34th)
    # merge into one verse each - see the module docstring for why.
    merged = []
    skip_next = False
    for i, couplet in enumerate(chaupai_couplets):
        if skip_next:
            skip_next = False
            continue
        if i in (13, 32):
            merged.append(couplet + " " + chaupai_couplets[i + 1])
            skip_next = True
        else:
            merged.append(couplet)
    if len(merged) != 38:
        raise RuntimeError(f"Hanuman Chalisa: expected 38 chaupai units after merging, got {len(merged)}")

    dev = {}
    dev[1] = " ".join(doha_lines[0:2])
    dev[2] = " ".join(doha_lines[2:4])
    for i, couplet in enumerate(merged):
        dev[3 + i] = couplet
    return dev


def _fetch_translation() -> dict:
    response = requests.get(EN_URL, headers=EN_HEADERS, timeout=30)
    response.raise_for_status()
    html_text = response.text

    start = html_text.find("Sri Guru charana saroja raj")
    end = html_text.find("Thulasidasa sada Hari Chera")
    end = html_text.find("</p>", end)
    span = html_text[start:end]

    raw_lines = [html.unescape(re.sub(r"<[^>]+>", "", ln)).strip() for ln in span.split("<br>")]
    blocks = []
    current = []
    for ln in raw_lines:
        if ln == "":
            if current:
                blocks.append(" ".join(current))
                current = []
        else:
            current.append(ln)
    if current:
        blocks.append(" ".join(current))

    # Blocks normally alternate [roman, english, roman, english, ...], but at
    # the two merge points (see module docstring) one roman block covers two
    # chaupais and is followed by a single english block for both - so pair
    # by classifying each block rather than assuming fixed alternation.
    # Chaupai roman blocks are the only ones ending in a verse-number digit;
    # the two opening-doha roman blocks are unnumbered, handled positionally.
    en = {}
    en[1] = blocks[1]
    en[2] = blocks[3]
    chaupai_num = 0
    i = 4
    while i < len(blocks):
        if not re.search(r"\d\.?\s*$", blocks[i]):
            raise RuntimeError(f"Hanuman Chalisa: expected a numbered verse block at index {i}: {blocks[i]!r}")
        chaupai_num += 1
        en[2 + chaupai_num] = blocks[i + 1]
        i += 2
    if chaupai_num != 38:
        raise RuntimeError(f"Hanuman Chalisa: expected 38 chaupai translation units, got {chaupai_num}")
    return en


def load():
    dev = _fetch_devanagari()
    en = _fetch_translation()

    missing_en = sorted(set(dev) - set(en))
    if missing_en:
        raise RuntimeError(f"Hanuman Chalisa: missing translation for verses {missing_en}")

    rows = []
    for n in range(1, 41):
        rows.append({
            "devanagari": dev[n],
            "english": en[n],
            "verse": n,
        })
    return rows
