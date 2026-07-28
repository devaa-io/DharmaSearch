#!/usr/bin/env python3
"""Upgrade MongoDB scripture data from the DharmaSearch content pipeline.

The backend seeds ``db.verses`` only when the collection is empty. This standalone
script provides an idempotent upgrade path from ``dharmasearch-handoff/app_data.json``.

Safety properties:

* The default run is a dry run. Nothing is written without ``--apply``.
* The default write is additive for existing documents. It adds verified script
  representations without changing ``text``, ``translation``, ``keywords``, or
  other fields rendered by the connected dashboard.
* New documents receive the pipeline's complete renderable representation via
  ``$setOnInsert``.
* Existing transliterations are preserved; pipeline scripts are set by dotted key.
* Replacing existing text and translations is opt-in via ``--replace-text``.
* Nothing is deleted. Mongo-only verse IDs are reported as orphans.

Usage:

    python3 seed_from_pipeline.py
    python3 seed_from_pipeline.py --apply
    python3 seed_from_pipeline.py --apply --replace-text
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from dotenv import load_dotenv
    from pymongo import MongoClient, UpdateOne
except ImportError:
    sys.exit("Missing dependencies. Run from the backend venv: pip install -r requirements.txt")


BACKEND_DIR = Path(__file__).resolve().parent
REPO_ROOT = BACKEND_DIR.parent
APP_DATA = REPO_ROOT / "dharmasearch-handoff" / "app_data.json"

# app_data.json verse key -> Mongo verse document key
CORE_MAP = {
    "id": "verse_id",
    "tid": "text_id",
    "tn": "text_name",
    "ch": "chapter",
    "cn": "chapter_name",
    "vn": "verse_number",
}
SCRIPT_CODES = ("ml", "ta", "te", "kn")


def load_payload(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"Pipeline payload not found: {path}\nRun build_app.py in dharmasearch-handoff first.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        sys.exit(f"{path} is not valid JSON: {error}")
    for key in ("texts", "verses"):
        if not isinstance(payload.get(key), list):
            sys.exit(f"{path} missing required list '{key}'")
    return payload


def validate_unique_ids(items: list[dict], key: str, label: str) -> None:
    values = [item.get(key) for item in items]
    missing = sum(value is None or value == "" for value in values)
    duplicates = sorted(value for value, count in Counter(values).items() if value and count > 1)
    if missing or duplicates:
        details = []
        if missing:
            details.append(f"{missing} missing {key}")
        if duplicates:
            details.append(f"duplicate {key}: {', '.join(duplicates[:10])}")
        sys.exit(f"Invalid pipeline {label}: {'; '.join(details)}")


def additive_verse_update(row: dict) -> dict:
    """Fields safe to add to an existing verse without changing current rendering."""
    update = {"verified": bool(row.get("complete"))}
    if row.get("dev"):
        update["devanagari"] = row["dev"]
    if row.get("iast"):
        update["iast"] = row["iast"]

    # Dotted updates preserve existing keys such as the Emergent-era ``hi`` value.
    scripts = row.get("scripts") or {}
    for code in SCRIPT_CODES:
        if scripts.get(code):
            update[f"transliterations.{code}"] = scripts[code]
    return update


def insert_only_verse_fields(row: dict) -> dict:
    """Complete dashboard-compatible document used only when an upsert inserts."""
    fields = {}
    for source, destination in CORE_MAP.items():
        if row.get(source) is not None:
            fields[destination] = row[source]

    if row.get("roman"):
        fields["text"] = row["roman"]
    if row.get("en"):
        fields["translation"] = row["en"]
    if row.get("kw"):
        fields["keywords"] = row["kw"]
    return fields


def replacement_fields(row: dict) -> dict:
    """Explicitly opted-in replacements for existing dashboard-facing fields."""
    update = {}
    if row.get("roman"):
        update["text"] = row["roman"]
    if row.get("en"):
        update["translation"] = row["en"]
    if row.get("kw"):
        update["keywords"] = row["kw"]
    return update


def insert_only_text_fields(text: dict, chapter_count: int, verse_count: int) -> dict:
    """Complete scripture metadata used only when an upsert inserts."""
    fields = {
        "text_id": text["id"],
        "total_verses": verse_count,
    }
    if text.get("name"):
        fields["name"] = text["name"]
    if text.get("desc"):
        fields["description"] = text["desc"]
    if text.get("lang"):
        fields["language"] = text["lang"]
    if chapter_count:
        fields["total_chapters"] = chapter_count
    return fields


def verse_operation(row: dict, replace_text: bool) -> UpdateOne:
    set_fields = additive_verse_update(row)
    insert_fields = insert_only_verse_fields(row)
    if replace_text:
        replacements = replacement_fields(row)
        set_fields.update(replacements)
        for field in replacements:
            insert_fields.pop(field, None)
    return UpdateOne(
        {"verse_id": row["id"]},
        {
            "$set": set_fields,
            "$setOnInsert": insert_fields,
        },
        upsert=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write to MongoDB (default is a dry run)")
    parser.add_argument(
        "--replace-text",
        action="store_true",
        help="also overwrite existing text/translation/keywords with pipeline values",
    )
    parser.add_argument("--data", default=str(APP_DATA), help="path to app_data.json")
    args = parser.parse_args()

    load_dotenv(BACKEND_DIR / ".env")
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME")
    if not mongo_url or not db_name:
        sys.exit("MONGO_URL and DB_NAME must be set (see backend/.env)")

    payload = load_payload(Path(args.data))
    rows = [row for row in payload["verses"] if row.get("id")]
    texts = [text for text in payload["texts"] if text.get("id")]
    validate_unique_ids(rows, "id", "verses")
    validate_unique_ids(texts, "id", "texts")

    client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
    try:
        client.admin.command("ping")
    except Exception as error:  # noqa: BLE001 - surface any connection failure plainly
        client.close()
        sys.exit(f"Cannot reach MongoDB: {error}")
    db = client[db_name]

    try:
        existing = {
            doc["verse_id"]
            for doc in db.verses.find({"verse_id": {"$exists": True}}, {"verse_id": 1, "_id": 0})
        }
        pipeline_ids = {row["id"] for row in rows}

        to_insert = sorted(pipeline_ids - existing)
        to_update = sorted(pipeline_ids & existing)
        orphans = sorted(existing - pipeline_ids)

        verified = sum(1 for row in rows if row.get("complete"))
        with_dev = sum(1 for row in rows if row.get("dev"))

        print(f"database        : {db_name}")
        print(f"pipeline payload: {args.data}")
        print(f"pipeline verses : {len(rows)} ({verified} verified, {with_dev} with Devanagari)")
        print(f"already in mongo: {len(existing)}")
        print()
        print(f"  will update   : {len(to_update)}")
        print(f"  will insert   : {len(to_insert)}")
        print(f"  orphans       : {len(orphans)}  (in Mongo, absent from pipeline - NOT deleted)")
        if orphans:
            preview = ", ".join(orphans[:10])
            print(f"                  e.g. {preview}{' ...' if len(orphans) > 10 else ''}")
        print()
        print("mode            : " + ("APPLY" if args.apply else "DRY RUN (no writes)"))
        print("existing text   : " + ("REPLACED from pipeline" if args.replace_text else "left untouched"))

        if not args.apply:
            print("\nNothing written. Re-run with --apply to perform the upgrade.")
            return

        operations = [verse_operation(row, args.replace_text) for row in rows]
        result = db.verses.bulk_write(operations, ordered=False)
        print(
            f"\nverses: matched={result.matched_count} "
            f"modified={result.modified_count} upserted={len(result.upserted_ids)}"
        )

        chapters: dict[str, set] = defaultdict(set)
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[row["tid"]] += 1
            if row.get("ch") is not None:
                chapters[row["tid"]].add(row["ch"])

        text_ops = [
            UpdateOne(
                {"text_id": text["id"]},
                {
                    "$set": {"verified": bool(text.get("complete"))},
                    "$setOnInsert": insert_only_text_fields(
                        text,
                        len(chapters.get(text["id"], ())),
                        counts.get(text["id"], 0),
                    ),
                },
                upsert=True,
            )
            for text in texts
        ]
        text_result = db.scriptures.bulk_write(text_ops, ordered=False)
        print(
            f"texts : matched={text_result.matched_count} "
            f"modified={text_result.modified_count} upserted={len(text_result.upserted_ids)}"
        )

        sample = db.verses.find_one({"verse_id": "bg-1-1"}, {"_id": 0})
        if sample:
            print("\nspot check bg-1-1:")
            print(f"  devanagari      : {(sample.get('devanagari') or '(none)')[:52]}")
            print(f"  transliterations: {sorted((sample.get('transliterations') or {}).keys())}")
            print(f"  verified        : {sample.get('verified')}")

        print("\nDone. Existing bookmarks/annotations/plan progress are unaffected (verse_id unchanged).")
    finally:
        client.close()


if __name__ == "__main__":
    main()
