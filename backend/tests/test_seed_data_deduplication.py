"""Regression tests for canonical Upanishad seed-data deduplication."""
import json
import sys
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

from scripture_data import get_all_verses  # noqa: E402


LEGACY_DUPLICATE_IDS = {
    "isha-1", "isha-2", "isha-4", "isha-5", "isha-6", "isha-7",
    "kena-1", "kena-2", "kena-3",
    "katha-1", "katha-2", "katha-3", "katha-4", "katha-5", "katha-6",
    "mundaka-1", "mundaka-2", "mundaka-3", "mundaka-4", "mandukya-1",
}
LEGACY_UPANISHAD_CHAPTERS = {
    "Chandogya Upanishad", "Brihadaranyaka Upanishad", "Taittiriya Upanishad",
}
CANONICAL_ISHA_IDS = {f"isha-up-{verse_number}" for verse_number in range(1, 19)}


class TestSeedDataDeduplication(unittest.TestCase):
    def test_legacy_semantic_duplicates_are_absent_from_seed_data(self):
        verse_ids = {verse["verse_id"] for verse in get_all_verses()}

        self.assertTrue(LEGACY_DUPLICATE_IDS.isdisjoint(verse_ids))

    def test_non_duplicate_legacy_upanishad_rows_are_retained(self):
        legacy_rows = [
            verse for verse in get_all_verses()
            if verse["text_id"] == "upanishads"
            and verse["chapter_name"] in LEGACY_UPANISHAD_CHAPTERS
        ]

        self.assertEqual(len(legacy_rows), 13)

    def test_seed_verse_ids_are_unique(self):
        verse_ids = [verse["verse_id"] for verse in get_all_verses()]

        self.assertEqual(len(verse_ids), len(set(verse_ids)))

    def test_pipeline_app_data_contains_complete_canonical_isha_without_legacy_ids(self):
        app_data_path = PROJECT_ROOT / "dharmasearch-handoff" / "app_data.json"
        app_data = json.loads(app_data_path.read_text())
        verses = app_data["verses"]
        verse_ids = {verse["id"] for verse in verses}
        canonical_isha = [
            verse for verse in verses if verse.get("tid") == "isha-upanishad"
        ]
        canonical_isha_ids = {verse["id"] for verse in canonical_isha}

        self.assertEqual(len(canonical_isha), 18)
        self.assertEqual(canonical_isha_ids, CANONICAL_ISHA_IDS)
        self.assertEqual(len(canonical_isha_ids), len(canonical_isha))
        self.assertTrue(all(verse.get("complete") is True for verse in canonical_isha))
        self.assertTrue(LEGACY_DUPLICATE_IDS.isdisjoint(verse_ids))
