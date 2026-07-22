from __future__ import annotations

import os
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build_app
import ingest_pipeline
from ingest_pipeline import clean_devanagari, load_verses
from loaders._wikisource import rendered_text
from pipeline_io import write_text_atomic
from pipeline_validation import ValidationError, validate_app_payload, validate_dataset
import verify_pipeline


def complete_dataset_row(**overrides):
    row = {
        "verse_id": "sample-1-1",
        "text_id": "sample",
        "text_name": "Sample",
        "chapter": 1,
        "verse": 1,
        "devanagari": "धर्मः",
        "iast": "dharmaḥ",
        "english": "Dharma.",
        "scripts": {"ml": "ധർമഃ", "ta": "த⁴ர்மஃ", "te": "ధర్మః", "kn": "ಧರ್ಮಃ"},
    }
    row.update(overrides)
    return row


class DatasetValidationTests(unittest.TestCase):
    def test_wikisource_parser_preserves_inline_words(self):
        markup = "<p>Na<span>k</span>iketa and Ri<span>sh</span>i</p><p>Next line</p><style>.bad{}</style>"
        self.assertEqual(rendered_text(markup), "Nakiketa and Rishi\nNext line")

    def test_complete_dataset_passes(self):
        validate_dataset([complete_dataset_row()], expected_text_id="sample")

    def test_duplicate_identity_fails(self):
        second = complete_dataset_row(verse_id="sample-copy")
        with self.assertRaisesRegex(ValidationError, "duplicate chapter/verse identity"):
            validate_dataset([complete_dataset_row(), second], expected_text_id="sample")

    def test_missing_script_fails(self):
        row = complete_dataset_row()
        row["scripts"]["ta"] = ""
        with self.assertRaisesRegex(ValidationError, "missing script ta"):
            validate_dataset([row], expected_text_id="sample")

    def test_wikisource_css_contamination_fails(self):
        row = complete_dataset_row(english="Translation. .mw-parser-output .references{font-size:83%}")
        with self.assertRaisesRegex(ValidationError, "HTML/CSS contamination"):
            validate_dataset([row], expected_text_id="sample")

    def test_implausibly_long_translation_fails(self):
        row = complete_dataset_row(english="commentary " * 600)
        with self.assertRaisesRegex(ValidationError, "implausibly long"):
            validate_dataset([row], expected_text_id="sample")

    def test_devanagari_cleaning_removes_inline_number(self):
        self.assertEqual(clean_devanagari("धर्मक्षेत्रे ॥1.1॥\n\nकुरुक्षेत्रे"), "धर्मक्षेत्रे \nकुरुक्षेत्रे")

    def test_null_source_text_is_a_gap_not_literal_none(self):
        config = {
            "text_id": "sample",
            "text_name": "Sample",
            "fields": {"devanagari": "dev", "iast": "iast", "english": "en", "verse": "verse"},
        }
        raw = {"dev": None, "iast": None, "en": None, "verse": 1}
        with mock.patch.object(ingest_pipeline, "load_verses", return_value=[raw]):
            rows, gaps = ingest_pipeline.build(config)
        self.assertTrue(gaps)
        self.assertEqual(rows[0]["devanagari"], "")
        self.assertEqual(rows[0]["iast"], "")
        self.assertEqual(rows[0]["english"], "")
        self.assertNotIn("None", json.dumps(rows))

    def test_string_source_text_is_unchanged(self):
        config = {
            "text_id": "sample",
            "text_name": "Sample",
            "fields": {"devanagari": "dev", "iast": "iast", "english": "en", "verse": "verse"},
        }
        raw = {"dev": "धर्मः", "iast": "dharmaḥ", "en": "Dharma.", "verse": 1}
        with mock.patch.object(ingest_pipeline, "load_verses", return_value=[raw]):
            rows, gaps = ingest_pipeline.build(config)
        self.assertEqual(gaps, [])
        self.assertEqual(rows[0]["devanagari"], raw["dev"])
        self.assertEqual(rows[0]["iast"], raw["iast"])
        self.assertEqual(rows[0]["english"], raw["en"])


class AppValidationTests(unittest.TestCase):
    def test_complete_text_requires_every_representation(self):
        payload = {
            "texts": [{"id": "sample", "tv": 1, "complete": True}],
            "verses": [{
                "id": "sample-1", "tid": "sample", "vn": 1, "complete": True,
                "dev": "धर्मः", "iast": "dharmaḥ", "en": "Dharma.",
                "scripts": {"ml": "ധർമഃ", "ta": "", "te": "ధర్మః", "kn": "ಧರ್ಮಃ"},
            }],
        }
        with self.assertRaisesRegex(ValidationError, "missing script ta"):
            validate_app_payload(payload)

    def test_render_requires_one_placeholder_and_escapes_script_end(self):
        rendered = build_app.render_html("<script>const DB=__DATA__;</script>", '{"en":"</script>"}')
        self.assertIn(r"\u003c/script>", rendered)
        self.assertNotIn('{"en":"</script>"}', rendered)
        with self.assertRaisesRegex(ValueError, "exactly one"):
            build_app.render_html("__DATA__ __DATA__", "{}")

    def test_react_payload_is_compact_and_unicode_safe(self):
        self.assertEqual(build_app.render_react_payload({"dev": "धर्मः"}), '{"dev":"धर्मः"}\n')


