#!/usr/bin/env python3
"""Merge the completed Narayaneeyam dataset into app_data.json.

Exposes merge(app) so build/merge_completed.py can run it as part of the
single documented full-rebuild path, and still works standalone.
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

TID = "narayaneeyam"
TN = "Narayaneeyam"
COUNT = 1033
CANTOS = 100
REQUIRED_SCRIPTS = ("ml", "ta", "te", "kn")

DESC = (
    "Melpathur Narayana Bhattatiri's 100-canto devotional condensation of the "
    "Bhagavata Purana, in praise of Krishna at Guruvayoor - 1033 verses. "
    "Devanagari from sanskritdocuments.org; English by P. R. Ramachander."
)


def load_dataset() -> list[dict]:
    rows = json.loads((BASE / "data" / f"{TID}.json").read_text(encoding="utf-8"))
    if len(rows) != COUNT:
        raise ValueError(f"{TID}: expected {COUNT} rows, got {len(rows)}")
    return rows


def app_verses(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        chapter, verse = row["chapter"], row["verse"]
        item = {
            "id": f"nym-{chapter}-{verse}", "tid": TID, "tn": TN,
            "ch": chapter, "cn": f"Dasakam {chapter}", "vn": verse, "complete": True,
            "roman": row["iast"], "dev": row["devanagari"], "iast": row["iast"],
            "en": row["english"], "kw": "",
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
    rows = app_verses(load_dataset())

    app["texts"] = [text for text in app["texts"] if text.get("id") != TID]
    insert_at = next(
        (i for i, text in enumerate(app["texts"]) if text.get("id") == "hanuman-chalisa"), -1
    ) + 1
    app["texts"].insert(insert_at, {
        "id": TID, "name": TN, "desc": DESC,
        "lang": "Sanskrit", "tv": COUNT, "complete": True,
    })

    app["chapterMeta"][TID] = {
        str(ch): {"dev": "", "tr": f"Dasakam {ch}", "mean": ""}
        for ch in range(1, CANTOS + 1)
    }

    app["verses"] = [verse for verse in app["verses"] if verse.get("tid") != TID]
    app["verses"].extend(rows)

    ids = [verse["id"] for verse in app["verses"]]
    if len(ids) != len(set(ids)):
        raise ValueError("app payload contains duplicate verse IDs")
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
    print(f"Merged Narayaneeyam into {app_path}")
    print(f"Texts: {len(merged['texts'])} | verses: {len(merged['verses'])}")


if __name__ == "__main__":
    main()
