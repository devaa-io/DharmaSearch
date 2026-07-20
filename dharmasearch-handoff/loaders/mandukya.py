# loaders/mandukya.py
#
# Mandukya Upanishad - 12 verses, Atharva Veda. The shortest principal
# Upanishad: the syllable Om analysed into its four matras (a/u/m/silence)
# mapped onto the four states of consciousness (waking/dream/deep sleep/turiya).
#
# SOURCES:
#   Devanagari : sanskritdocuments.org  (doc_upanishhat/maandu.html)
#                Real Unicode Devanagari, 12 verses, no chapter subdivisions.
#
#   English    : Robert Ernest Hume, "The Thirteen Principal Upanishads"
#                (Oxford University Press, 1921), via the archive.org OCR scan
#                (identifier: thirteenprincipa028442mbp).
#                LICENSING: published 1921, in the United States -> public
#                domain in the US (all works published before 1929 are PD
#                regardless of author death date; Hume died 1948, so this is
#                PD on both grounds).
#                NOTE ON FIDELITY: the archive.org text is OCR'd from a 1921
#                scan and has scanning noise (misplaced footnote markers, a
#                few misread characters in the Sanskrit glosses, page-break
#                artifacts). Rather than parse that noisy OCR automatically at
#                pipeline-run time - which risks a silent misalignment for a
#                sacred text - the 12 verses below were manually transcribed
#                from the OCR output and cross-checked against the raw scan
#                text, preserving Hume's exact wording. Only OCR noise
#                (footnote numbers, stray page numbers, scanning glitches) was
#                removed; no wording was changed or modernised.
import re
import html
import requests

DEV_URL = "https://sanskritdocuments.org/doc_upanishhat/maandu.html"
DEV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}

DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}

ENGLISH = {
    1: ("Om!—This syllable is this whole world. Its further explanation is:— "
        "The past, the present, the future—everything is just the word Om. "
        "And whatever else that transcends threefold time—that, too, is just the word Om."),
    2: ("For truly, everything here is Brahma; this self (ātman) is Brahma. "
        "This same self has four fourths."),
    3: ("The waking state (jāgarita-sthāna), outwardly cognitive, having seven limbs, "
        "having nineteen mouths, enjoying the gross (sthūla-bhuj), the Common-to-all-men "
        "(vaiśvānara), is the first fourth."),
    4: ("The dreaming state (svapna-sthāna), inwardly cognitive, having seven limbs, "
        "having nineteen mouths, enjoying the exquisite (pravivikta-bhuj), the Brilliant "
        "(taijasa), is the second fourth."),
    5: ("If one asleep desires no desire whatsoever, sees no dream whatsoever—that is deep "
        "sleep (suṣupta). The deep-sleep state (suṣupta-sthāna), unified (ekī-bhūta), "
        "just a cognition-mass (prajñāna-ghana), consisting of bliss (ānanda-maya), "
        "enjoying bliss (ānanda-bhuj), whose mouth is thought (cetas), the Cognitional "
        "(prājña), is the third fourth."),
    6: ("This is the lord of all (sarveśvara). This is the all-knowing (sarva-jña). This is "
        "the inner controller (antaryāmin). This is the source (yoni) of all, for this is "
        "the origin and the end of beings."),
    7: ("Not inwardly cognitive, not outwardly cognitive, not both-wise cognitive, not a "
        "cognition-mass, not cognitive, not non-cognitive, unseen, with which there can be no "
        "dealing, ungraspable, having no distinctive mark, non-thinkable, that cannot be "
        "designated, the essence of the assurance of which is the state of being one with the "
        "Self, the cessation of development, tranquil, benign, without a second—[such] they "
        "think is the fourth. He is the Self (Ātman). He should be discerned."),
    8: ("This is the Self with regard to the word Om, with regard to its elements. The "
        "elements are the fourths; the fourths, the elements: the letter a, the letter u, "
        "the letter m."),
    9: ("The waking state, the Common-to-all-men, is the letter a, the first element, from "
        "āpti ('obtaining') or from ādimatva ('being first'). He obtains, verily, indeed, "
        "all desires, he becomes first—he who knows this."),
    10: ("The sleeping state, the Brilliant, is the letter u, the second element, from "
         "utkarṣa ('exaltation') or from ubhayatva ('intermediateness'). He exalts, verily, "
         "indeed, the continuity of knowledge; and he becomes equal (samāna); no one ignorant "
         "of Brahma is born in the family of him who knows this."),
    11: ("The deep-sleep state, the Cognitional, is the letter m, the third element, from "
         "miti ('erecting') or from apīti ('immerging'). He, verily, indeed, erects (minoti) "
         "this whole world, and he becomes its immerging—he who knows this."),
    12: ("The fourth is without an element, with which there can be no dealing, the cessation "
         "of development, benign, without a second. Thus Om is the Self (Ātman) indeed. He "
         "who knows this, with his self enters the Self—yea, he who knows this!"),
}


def _deva2int(s: str) -> int:
    return int("".join(DEVA_MAP.get(ch, ch) for ch in s))


def _fetch_devanagari():
    """Return {verse: devanagari_text} for all 12 Mandukya verses."""
    raw = requests.get(DEV_URL, headers=DEV_HEADERS, timeout=30).text
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    marker = txt.find("इत्येतदक्षर")
    start = txt.rfind("ॐ", 0, marker) if marker >= 0 else -1
    if start < 0:
        raise RuntimeError("Mandukya: could not locate verse span in source page")
    end = txt.find("॥ १२॥", start)
    if end < 0:
        raise RuntimeError("Mandukya: could not locate closing verse 12 marker")
    span = txt[start:end + len("॥ १२॥")]
    parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", span)
    dev = {}
    for i in range(1, len(parts), 2):
        vn = _deva2int(parts[i])
        v = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip() + " ॥"
        dev[vn] = v
    if len(dev) != 12 or sorted(dev) != list(range(1, 13)):
        raise RuntimeError(f"Mandukya: expected 12 verses, parsed {sorted(dev)}")
    return dev


def load():
    dev = _fetch_devanagari()
    rows = []
    for vn in range(1, 13):
        rows.append({
            "devanagari": dev[vn],
            "translation": ENGLISH[vn],
            "verse": vn,
        })
    return rows
