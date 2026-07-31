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


CANTOS_PATH = BASE / "data" / f"{TID}-cantos.json"


def chapter_meta() -> dict:
    """Real canto titles for the chapter picker, from the stored copy.

    Kept as a committed file rather than fetched here so that merging stays
    offline and reproducible; refresh it with --refresh-cantos when the
    source changes.
    """
    if not CANTOS_PATH.exists():
        raise FileNotFoundError(
            f"{CANTOS_PATH} is missing. Regenerate it with:\n"
            f"    python3 build/merge_narayaneeyam.py --refresh-cantos"
        )
    titles = json.loads(CANTOS_PATH.read_text(encoding="utf-8"))
    missing = [ch for ch in range(1, CANTOS + 1) if str(ch) not in titles]
    if missing:
        raise ValueError(f"{TID}: canto titles missing for {missing}")
    return {
        str(ch): {
            "dev": titles[str(ch)]["dev"],
            "tr": f"Dasakam {ch}",
            "mean": titles[str(ch)]["en"],
        }
        for ch in range(1, CANTOS + 1)
    }


def refresh_cantos() -> None:
    """Re-fetch the canto titles from the source and store them."""
    sys.path.insert(0, str(BASE / "loaders"))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "narayaneeyam_loader", BASE / "loaders" / "narayaneeyam.py"
    )
    loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loader)
    titles = {str(number): value for number, value in sorted(loader.canto_titles().items())}
    write_text_atomic(CANTOS_PATH, json.dumps(titles, ensure_ascii=False, indent=1))
    print(f"Wrote {CANTOS_PATH} ({len(titles)} cantos)")


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

    app["chapterMeta"][TID] = chapter_meta()

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
    parser.add_argument(
        "--refresh-cantos", action="store_true",
        help="re-fetch canto titles from the source, then exit",
    )
    args = parser.parse_args()

    if args.refresh_cantos:
        refresh_cantos()
        return

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
