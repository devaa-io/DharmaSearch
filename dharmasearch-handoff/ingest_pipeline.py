#!/usr/bin/env python3
"""
DharmaSearch scripture ingestion pipeline
=========================================

Purpose
-------
Turn an authoritative Devanagari source for any Hindu text into a COMPLETE,
gap-free dataset carrying seven representations per verse:

    devanagari | iast | malayalam | tamil | telugu | kannada | english

The design rule this enforces: transliteration is only ever done SCRIPT -> SCRIPT
from correct Devanagari. It never guesses from lossy ASCII romanisation. That is
what keeps sacred text faithful (long vowels, retroflexes and sibilants survive).

It also enforces the "not half done" rule with a hard gap gate: if ANY verse is
missing ANY field, the build FAILS and tells you exactly which verses and fields,
rather than silently shipping a partial text.

Why this runs on YOUR infrastructure, not in the chat sandbox
-------------------------------------------------------------
The Bhagavad Gita had a clean MIT-licensed GitHub dataset (gita/gita), so it was
completed in-session. The other 15 texts live in scholarly archives the sandbox
cannot reach - sanskritdocuments.org, GRETIL, the Muktabodha and Vedanta corpora.
Run this on a machine with open network access (your laptop, a Render job, etc.)
and those sources are one fetch away.

Requirements
------------
    python3 -m pip install -r requirements.txt

Usage
-----
    python3 ingest_pipeline.py --config sources/isha_config.json --out data/isha-upanishad.json

Each source config is a small JSON file you write per text (see SOURCE_CONFIG_SPEC
and the worked Gita example at the bottom). The pipeline is source-agnostic: you
supply a loader that returns a list of raw verse dicts, and a field map telling the
pipeline which keys hold Devanagari / IAST / English.

Author: built for devaa-io/DharmaSearch
License: MIT (matching the app)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

from pipeline_io import write_text_atomic
from pipeline_validation import validate_dataset

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
except ImportError:
    sys.exit("Missing dependency. Run: python3 -m pip install -r requirements.txt")


# ----------------------------------------------------------------------------
# The four southern scripts we generate from Devanagari. Hindi shares Devanagari,
# so it is not re-transliterated; IAST/English come from the source.
# ----------------------------------------------------------------------------
TARGET_SCRIPTS = [
    ("ml", sanscript.MALAYALAM),
    ("ta", sanscript.TAMIL),
    ("te", sanscript.TELUGU),
    ("kn", sanscript.KANNADA),
]

REQUIRED_FIELDS = ["devanagari", "iast", "english", "ml", "ta", "te", "kn"]


# ----------------------------------------------------------------------------
# Cleaning helpers
# ----------------------------------------------------------------------------
def clean_devanagari(s: str) -> str:
    """Strip inline verse-number tags (।।1.1।।), CRs, and collapse blank lines.
    Keeps speaker lines (e.g. 'धृतराष्ट्र उवाच') and the danda punctuation."""
    if not s:
        return ""
    s = s.replace("\r", "")
    s = re.sub(r"[।॥]*\s*\d+[\.\-]\d+\s*[।॥]*", "", s)   # ।।1.1।। style tags
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return s


def source_text(value) -> str:
    """Return source text without converting nulls or other values into scripture."""
    return value if isinstance(value, str) else ""


def to_scripts(devanagari: str) -> dict:
    """Lossless Devanagari -> southern scripts. Returns {code: text}."""
    out = {}
    for code, scheme in TARGET_SCRIPTS:
        try:
            out[code] = transliterate(devanagari, sanscript.DEVANAGARI, scheme)
        except Exception:
            out[code] = ""   # empty -> caught by the gap gate
    return out


def derive_iast(devanagari: str) -> str:
    """Fallback IAST if the source lacks it - generated from Devanagari, so faithful."""
    try:
        return transliterate(devanagari, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:
        return ""


# ----------------------------------------------------------------------------
# Source config
# ----------------------------------------------------------------------------
SOURCE_CONFIG_SPEC = """
A source config is JSON describing ONE text:

