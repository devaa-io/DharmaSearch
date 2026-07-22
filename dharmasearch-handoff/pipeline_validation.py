"""Shared structural validation for DharmaSearch datasets and app payloads."""

from __future__ import annotations

from collections import Counter
import re
from typing import Any


DATASET_FIELDS = ("devanagari", "iast", "english")
APP_FIELDS = ("dev", "iast", "en")
SCRIPT_CODES = ("ml", "ta", "te", "kn")
CONTAMINATION = re.compile(r"\.mw-parser-output|\{\s*font-size\s*:|<\/?(?:style|script)\b", re.I)


class ValidationError(ValueError):
    """Raised when a dataset or app payload violates a release invariant."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        shown = "\n  - ".join(errors[:25])
        suffix = f"\n  - ... and {len(errors) - 25} more" if len(errors) > 25 else ""
        super().__init__(f"validation failed ({len(errors)} error(s)):\n  - {shown}{suffix}")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_dataset(rows: Any, expected_text_id: str | None = None) -> None:
    """Validate a zero-gap pipeline dataset, raising ValidationError on failure."""
    errors: list[str] = []
    if not isinstance(rows, list):
        raise ValidationError(["dataset root must be a JSON array"])
    if not rows:
        raise ValidationError(["dataset must contain at least one verse"])

    verse_ids: list[str] = []
    identities: list[tuple[Any, Any]] = []
    for index, row in enumerate(rows, 1):
        label = f"row {index}"
        if not isinstance(row, dict):
            errors.append(f"{label}: expected an object")
            continue
        verse_id = row.get("verse_id")
        if not _nonempty(verse_id):
            errors.append(f"{label}: missing verse_id")
        else:
            verse_ids.append(verse_id)
            label = verse_id
        if expected_text_id and row.get("text_id") != expected_text_id:
            errors.append(f"{label}: text_id is {row.get('text_id')!r}, expected {expected_text_id!r}")
        if row.get("verse") is None:
            errors.append(f"{label}: missing verse number")
        identities.append((row.get("chapter"), row.get("verse")))
        for field in DATASET_FIELDS:
            if not _nonempty(row.get(field)):
                errors.append(f"{label}: missing {field}")
        if _nonempty(row.get("english")) and CONTAMINATION.search(row["english"]):
            errors.append(f"{label}: English contains HTML/CSS contamination")
        if _nonempty(row.get("english")) and len(row["english"]) > 5000:
            errors.append(f"{label}: English is implausibly long ({len(row['english'])} characters)")
        scripts = row.get("scripts")
        if not isinstance(scripts, dict):
            errors.append(f"{label}: scripts must be an object")
        else:
            for code in SCRIPT_CODES:
                if not _nonempty(scripts.get(code)):
                    errors.append(f"{label}: missing script {code}")

    for verse_id, count in Counter(verse_ids).items():
        if count > 1:
            errors.append(f"duplicate verse_id {verse_id!r} ({count} rows)")
    for identity, count in Counter(identities).items():
        if count > 1:
            errors.append(f"duplicate chapter/verse identity {identity!r} ({count} rows)")
    if errors:
        raise ValidationError(errors)


def validate_app_payload(payload: Any) -> None:
    """Validate text/verse counts and all release invariants in app_data.json."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        raise ValidationError(["app payload root must be a JSON object"])
    texts = payload.get("texts")
    verses = payload.get("verses")
    if not isinstance(texts, list):
        errors.append("payload.texts must be an array")
    if not isinstance(verses, list):
        errors.append("payload.verses must be an array")
    if errors:
        raise ValidationError(errors)

    text_ids = [text.get("id") for text in texts if isinstance(text, dict)]
    for text_id, count in Counter(text_ids).items():
        if not _nonempty(text_id):
            errors.append("text entry missing id")
        elif count > 1:
            errors.append(f"duplicate text id {text_id!r} ({count} entries)")
    known_text_ids = {text_id for text_id in text_ids if _nonempty(text_id)}

    verse_ids: list[str] = []
    counts: Counter[str] = Counter()
    for index, verse in enumerate(verses, 1):
        label = f"verse row {index}"
        if not isinstance(verse, dict):
            errors.append(f"{label}: expected an object")
            continue
        verse_id = verse.get("id")
        if not _nonempty(verse_id):
            errors.append(f"{label}: missing id")
        else:
            verse_ids.append(verse_id)
            label = verse_id
        tid = verse.get("tid")
        if tid not in known_text_ids:
            errors.append(f"{label}: unknown text id {tid!r}")
        else:
            counts[tid] += 1
        if verse.get("vn") is None:
            errors.append(f"{label}: missing verse number")

    for verse_id, count in Counter(verse_ids).items():
        if count > 1:
            errors.append(f"duplicate app verse id {verse_id!r} ({count} rows)")

    for text in texts:
        if not isinstance(text, dict):
            errors.append("text entry must be an object")
            continue
        tid = text.get("id")
        declared = text.get("tv")
        actual = counts[tid]
        if declared != actual:
            errors.append(f"{tid}: declares {declared!r} verses, found {actual}")
        if not text.get("complete"):
            continue
        for verse in (row for row in verses if isinstance(row, dict) and row.get("tid") == tid):
            label = verse.get("id", f"{tid} verse")
            if verse.get("complete") is not True:
                errors.append(f"{label}: belongs to a complete text but is not marked complete")
            for field in APP_FIELDS:
                if not _nonempty(verse.get(field)):
                    errors.append(f"{label}: missing {field}")
            if _nonempty(verse.get("en")) and CONTAMINATION.search(verse["en"]):
                errors.append(f"{label}: English contains HTML/CSS contamination")
            if _nonempty(verse.get("en")) and len(verse["en"]) > 5000:
                errors.append(f"{label}: English is implausibly long ({len(verse['en'])} characters)")
            scripts = verse.get("scripts")
            if not isinstance(scripts, dict):
                errors.append(f"{label}: scripts must be an object")
            else:
                for code in SCRIPT_CODES:
                    if not _nonempty(scripts.get(code)):
                        errors.append(f"{label}: missing script {code}")

    if errors:
        raise ValidationError(errors)
