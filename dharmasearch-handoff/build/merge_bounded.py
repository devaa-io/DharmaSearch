#!/usr/bin/env python3
"""Merge completed, chaptered works that do not belong to another text family."""

from __future__ import annotations

import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from pipeline_validation import SCRIPT_CODES, validate_app_payload, validate_dataset


SPECS = [
    {
        "tid": "yoga-sutras",
        "name": "Yoga Sutras of Patanjali",
        "prefix": "ys",
        "lang": "Sanskrit",
        "chapters": {
            1: "Samadhi Pada",
            2: "Sadhana Pada",
            3: "Vibhuti Pada",
            4: "Kaivalya Pada",
        },
        "count": 195,
        "desc": (
            "Patanjali's 195 sutras on yoga and liberation, arranged in four padas. "
            "Devanagari from sanskritdocuments.org; English interpretation by "
            "Charles Johnston (1912), via Project Gutenberg."
        ),
    },
]


def _app_rows(spec: dict, dataset: list[dict]) -> list[dict]:
    rows = []
    for source in dataset:
        chapter = source["chapter"]
        verse = source["verse"]
        if chapter not in spec["chapters"]:
            raise ValueError(f"{spec['tid']}: unexpected chapter {chapter}")
        rows.append({
            "id": f"{spec['prefix']}-{chapter}-{verse}",
            "tid": spec["tid"],
            "tn": spec["name"],
            "ch": chapter,
            "cn": spec["chapters"][chapter],
            "vn": verse,
            "complete": True,
            "roman": source["iast"],
            "dev": source["devanagari"],
            "iast": source["iast"],
            "en": source["english"],
            "kw": "",
            "scripts": {code: source["scripts"][code] for code in SCRIPT_CODES},
            "temple": "",
        })
    return rows


def merge(app: dict) -> dict:
    completed_ids = {spec["tid"] for spec in SPECS}
    original_positions = {
        text["id"]: index for index, text in enumerate(app["texts"])
        if text.get("id") in completed_ids
    }
    app["texts"] = [text for text in app["texts"] if text.get("id") not in completed_ids]
    app["verses"] = [row for row in app["verses"] if row.get("tid") not in completed_ids]

    for spec in SPECS:
        path = BASE / "data" / f"{spec['tid']}.json"
        dataset = json.loads(path.read_text(encoding="utf-8"))
        validate_dataset(dataset, expected_text_id=spec["tid"])
        if len(dataset) != spec["count"]:
            raise ValueError(
                f"{spec['tid']}: expected {spec['count']} rows, got {len(dataset)}"
            )
        text = {
            "id": spec["tid"],
            "name": spec["name"],
            "desc": spec["desc"],
            "lang": spec["lang"],
            "tv": spec["count"],
            "complete": True,
        }
        position = min(original_positions.get(spec["tid"], len(app["texts"])), len(app["texts"]))
        app["texts"].insert(position, text)
        app["chapterMeta"][spec["tid"]] = {
            str(number): {"dev": "", "tr": name, "mean": ""}
            for number, name in spec["chapters"].items()
        }
        app["verses"].extend(_app_rows(spec, dataset))

    validate_app_payload(app)
    return app
