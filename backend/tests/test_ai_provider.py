import asyncio
import base64
import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from pydantic import ValidationError

import ai_provider

os.environ.setdefault("MONGO_URL", "mongodb://127.0.0.1:27017")
os.environ.setdefault("DB_NAME", "dharmasearch_unit_tests")
os.environ.setdefault("JWT_SECRET", "unit-test-secret")


class AIProviderTests(unittest.TestCase):
    def setUp(self):
        self.verse = {
            "translation": "English meaning",
            "devanagari": "कर्मण्येवाधिकारस्ते",
            "iast": "legacy verified iast",
            "text": "karmanye vadhikaraste",
            "transliterations": {
                "iast": "karmaṇy evādhikāras te",
                "ml": "കർമണ്യേവാധികാരസ്തേ",
                "ta": "கர்மண்யேவாதிகாரஸ்தே",
                "te": "కర్మణ్యేవాధికారస్తే",
                "kn": "ಕರ್ಮಣ್ಯೇವಾಧಿಕಾರಸ್ತೇ",
            },
        }

    def test_all_supported_scripts_map_to_exact_verified_fields(self):
        expected = {
            "en": "English meaning",
            "dev": "कर्मण्येवाधिकारस्ते",
            "iast": "karmaṇy evādhikāras te",
            "ml": "കർമണ്യേവാധികാരസ്തേ",
            "ta": "கர்மண்யேவாதிகாரஸ்தே",
            "te": "కర్మణ్యేవాధికారస్తే",
            "kn": "ಕರ್ಮಣ್ಯೇವಾಧಿಕಾರಸ್ತೇ",
        }
        self.assertEqual(set(expected), set(ai_provider.SUPPORTED_TTS_SCRIPTS))
        for script, text in expected.items():
            with self.subTest(script=script):
                self.assertEqual(ai_provider.select_tts_text(self.verse, script), text)

    def test_iast_requires_the_nested_verified_transliteration(self):
        verse = {"iast": "ātmā", "text": "aatmaa", "transliterations": {}}
        self.assertEqual(ai_provider.select_tts_text(verse, "iast"), "")
        self.assertEqual(
            ai_provider.select_tts_text(
                {"transliterations": {"iast": "ātmā"}},
                "iast",
            ),
            "ātmā",
        )
        self.assertEqual(
            ai_provider.select_tts_text({"text": "roman only"}, "iast"),
            "",
        )

    def test_text_is_normalized_to_nfc(self):
        verse = {"translation": "e\u0301"}
        self.assertEqual(ai_provider.select_tts_text(verse, "en"), "é")

    def test_cache_changes_for_every_audio_input(self):
        base = {
            "verse_id": "bg-2-47",
            "script": "dev",
            "voice": "sage",
            "model": "gpt-4o-mini-tts",
            "source_text": "कर्म",
        }
        first = ai_provider.tts_cache_id(**base)
        self.assertEqual(first, ai_provider.tts_cache_id(**base))
        for field, value in {
            "script": "iast",
            "voice": "nova",
            "model": "future-model",
            "source_text": "धर्म",
        }.items():
            changed = dict(base)
            changed[field] = value
            with self.subTest(field=field):
                self.assertNotEqual(first, ai_provider.tts_cache_id(**changed))

    def test_ai_ids_are_capped_deduplicated_and_constrained(self):
        candidates = [f"id-{number}" for number in range(12)]
        payload = {
            "verse_ids": [
                "id-1",
                "unknown",
                "id-1",
                *[f"id-{number}" for number in range(2, 12)],
                42,
            ]
        }
        result = ai_provider.validated_ai_verse_ids(
            json.dumps(payload),
            candidates,
        )
        self.assertEqual(
            result,
            ["id-1", "id-2", "id-3", "id-4", "id-5", "id-6", "id-7", "id-8", "id-9", "id-10"],
        )

    def test_invalid_ai_response_returns_no_ids(self):
        self.assertEqual(ai_provider.validated_ai_verse_ids("not json", ["id-1"]), [])

    def test_tts_model_rejects_invalid_script_and_voice(self):
        from server import TTSInput

        with self.assertRaises(ValidationError):
            TTSInput(verse_id="bg-2-47", script="roman")
        with self.assertRaises(ValidationError):
            TTSInput(verse_id="bg-2-47", voice="arbitrary")

    def test_direct_tts_returns_base64_audio(self):
        create = AsyncMock(return_value=SimpleNamespace(content=b"mp3-bytes"))
        client = SimpleNamespace(
            audio=SimpleNamespace(speech=SimpleNamespace(create=create)),
        )
        with patch.object(ai_provider, "get_openai_client", return_value=client):
            result = asyncio.run(
                ai_provider.synthesize_tts(
                    text="कर्म",
                    script="dev",
                    voice="sage",
                    model="gpt-4o-mini-tts",
                )
            )
        self.assertEqual(result, base64.b64encode(b"mp3-bytes").decode("ascii"))
        kwargs = create.await_args.kwargs
        self.assertEqual(kwargs["input"], "कर्म")
        self.assertNotIn("English", kwargs["input"])
        self.assertIn("Devanagari", kwargs["instructions"])


if __name__ == "__main__":
    unittest.main()
