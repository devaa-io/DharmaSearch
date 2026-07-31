# loaders/hanuman_chalisa.py
#
# Hanuman Chalisa - Tulsidas's 40 chaupais (quatrains) in praise of Hanuman,
# framed by two opening dohas (couplets).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org (doc_hanumaana/hanuman40.html) - the
#     original Awadhi text (NOT the separate Sanskrit-translation page on the
#     same site, doc_hanumaana/hanumAnachAlisAsaMskRRita.html, which is a
#     different, modern derivative work by Ravindra Kumar Markandeya).
#
#   English : P. R. Ramachander, hosted at celextel.org's Vedanta Spiritual
#     Library - same source/site already accepted for Vishnu Sahasranama,
#     Soundarya Lahari and Lalita Sahasranama.
#
# NUMBERING (the thing to be careful about here):
#   Chaupais keep their canonical numbers 1-40, in their own section, so a
#   reader cross-referencing any other edition lands on the same verse. The
#   two dohas are section 1; the chaupais are section 2 numbered from 1.
#
#   Celextel's translation combines two pairs of chaupais under one shared
#   English paragraph each (14+15 and 33+34): the pair's two romanised
#   couplets run together with no blank line, followed by a single English
#   block covering both. An earlier version of this loader merged the
#   Devanagari to match, which silently shifted every subsequent verse out of
#   step with canonical numbering - the exact "user says it is wrong" failure
#   this project exists to avoid. Instead both members of such a pair keep
#   their own number and Devanagari, and share the combined translation with
#   a parenthetical note saying so.
#
#   Celextel's own printed verse numbers are NOT trustworthy as indices: the
#   page labels one chaupai 19 and the following one 18, and prints 19 twice.
#   So couplets are counted in document order and assigned canonical numbers
#   positionally; the source's digits are only used to detect how many
#   couplets a block holds, never to decide which verse it is.
#
#   Scope: the source page's closing doha ("pavana-tanaya sankata harana...")
#   and its Aarti are excluded, as celextel translates neither.
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

DOHA_SECTION = 1
CHAUPAI_SECTION = 2

# A standalone 1-2 digit token, i.e. a printed verse number rather than a
# digit embedded in a word. Numbers inside the verses themselves are always
# spelled out in this text ("sahasra", "sat baar"), never written as digits.
NUMBER_TOKEN = re.compile(r"(?<![\w.])\d{1,2}(?![\w.])")


def _fetch_devanagari():
    """Return (2 doha couplets, 40 chaupai couplets), each as one string."""
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
    # The closing doha sits between the last chaupai and the Aarti.
    chaupai_block = chaupai_block[:chaupai_block.rfind("दोहा")]

    doha_lines = [l.strip() for l in doha_block.split("\n") if l.strip()]
    chaupai_lines = [l.strip() for l in chaupai_block.split("\n") if l.strip()]

    if len(doha_lines) != 4:
        raise RuntimeError(f"Hanuman Chalisa: expected 4 opening doha lines, got {len(doha_lines)}")
    if len(chaupai_lines) != 80:
        raise RuntimeError(f"Hanuman Chalisa: expected 80 chaupai lines, got {len(chaupai_lines)}")

    dohas = [" ".join(doha_lines[0:2]), " ".join(doha_lines[2:4])]
    chaupais = [" ".join(chaupai_lines[2 * i:2 * i + 2]) for i in range(40)]
    return dohas, chaupais


def _fetch_translation():
    """Return (2 doha translations, {chaupai_no: english}, shared-number groups)."""
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

    # blocks[0..3] are the two dohas as [roman, english, roman, english];
    # from index 4 the same alternation continues, except a roman block may
    # carry two couplets where celextel merged the translation.
    dohas = [blocks[1], blocks[3]]

    chaupai_en = {}
    shared_groups = []
    next_number = 1
    i = 4
    while i < len(blocks):
        roman, english = blocks[i], blocks[i + 1]
        couplet_count = len(NUMBER_TOKEN.findall(roman))
        if couplet_count == 0:
            raise RuntimeError(f"Hanuman Chalisa: no verse number in roman block {i}: {roman[:60]!r}")
        covered = tuple(range(next_number, next_number + couplet_count))
        for n in covered:
            chaupai_en[n] = english
        if couplet_count > 1:
            shared_groups.append(covered)
        next_number += couplet_count
        i += 2

    total = next_number - 1
    if total != 40:
        raise RuntimeError(f"Hanuman Chalisa: expected 40 chaupai translations, got {total}")
    return dohas, chaupai_en, shared_groups


def load():
    dev_dohas, dev_chaupais = _fetch_devanagari()
    en_dohas, en_chaupais, shared_groups = _fetch_translation()

    shared_of = {n: group for group in shared_groups for n in group}

    rows = []
    for i, couplet in enumerate(dev_dohas, start=1):
        rows.append({
            "devanagari": couplet,
            "english": en_dohas[i - 1],
            "chapter": DOHA_SECTION,
            "verse": i,
        })
    for i, couplet in enumerate(dev_chaupais, start=1):
        english = en_chaupais[i]
        group = shared_of.get(i)
        if group:
            listed = " and ".join(str(n) for n in group)
            english = f"{english} (This translation covers verses {listed} together.)"
        rows.append({
            "devanagari": couplet,
            "english": english,
            "chapter": CHAUPAI_SECTION,
            "verse": i,
        })
    return rows