class AtomicWriteTests(unittest.TestCase):
    def test_preserves_existing_destination_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "generated.json"
            destination.write_text("old", encoding="utf-8")
            destination.chmod(0o640)
            write_text_atomic(destination, "new")
            self.assertEqual(destination.read_text(encoding="utf-8"), "new")
            self.assertEqual(destination.stat().st_mode & 0o7777, 0o640)

    def test_new_destination_uses_portable_default_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "generated.json"
            write_text_atomic(destination, "new")
            self.assertEqual(destination.stat().st_mode & 0o7777, 0o644)


class BuildAppPathTests(unittest.TestCase):
    def test_default_react_data_target_is_repository_relative_from_another_cwd(self):
        payload = {
            "texts": [{"id": "sample", "tv": 1, "complete": True}],
            "verses": [{
                "id": "sample-0-1", "tid": "sample", "ch": 0, "vn": 1, "complete": True,
                "dev": "धर्मः", "iast": "dharmaḥ", "en": "Dharma.",
                "scripts": {"ml": "ധർമഃ", "ta": "த⁴ர்மஃ", "te": "ధర్మః", "kn": "ಧರ್ಮಃ"},
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            template = work / "template.html"
            data = work / "payload.json"
            output = work / "app.html"
            template.write_text("<script>const DB=__DATA__;</script>", encoding="utf-8")
            data.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            output.write_text("old", encoding="utf-8")
            writes = []

            def record_write(path, content):
                writes.append((path, content))
                if path == output:
                    path.write_text(content, encoding="utf-8")

            previous = Path.cwd()
            try:
                os.chdir("/")
                with mock.patch.object(sys, "argv", [
                    "build_app.py", "--template", str(template), "--data", str(data), "--out", str(output),
                ]), mock.patch.object(build_app, "write_text_atomic", side_effect=record_write):
                    build_app.main()
            finally:
                os.chdir(previous)

        self.assertEqual(writes[1][0], build_app.DEFAULT_REACT_DATA)

    def test_explicit_react_data_target_is_preserved(self):
        payload = {"texts": [], "verses": []}
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            template = work / "template.html"
            data = work / "payload.json"
            output = work / "app.html"
            explicit_react_data = work / "custom" / "scripture.json"
            template.write_text("<script>const DB=__DATA__;</script>", encoding="utf-8")
            data.write_text(json.dumps(payload), encoding="utf-8")
            output.write_text("old", encoding="utf-8")
            writes = []

            def record_write(path, content):
                writes.append((path, content))
                if path == output:
                    path.write_text(content, encoding="utf-8")

            with mock.patch.object(sys, "argv", [
                "build_app.py", "--template", str(template), "--data", str(data), "--out", str(output),
                "--react-data", str(explicit_react_data),
            ]), mock.patch.object(build_app, "write_text_atomic", side_effect=record_write):
                build_app.main()

        self.assertEqual(writes[1][0], explicit_react_data)


class VerifyPipelineRegressionTests(unittest.TestCase):
    def _verify_chapter_mapping(self, row, app_chapter):
        payload = {
            "texts": [{"id": "sample", "tv": 1, "complete": True}],
            "verses": [{
                "id": f"sample-{app_chapter}-1", "tid": "sample", "ch": app_chapter,
                "vn": 1, "complete": True, "dev": row["devanagari"], "iast": row["iast"],
                "en": row["english"], "scripts": row["scripts"],
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "handoff"
            (base / "sources").mkdir(parents=True)
            (base / "data").mkdir()
            (base / "sources" / "sample_config.json").write_text('{"text_id":"sample"}', encoding="utf-8")
            (base / "data" / "sample.json").write_text(json.dumps([row], ensure_ascii=False), encoding="utf-8")
            raw_payload = json.dumps(payload, ensure_ascii=False)
            (base / "app_data.json").write_text(raw_payload, encoding="utf-8")
            template = "<script>const DB=__DATA__;</script>"
            (base / "app_tpl.html").write_text(template, encoding="utf-8")
            (base / "app.html").write_text(build_app.render_html(template, raw_payload), encoding="utf-8")
            react_path = base.parent / "frontend" / "public" / "scripture-data.json"
            react_path.parent.mkdir(parents=True)
            react_path.write_text(build_app.render_react_payload(payload), encoding="utf-8")

            with mock.patch.object(verify_pipeline, "BASE", base):
                self.assertEqual(verify_pipeline.verify(), (1, 1))

    def test_chapter_zero_is_not_coerced_to_chapter_one(self):
        row = complete_dataset_row(chapter=0)
        self._verify_chapter_mapping(row, app_chapter=0)

    def test_missing_and_none_chapter_default_to_one(self):
        missing_chapter = complete_dataset_row()
        missing_chapter.pop("chapter")
        self._verify_chapter_mapping(missing_chapter, app_chapter=1)
        self._verify_chapter_mapping(complete_dataset_row(chapter=None), app_chapter=1)


class LoaderResolutionTests(unittest.TestCase):
    def test_loader_is_resolved_from_config_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            config_dir = Path(directory)
            loader = config_dir / "loader.py"
            loader.write_text("def load():\n    return [{'verse': 1}]\n", encoding="utf-8")
            previous = Path.cwd()
            try:
                os.chdir("/")
                rows = load_verses({"loader": "loader.py"}, config_dir=config_dir)
            finally:
                os.chdir(previous)
            self.assertEqual(rows, [{"verse": 1}])


class RepositoryIntegrationTests(unittest.TestCase):
    def test_committed_payload_and_generated_app_are_consistent(self):
        datasets, rows = verify_pipeline.verify(live=False)
        self.assertEqual(datasets, 7)
        self.assertEqual(rows, 1017)


if __name__ == "__main__":
    unittest.main()
