#!/usr/bin/env python3
"""Merge all completed Upanishad datasets into app_data.json.

The operation is idempotent. It also removes low-fidelity rows for these same
texts from the legacy ``upanishads`` preview group so Explore/search does not
show duplicate passages.
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
        "tid": "isha-upanishad",
        "name": "Isha Upanishad",
        "count": 18,
        "prefix": "isha-up",
        "sections": {1: "Īśāvāsya Upaniṣad"},
        "chapter_meta": {
            "1": {
                "dev": "ईशावास्योपनिषद्",
                "tr": "Īśāvāsya Upaniṣad",
                "mean": "The Upanishad of the Lord's Indwelling",
            }
        },
        "desc": (
            "One of the shortest yet most profound principal Upanishads (18 mantras), "
            "from the Shukla Yajurveda. It teaches seeing the divine in all things and "
            "acting without attachment. English by Max Muller (SBE Vol. 1, 1879, "
            "public domain)."
        ),
    },
    {
        "tid": "mandukya-upanishad",
        "name": "Mandukya Upanishad",
        "count": 12,
        "prefix": "mandukya-up",
        "sections": {1: "Mandukya Upanishad"},
        "desc": (
            "12 verses, Atharva Veda - the shortest principal Upanishad. Analyses the "
            "syllable Om into its matras (a/u/m/silence), mapped onto the four states "
            "of consciousness: waking, dream, deep sleep, and the fourth (turiya) "
            "beyond them. English by Robert Ernest Hume (Thirteen Principal Upanishads, "
            "Oxford University Press, 1921, public domain)."
        ),
    },
    {
        "tid": "kena-upanishad",
        "name": "Kena Upanishad",
        "count": 35,
        "prefix": "kena-up",
        "sections": {1: "Prathama Khanda", 2: "Dvitiya Khanda", 3: "Tritiya Khanda", 4: "Chaturtha Khanda"},
        "desc": (
            "35 mantras in 4 khandas, from the Sama Veda. Poses the question 'by whose "
            "will does the mind think?' and points beyond sense and intellect to Brahman "
            "as the ungraspable ground of knowing itself. English by Max Muller "
            "(SBE Vol. 1, 1879, public domain)."
        ),
    },
    {
        "tid": "katha-upanishad",
        "name": "Katha Upanishad",
        "count": 120,
        "prefix": "katha-up",
        "sections": {
            1: "Adhyaya I, Valli 1", 2: "Adhyaya I, Valli 2", 3: "Adhyaya I, Valli 3",
            4: "Adhyaya II, Valli 1", 5: "Adhyaya II, Valli 2", 6: "Adhyaya II, Valli 3",
        },
        "desc": (
            "120 verses in 6 vallis (2 adhyayas), Krishna Yajurveda. The boy Naciketas "
            "questions Death itself and receives the teaching on the immortal Self beyond "
            "the body. English by Max Muller (SBE Vol. 15, 1884, public domain)."
        ),
    },
    {
        "tid": "mundaka-upanishad",
        "name": "Mundaka Upanishad",
        "count": 64,
        "prefix": "mundaka-up",
        "sections": {
            1: "Mundaka I, Khanda 1", 2: "Mundaka I, Khanda 2",
            3: "Mundaka II, Khanda 1", 4: "Mundaka II, Khanda 2",
            5: "Mundaka III, Khanda 1", 6: "Mundaka III, Khanda 2",
        },
        "desc": (
            "64 verses in 3 mundakas of 2 khandas each, Atharva Veda. Distinguishes lower "
            "knowledge (the sciences and scriptures) from the higher knowledge of the "
            "imperishable Brahman, in the famous image of two birds on one tree. English "
            "by Max Muller (SBE Vol. 15, 1884, public domain)."
        ),
    },
    {
        "tid": "prashna-upanishad",
        "name": "Prashna Upanishad",
        "count": 67,
        "prefix": "prashna-up",
        "sections": {n: f"Prashna {n}" for n in range(1, 7)},
        "desc": (
            "67 verses in 6 prashnas (questions), Atharva Veda. Six seekers each put one "
            "question to the sage Pippalada, on the origin of beings, prana, sleep and "
            "dream, meditation on Om, and the sixteen parts of the person. English by "
            "Max Muller (SBE Vol. 15, 1884, public domain)."
        ),
    },
]


def chapter_meta(spec: dict) -> dict:
    if "chapter_meta" in spec:
        return spec["chapter_meta"]
    return {
        str(chapter): {"dev": "", "tr": name, "mean": ""}
        for chapter, name in spec["sections"].items()
    }


def load_dataset(spec: dict) -> list[dict]:
    path = BASE / "data" / f"{spec['tid']}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    if len(rows) != spec["count"]:
        raise ValueError(f"{spec['tid']}: expected {spec['count']} rows, got {len(rows)}")
    return rows


def app_verses(spec: dict, rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        chapter = row.get("chapter")
        chapter = 1 if chapter is None else chapter
        verse = row["verse"]
        if chapter not in spec["sections"]:
            raise ValueError(f"{spec['tid']}: unexpected chapter {chapter}")
        item = {
            "id": f"{spec['prefix']}-{chapter}-{verse}" if len(spec["sections"]) > 1 else f"{spec['prefix']}-{verse}",
            "tid": spec["tid"],
            "tn": spec["name"],
            "ch": chapter,
            "cn": spec["sections"][chapter],
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
    completed_names = {spec["name"] for spec in SPECS}

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
        verse for verse in app["verses"]
        if verse.get("tid") not in completed_ids
        and not (verse.get("tid") == "upanishads" and verse.get("cn") in completed_names)
    ]
    for spec in SPECS:
        app["chapterMeta"][spec["tid"]] = chapter_meta(spec)
        app["verses"].extend(app_verses(spec, load_dataset(spec)))

    for text in app["texts"]:
        if text.get("id") == "upanishads":
            text["tv"] = sum(verse.get("tid") == "upanishads" for verse in app["verses"])

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
    print(f"Merged {len(SPECS)} completed Upanishads into {app_path}")
    print(f"Texts: {len(merged['texts'])} | verses: {len(merged['verses'])}")


if __name__ == "__main__":
    main()