{
  "text_id": "isha-upanishad",
  "text_name": "Isha Upanishad",
  "language": "Sanskrit",
  "loader": "loaders/isha.py",      # a python file exposing load() -> list[dict]
  "fields": {                        # which raw keys hold what
    "devanagari": "text",
    "iast": "transliteration",       # optional - derived from Devanagari if absent
    "english": "translation",
    "chapter": "chapter",            # optional
    "verse": "verse"
  }
}

The loader file must define:  def load() -> list[dict]
It may fetch from any URL, read a local file, whatever - it just returns raw verses.
Keeping the loader separate means each text's quirks live in one small file, and the
pipeline core never changes.
"""


def load_verses(config: dict, config_dir: Path | None = None) -> list:
    """Import the text's loader module and call load()."""
    loader_path = Path(config["loader"])
    if not loader_path.is_absolute():
        roots = [config_dir, config_dir.parent] if config_dir else [Path.cwd()]
        candidates = [(root / loader_path).resolve() for root in roots]
        loader_path = next((path for path in candidates if path.exists()), candidates[0])
    if not loader_path.exists():
        raise FileNotFoundError(f"loader not found: {loader_path}")
    spec = importlib.util.spec_from_file_location("loader", loader_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not import loader: {loader_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "load"):
        raise AttributeError(f"{loader_path} must define load() -> list[dict]")
    rows = mod.load()
    if not isinstance(rows, list):
        raise TypeError(f"{loader_path}: load() must return a list")
    if not rows:
        raise ValueError(f"{loader_path}: load() returned no verses")
    if any(not isinstance(row, dict) for row in rows):
        raise TypeError(f"{loader_path}: every loaded verse must be a dict")
    return rows


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
def build(config: dict, config_dir: Path | None = None) -> tuple[list, list]:
    raw = load_verses(config, config_dir=config_dir)
    fm = config["fields"]
    tid = config["text_id"]
    tname = config["text_name"]
    out, gaps = [], []

    seen_identities = set()
    for i, rv in enumerate(raw):
        dev = clean_devanagari(source_text(rv.get(fm["devanagari"], "")))
        iast = source_text(rv.get(fm.get("iast", ""), "")).strip() or derive_iast(dev)
        english = source_text(rv.get(fm.get("english", ""), "")).strip()
        ch = rv.get(fm.get("chapter", ""), None)
        vn = rv.get(fm.get("verse", ""), i + 1)
        identity = (ch, vn)
        if identity in seen_identities:
            raise ValueError(f"duplicate chapter/verse identity {identity!r}")
        seen_identities.add(identity)

        row = {
            "verse_id": f"{tid}-{ch}-{vn}" if ch is not None else f"{tid}-{vn}",
            "text_id": tid, "text_name": tname,
            "chapter": ch, "verse": vn,
            "devanagari": dev, "iast": iast, "english": english,
            "scripts": to_scripts(dev),
        }

        # gap gate: collect every missing required field
        missing = []
        if not row["devanagari"]: missing.append("devanagari")
        if not row["iast"]:       missing.append("iast")
        if not row["english"]:    missing.append("english")
        for code, _ in TARGET_SCRIPTS:
            if not row["scripts"].get(code):
                missing.append(code)
        if missing:
            gaps.append((row["verse_id"], missing))
        out.append(row)

    if not gaps:
        validate_dataset(out, expected_text_id=tid)
    return out, gaps


def main():
    ap = argparse.ArgumentParser(description="DharmaSearch scripture ingestion pipeline")
    ap.add_argument("--config", required=True, help="path to a source config JSON")
    ap.add_argument("--out", required=True, help="output dataset path")
    ap.add_argument("--allow-gaps", action="store_true",
                    help="write output even if gaps exist (NOT recommended for release)")
    args = ap.parse_args()

    config_path = Path(args.config).resolve()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        verses, gaps = build(config, config_dir=config_path.parent)
    except (OSError, ValueError, TypeError, AttributeError, ImportError, KeyError) as error:
        sys.exit(f"BUILD FAILED: {error}")

    print(f"Text        : {config['text_name']} ({config['text_id']})")
    print(f"Verses built: {len(verses)}")
    print(f"Gaps        : {len(gaps)}")

    if gaps:
        print("\n--- GAP REPORT (first 25) ---")
        for vid, miss in gaps[:25]:
            print(f"  {vid:24} missing: {', '.join(miss)}")
        if not args.allow_gaps:
            sys.exit(
                f"\nBUILD FAILED: {len(gaps)} verse(s) incomplete. "
                "Fix the source/loader and re-run. "
                "(Use --allow-gaps only for debugging, never for release.)"
            )

    output_path = Path(args.out)
    write_text_atomic(output_path, json.dumps(verses, ensure_ascii=False))
    print(f"\nWrote {args.out}  ({output_path.stat().st_size // 1024} KB)")
    print("Zero gaps - safe to ship." if not gaps else "Written WITH gaps (debug).")


if __name__ == "__main__":
    main()


# ============================================================================
# WORKED EXAMPLE - the exact loader used to complete the Bhagavad Gita.
# Save as loaders/gita.py and point a config at it to reproduce the 701-verse build.
# ============================================================================
_GITA_LOADER_EXAMPLE = r'''
# loaders/gita.py
import requests

VERSE_URL = "https://raw.githubusercontent.com/gita/gita/main/data/verse.json"
TRANS_URL = "https://raw.githubusercontent.com/gita/gita/main/data/translation.json"

def load():
    verses = requests.get(VERSE_URL, timeout=30).json()
    trans  = requests.get(TRANS_URL, timeout=30).json()
    # pick one complete public-domain English translation
    english = {t["verse_id"]: t["description"]
               for t in trans
               if t["lang"] == "english" and t["authorName"] == "Swami Sivananda"}
    rows = []
    for v in verses:
        rows.append({
            "text": v["text"],                     # Devanagari (with inline tags, cleaned by pipeline)
            "transliteration": v["transliteration"],  # proper IAST with diacritics
            "translation": english.get(v["id"], ""),
            "chapter": v["chapter_number"],
            "verse": v["verse_number"],
        })
    return rows
'''

_GITA_CONFIG_EXAMPLE = r'''
{
  "text_id": "bhagavad-gita",
  "text_name": "Bhagavad Gita",
  "language": "Sanskrit",
  "loader": "loaders/gita.py",
  "fields": {
    "devanagari": "text",
    "iast": "transliteration",
    "english": "translation",
    "chapter": "chapter",
    "verse": "verse"
  }
}
'''

# ============================================================================
# SOURCING NOTES for the remaining 15 texts (where to point new loaders)
# ============================================================================
_SOURCING_NOTES = r"""
Clean, verifiable Devanagari sources to target from your own infra:

  sanskritdocuments.org   - Upanishads, all major stotras (Vishnu/Lalita Sahasranama,
                            Soundarya Lahari, Hanuman Chalisa), Narayaneeyam. Devanagari
                            + often IAST. The single best starting point.
  GRETIL (gretil.sub.uni-goettingen.de) - scholarly critical editions incl. the full
                            Ramayana and Mahabharata, verse by verse. This is where the
                            "every single verse" R&M ingestion sources from.
  Muktabodha digital library - tantric and Purana texts.
  bhagavata.org           - complete Srimad Bhagavatam, canto by canto.

Per-text plan:
  Tier 1 (single stotra/short text - one loader each, minutes to run):
    Hanuman Chalisa, Vishnu Sahasranama, Lalita Sahasranama, Soundarya Lahari,
    Narayaneeyam, principal Upanishads (Isha, Kena, Katha, Prashna, Mundaka,
    Mandukya, Aitareya, Taittiriya, Chandogya, Brihadaranyaka).
  Tier 2 (large but bounded):
    Devi Mahatmyam (~700), Yoga Sutras (~196), Vishnu/other Purana selections,
    Vivekachudamani (~580), Adhyatma Ramayanam.
  Tier 3 (every verse - months, but scripted):
    Ramayana (~24,000), Mahabharata (~100,000). Source from GRETIL critical edition.
    Run in chapter/parva batches; the gap gate guarantees each batch is whole.

For every text the recipe is identical:
  1. write loaders/<text>.py returning raw verses with a Devanagari field
  2. write a config pointing at it
  3. python3 ingest_pipeline.py --config <config> --out data/<text>.json
  4. build fails if ANY verse is incomplete -> fix source -> rerun -> zero gaps
"""
