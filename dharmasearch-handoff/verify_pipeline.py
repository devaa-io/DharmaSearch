#!/usr/bin/env python3
"""Verify committed datasets, app payload, and optionally all live sources."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from build_app import render_html, render_react_payload
from ingest_pipeline import build
from pipeline_validation import ValidationError, validate_app_payload, validate_dataset


BASE = Path(__file__).resolve().parent


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: {error}") from error


def verify(live: bool = False) -> tuple[int, int]:
    configs = sorted((BASE / "sources").glob("*_config.json"))
    if not configs:
        raise ValueError("no source configs found")

    app_path = BASE / "app_data.json"
    app = load_json(app_path)
    validate_app_payload(app)
    app_counts = {
        text["id"]: sum(verse.get("tid") == text["id"] for verse in app["verses"])
        for text in app["texts"]
    }
    app_rows = {}
    for verse in app["verses"]:
        key = (verse.get("tid"), verse.get("ch"), verse.get("vn"))
        if key in app_rows:
            raise ValueError(f"duplicate app text/chapter/verse identity {key!r}")
        app_rows[key] = verse

    dataset_rows = 0
    for config_path in configs:
        config = load_json(config_path)
        text_id = config["text_id"]
        dataset_path = BASE / "data" / f"{text_id}.json"
        dataset = load_json(dataset_path)
        validate_dataset(dataset, expected_text_id=text_id)
        dataset_rows += len(dataset)
        if app_counts.get(text_id) != len(dataset):
            raise ValueError(
                f"{text_id}: dataset has {len(dataset)} rows but app payload has {app_counts.get(text_id)!r}"
            )
        for row in dataset:
            chapter = row.get("chapter")
            key = (text_id, 1 if chapter is None else chapter, row["verse"])
            app_row = app_rows.get(key)
            if app_row is None:
                raise ValueError(f"{text_id}: dataset row {key[1:]} is missing from app payload")
            comparisons = {
                "dev": row["devanagari"],
                "iast": row["iast"],
                "en": row["english"],
            }
            comparisons.update({f"script {code}": row["scripts"][code] for code in ("ml", "ta", "te", "kn")})
            for field, expected in comparisons.items():
                actual = app_row["scripts"].get(field.removeprefix("script ")) if field.startswith("script ") else app_row.get(field)
                if actual != expected:
                    raise ValueError(f"{app_row['id']}: app {field} differs from committed dataset")
        if live:
            rebuilt, gaps = build(config, config_dir=config_path.parent)
            if gaps:
                raise ValueError(f"{text_id}: live rebuild contains {len(gaps)} gap(s)")
            if rebuilt != dataset:
                raise ValueError(f"{text_id}: live rebuild differs from {dataset_path.name}")
        print(f"OK  {text_id:22} {len(dataset):4} verses" + ("  live match" if live else ""))

    template = (BASE / "app_tpl.html").read_text(encoding="utf-8")
    raw_app = app_path.read_text(encoding="utf-8")
    expected_html = render_html(template, raw_app)
    actual_html = (BASE / "app.html").read_text(encoding="utf-8")
    if actual_html != expected_html:
        raise ValueError("app.html is stale; run python3 build_app.py")

    react_path = BASE.parent / "frontend" / "public" / "scripture-data.json"
    if not react_path.exists():
        raise ValueError("React scripture data is missing; run python3 build_app.py")
    if react_path.read_text(encoding="utf-8") != render_react_payload(app):
        raise ValueError("React scripture data is stale; run python3 build_app.py")
    return len(configs), dataset_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="refetch every upstream source and compare rebuilt rows with committed datasets",
    )
    args = parser.parse_args()
    try:
        datasets, rows = verify(live=args.live)
    except (ValidationError, ValueError, OSError, KeyError) as error:
        sys.exit(f"VERIFY FAILED: {error}")
    print(f"\nVerified {datasets} datasets / {rows} completed verses and generated app consistency.")


if __name__ == "__main__":
    main()
