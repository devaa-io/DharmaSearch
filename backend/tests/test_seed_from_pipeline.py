import unittest

from seed_from_pipeline import additive_verse_update, replacement_fields


class PipelineSeederTests(unittest.TestCase):
    def test_iast_is_added_to_nested_transliterations_and_legacy_field(self):
        update = additive_verse_update(
            {
                "complete": True,
                "iast": "karmaṇy evādhikāras te",
                "roman": "karmanye vadhikaraste",
                "scripts": {},
            }
        )
        self.assertEqual(update["iast"], "karmaṇy evādhikāras te")
        self.assertEqual(
            update["transliterations.iast"],
            "karmaṇy evādhikāras te",
        )
        self.assertNotIn("text", update)

    def test_default_additive_update_does_not_replace_rendered_text(self):
        row = {
            "roman": "pipeline roman",
            "en": "pipeline translation",
            "kw": ["action"],
        }
        update = additive_verse_update(row)
        self.assertNotIn("text", update)
        self.assertNotIn("translation", update)
        self.assertNotIn("keywords", update)
        self.assertEqual(
            replacement_fields(row),
            {
                "text": "pipeline roman",
                "translation": "pipeline translation",
                "keywords": ["action"],
            },
        )


if __name__ == "__main__":
    unittest.main()
