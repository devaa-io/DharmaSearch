#!/usr/bin/env python3
"""Rebuild every completed app text from its canonical pipeline dataset."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE / "build"))

from merge_upanishads import merge as merge_upanishads
from pipeline_io import write_text_atomic
from pipeline_validation import SCRIPT_CODES, validate_app_payload, validate_dataset


def sync_canonical_datasets(app: dict) -> dict:
    """Copy canonical text fields into existing completed app rows."""
    complete_ids = {text["id"] for text in app["texts"] if text.get("complete")}
    app_rows = {
        (row.get("tid"), row.get("ch"), row.get("vn")): row
        for row in app["verses"]
        if row.get("tid") in complete_ids
    }
    for text_id in sorted(complete_ids):
        dataset_path = BASE / "data" / f"{text_id}.json"
        if not dataset_path.exists():
            raise ValueError(f"{text_id}: missing canonical dataset {dataset_path}")
        dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
        validate_dataset(dataset, expected_text_id=text_id)
        for source in dataset:
            chapter = source.get("chapter")
            key = (text_id, 1 if chapter is None else chapter, source["verse"])
            target = app_rows.get(key)
            if target is None:
                raise ValueError(f"{text_id}: app payload is missing chapter/verse {key[1:]}")
            target["dev"] = source["devanagari"]
            target["iast"] = source["iast"]
            target["roman"] = source["iast"]
            target["en"] = source["english"]
            target["scripts"] = {code: source["scripts"][code] for code in SCRIPT_CODES}
    validate_app_payload(app)
    return app


def merge(app: dict) -> dict:
    return sync_canonical_datasets(merge_upanishads(app))


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
    completed = sum(bool(text.get("complete")) for text in merged["texts"])
    print(f"Merged {completed} completed texts into {app_path}")
    print(f"Texts: {len(merged['texts'])} | verses: {len(merged['verses'])}")


if __name__ == "__main__":
    main()
