#!/usr/bin/env python3
"""Merge completed single-chapter stotra datasets into app_data.json.

Same shape as merge_upanishads.py - kept as a separate script because these
texts aren't Upanishads and don't belong in that module's naming.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from pipeline_io import write_text_atomic
from pipeline_validation import validate_app_payload


REQUIRED_SCRIPTS = ("ml", "ta", "te", "kn")

SPECS = [
    {
        "tid": "vishnu-sahasranama",
        "name": "Vishnu Sahasranama",
        "count": 108,
        "prefix": "vs",
        "section_name": "Names of Vishnu",
        "desc": (
            "The thousand names of Lord Vishnu in 108 slokas, from the Anushasana "
            "Parva of the Mahabharata. Daily recitation is a cornerstone of worship "
            "in Kerala Vishnu temples like Padmanabhaswamy and Guruvayur. Devanagari, "
            "IAST and English by Swami Krishnananda (The Divine Life Society)."
        ),
    },
    {
        "tid": "soundarya-lahari",
        "name": "Soundarya Lahari",
        "count": 100,
        "prefix": "sl",
        "section_name": "Ananda Lahari",
        "desc": (
            "100 verses attributed to Adi Shankaracharya in praise of the Divine "
            "Mother (verses 1-41 Anandalahari, 42-100 Saundaryalahari proper). "
            "Devanagari from sanskritdocuments.org; English by P. R. Ramachander."
        ),
    },
    {
        "tid": "lalita-sahasranama",
        "name": "Lalita Sahasranama",
        "count": 1000,
        "prefix": "ls",
        "section_name": "Names of Lalita",
        "desc": (
            "The 1000 names of Lalita Tripurasundari, from the Brahmanda Purana "
            "(Hayagriva-Agastya dialogue). Devanagari from sanskritdocuments.org; "
            "English by P. R. Ramachander."
        ),
    },
]


def load_dataset(spec: dict) -> list[dict]:
    path = BASE / "data" / f"{spec['tid']}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    if len(rows) != spec["count"]:
        raise ValueError(f"{spec['tid']}: expected {spec['count']} rows, got {len(rows)}")
    return rows


def app_verses(spec: dict, rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        verse = row["verse"]
        item = {
            "id": f"{spec['prefix']}-{verse}",
            "tid": spec["tid"],
            "tn": spec["name"],
            "ch": 1,
            "cn": spec["section_name"],
            "vn": verse,
            "complete": True,
            "roman": row["iast"],
            "dev": row["devanagari"],
            "iast": row["iast"],
            "en": row["english"],
            "kw": "",
            "scripts": {code: row["scripts"][code] for code in REQUIRED_SCRIPTS},
            "temple": "",
        }
        missing = [field for field in ("dev", "iast", "en") if not item[field]]
        missing.extend(code for code in REQUIRED_SCRIPTS if not item["scripts"][code])
        if missing:
            raise ValueError(f"{item['id']}: missing {', '.join(missing)}")
        out.append(item)
    return out


def merge(app: dict) -> dict:
    completed_ids = {spec["tid"] for spec in SPECS}

    app["texts"] = [text for text in app["texts"] if text.get("id") not in completed_ids]
    insert_at = next(i for i, text in enumerate(app["texts"]) if text.get("id") == "bhagavad-gita") + 1
    new_texts = [
        {
            "id": spec["tid"], "name": spec["name"], "desc": spec["desc"],
            "lang": "Sanskrit", "tv": spec["count"], "complete": True,
        }
        for spec in SPECS
    ]
    app["texts"][insert_at:insert_at] = new_texts

    app["verses"] = [
        verse for verse in app["verses"] if verse.get("tid") not in completed_ids
    ]
    for spec in SPECS:
        app["chapterMeta"][spec["tid"]] = {
            "1": {"dev": "", "tr": spec["section_name"], "mean": ""}
        }
        app["verses"].extend(app_verses(spec, load_dataset(spec)))

    ids = [verse["id"] for verse in app["verses"]]
    if len(ids) != len(set(ids)):
        raise ValueError("app payload contains duplicate verse IDs")
    for text in app["texts"]:
        actual = sum(verse.get("tid") == text["id"] for verse in app["verses"])
        if actual != text["tv"]:
            raise ValueError(f"{text['id']}: metadata says {text['tv']} verses, found {actual}")
    validate_app_payload(app)
    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=BASE / "app_data.json")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    app_path = args.app.resolve()
    app = json.loads(app_path.read_text(encoding="utf-8"))
    merged = merge(app)
    if not args.no_backup:
        shutil.copy2(app_path, app_path.with_suffix(app_path.suffix + ".bak"))
    write_text_atomic(app_path, json.dumps(merged, ensure_ascii=False))
    print(f"Merged {len(SPECS)} completed stotras into {app_path}")
    print(f"Texts: {len(merged['texts'])} | verses: {len(merged['verses'])}")


if __name__ == "__main__":
    main()
