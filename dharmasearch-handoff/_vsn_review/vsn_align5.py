#!/usr/bin/env python3
"""VSN aligner v5 - multi-candidate consonant-skeleton matching.
For each Sastry gloss, generate ALL candidate name-tokens; at the current
position in the authoritative verse skeleton, consume whichever candidate
matches (longest, sandhi-tolerant). Ground truth = sanskritdocuments Devanagari
verses. Cross-check counts vs deerao75. Diagnostic only."""
import re
import html
import requests
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "*/*"}
DEVA_DIGITS = "०१२३४५६७८९"
DEVA_MAP = {c: str(i) for i, c in enumerate(DEVA_DIGITS)}
VOWELS = set("aeiou")


def d2i(s):
    return int("".join(DEVA_MAP.get(c, c) for c in s))


def skel(roman):
    s = roman.lower()
    repl = {"ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṝ": "r", "ḷ": "l", "ṃ": "m", "ṁ": "m",
            "ḥ": "", "ṅ": "n", "ñ": "n", "ṭ": "t", "ḍ": "d", "ṇ": "n", "ś": "s", "ṣ": "s",
            "'": "", "’": "", "^": "", "~": "", "-": "", ".": ""}
    for k, v in repl.items():
        s = s.replace(k, v)
    s = s.replace("sh", "s").replace("ch", "c").replace("th", "t").replace("ph", "p").replace("kh", "k")
    s = re.sub(r"[^a-z]", "", s)
    s = "".join(ch for ch in s if ch not in VOWELS)
    s = re.sub(r"(.)\1+", r"\1", s)
    return s


def fetch_verses():
    d = requests.get("https://sanskritdocuments.org/doc_vishhnu/vsahasranew.html", headers=H, timeout=25).text
    dtx = html.unescape(re.sub(r"<[^>]+>", " ", d))
    ms = list(re.finditer(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", dtx))
    span = dtx[ms[28].end():ms[136].end()]
    parts = re.split(r"॥\s*([" + DEVA_DIGITS + r"]+)\s*॥", span)
    verses = {}
    for i in range(1, len(parts), 2):
        v = re.sub(r"\s+", " ", parts[i - 1]).strip().rstrip("।॥").strip()
        verses[d2i(parts[i])] = v
    v1 = verses[1]
    verses[1] = v1[v1.find("विश्वं"):] if "विश्वं" in v1 else v1
    return verses


def fetch_sastry_names():
    r = requests.get(
        "https://archive.org/download/in.ernet.dli.2015.1291/2015.1291.The-Vishnu-Sahasranama-1927_djvu.txt",
        headers=H, timeout=60)
    txt = r.text
    start = txt.find("1. Vi")
    end = txt.find("1000.")
    end = txt.find(".", end + 300)
    section = "\n" + txt[start:end + 400]
    section = (section.replace("\n55].", "\n551.").replace("\n907 .", "\n907.")
               .replace("\n96K.", "\n968.").replace("124.1", "124."))
    matches = list(re.finditer(r"\n[^\w\n]{0,3}(\d{1,4})\.\s", section))
    names = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
        s = m.end()
        e = matches[i + 1].start() if i + 1 < len(matches) else len(section)
        names.setdefault(n, re.sub(r"\s+", " ", section[s:e].split("\n\n")[0]).strip())
    return names


def candidate_skels(gloss):
    cands = []
    for pm in re.finditer(r"\(([^)]+)\)", gloss):
        inner = pm.group(1)
        if not re.search(r"\d", inner):
            cands.append(skel(inner))
    for w in re.findall(r"[A-Za-z][A-Za-z'’^~-]{1,30}", gloss):
        cands.append(skel(w))
    cands.append(skel(gloss.split(".")[0]))
    return [c for c in cands if len(c) >= 2]


def fetch_deerao_counts():
    ts = requests.get("https://raw.githubusercontent.com/deerao75/vishnusahasranama/main/src/data/shlokas.ts",
                      headers=H, timeout=25).text
    blocks = re.split(r"\{\s*number:\s*(\d+),", ts)
    counts = {}
    for i in range(1, len(blocks), 2):
        eng = re.search(r'englishMeaning:\s*"((?:[^"\\]|\\.)*)"', blocks[i + 1])
        counts[int(blocks[i])] = len(re.findall(r"\d+\.\s", eng.group(1))) if eng else 0
    return counts


if __name__ == "__main__":
    verses = fetch_verses()
    names = fetch_sastry_names()
    dcounts = fetch_deerao_counts()
    vskel = {vn: skel(transliterate(dev, sanscript.DEVANAGARI, sanscript.IAST)) for vn, dev in verses.items()}
    ncands = {n: candidate_skels(g) for n, g in names.items()}

    assignment = {vn: [] for vn in range(1, 109)}
    cur = 1
    for vn in range(1, 109):
        rem = vskel[vn]
        while cur <= 1000:
            best = None
            for cand in ncands[cur]:
                for probe in (cand, cand[:-1], cand[:-2]):
                    if len(probe) < 2:
                        continue
                    p = rem.find(probe)
                    if p != -1 and p <= 2:
                        if best is None or (p, -len(probe)) < best[0]:
                            best = ((p, -len(probe)), p + len(probe))
                        break
            if best is not None:
                rem = rem[best[1]:]
                assignment[vn].append(cur)
                cur += 1
            else:
                break

    total = sum(len(a) for a in assignment.values())
    empties = [vn for vn, a in assignment.items() if not a]
    print("total assigned:", total, "/1000 | next unconsumed name:", cur if cur <= 1000 else "ALL 1000 DONE")
    print("empty verses:", empties[:30])
    off = [(vn, len(assignment[vn]), dcounts.get(vn)) for vn in range(1, 109)
           if abs(len(assignment[vn]) - dcounts.get(vn, 0)) > 2]
    print("verses differing >2 from deerao count:", off[:25])
    print("v1:", len(assignment[1]), "v2:", len(assignment[2]), "v3:", len(assignment[3]),
          "v108:", len(assignment[108]))
