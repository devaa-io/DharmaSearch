import asyncio
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

os.environ.setdefault("MONGO_URL", "mongodb://127.0.0.1:27017")
os.environ.setdefault("DB_NAME", "dharmasearch_unit_tests")
os.environ.setdefault("JWT_SECRET", "unit-test-secret")
os.environ.setdefault(
    "CORS_ORIGINS",
    "http://localhost:3000,https://dharmasearch-demo.netlify.app",
)

import server  # noqa: E402


class MemoryRateLimits:
    def __init__(self):
        self.counts = {}

    async def find_one_and_update(self, query, update, **_kwargs):
        key = query["_id"]
        self.counts[key] = self.counts.get(key, 0) + update["$inc"]["count"]
        return {"_id": key, "count": self.counts[key]}


class MemoryTTSCache:
    def __init__(self, documents=None):
        self.documents = documents or {}

    async def find_one(self, query, _projection=None):
        document = self.documents.get(query["_id"])
        if document is None:
            return None
        return {key: value for key, value in document.items() if key != "_id"}

    async def update_one(self, query, update, **_kwargs):
        self.documents[query["_id"]] = {"_id": query["_id"], **update["$set"]}
        return SimpleNamespace()

    async def count_documents(self, _query):
        return len(self.documents)


class MemoryTTSLocks:
    def __init__(self):
        self.documents = {}

    async def insert_one(self, document):
        if document["_id"] in self.documents:
            raise DuplicateKeyError("already claimed")
        self.documents[document["_id"]] = dict(document)
        return SimpleNamespace()

    async def find_one(self, query, _projection=None):
        document = self.documents.get(query["_id"])
        if not document:
            return None
        expires_at = query.get("expires_at", {}).get("$gt")
        if expires_at and document["expires_at"] <= expires_at:
            return None
        return dict(document)

    async def find_one_and_update(self, query, update, **_kwargs):
        document = self.documents.get(query["_id"])
        if not document:
            return None
        latest_allowed = query.get("expires_at", {}).get("$lte")
        if latest_allowed and document["expires_at"] > latest_allowed:
            return None
        document.update(update["$set"])
        return dict(document)

    async def delete_one(self, query):
        document = self.documents.get(query["_id"])
        if document and document.get("token") == query.get("token"):
            del self.documents[query["_id"]]
        return SimpleNamespace()


class StaticVerses:
    def __init__(self, verse):
        self.verse = verse

    async def find_one(self, _query, _projection=None):
        return self.verse


class ServerRuntimeTests(unittest.IsolatedAsyncioTestCase):
    def request(self, *, headers=None, host="127.0.0.1", method="POST"):
        return SimpleNamespace(
            headers=headers or {},
            client=SimpleNamespace(host=host),
            method=method,
        )

    async def test_anonymous_devanagari_tts_is_cached_by_full_spec(self):
        verse = {
            "verse_id": "bg-2-47",
            "translation": "You have a right to action.",
            "devanagari": "कर्मण्येवाधिकारस्ते",
            "text": "karmanye vadhikaraste",
            "transliterations": {"iast": "karmaṇy evādhikāras te"},
        }
        fake_db = SimpleNamespace(
            verses=StaticVerses(verse),
            tts_cache=MemoryTTSCache(),
            tts_locks=MemoryTTSLocks(),
            rate_limits=MemoryRateLimits(),
        )
        synthesize = AsyncMock(return_value="bXAz")
        with (
            patch.object(server, "db", fake_db),
            patch.object(server, "synthesize_tts", synthesize),
            patch.dict(
                os.environ,
                {
                    "TTS_REQUESTS_PER_MINUTE": "30",
                    "TTS_GENERATIONS_PER_MINUTE": "5",
                    "TTS_GLOBAL_GENERATIONS_PER_MINUTE": "10",
                    "TTS_CACHE_MAX_ENTRIES": "350",
                    "TTS_MAX_AUDIO_BYTES": "500000",
                    "TRUST_PROXY_HEADERS": "false",
                },
            ),
        ):
            request = self.request()
            first = await server.generate_tts(
                server.TTSInput(verse_id="bg-2-47", script="dev"),
                request,
            )
            second = await server.generate_tts(
                server.TTSInput(verse_id="bg-2-47", script="dev"),
                request,
            )

        self.assertFalse(first["cached"])
        self.assertTrue(second["cached"])
        self.assertEqual(first["script"], "dev")
        self.assertEqual(first["mime_type"], "audio/mpeg")
        synthesize.assert_awaited_once()
        self.assertEqual(
            synthesize.await_args.kwargs["text"],
            "कर्मण्येवाधिकारस्ते",
        )
        self.assertNotIn("karmanye", synthesize.await_args.kwargs["text"])

    async def test_concurrent_cache_misses_coalesce_to_one_provider_call(self):
        verse = {
            "verse_id": "bg-2-47",
            "devanagari": "कर्मण्येवाधिकारस्ते",
        }
        fake_db = SimpleNamespace(
            verses=StaticVerses(verse),
            tts_cache=MemoryTTSCache(),
            tts_locks=MemoryTTSLocks(),
            rate_limits=MemoryRateLimits(),
        )

        async def delayed_audio(**_kwargs):
            await asyncio.sleep(0.05)
            return "bXAz"

        synthesize = AsyncMock(side_effect=delayed_audio)
        with (
            patch.object(server, "db", fake_db),
            patch.object(server, "synthesize_tts", synthesize),
        ):
            results = await asyncio.gather(
                server.generate_tts(
                    server.TTSInput(verse_id="bg-2-47", script="dev"),
                    self.request(host="198.51.100.1"),
                ),
                server.generate_tts(
                    server.TTSInput(verse_id="bg-2-47", script="dev"),
                    self.request(host="198.51.100.2"),
                ),
            )

        synthesize.assert_awaited_once()
        self.assertEqual(sorted(result["cached"] for result in results), [False, True])

    async def test_cache_capacity_stops_new_provider_generation(self):
        verse = {
            "verse_id": "bg-2-47",
            "devanagari": "कर्मण्येवाधिकारस्ते",
        }
        fake_db = SimpleNamespace(
            verses=StaticVerses(verse),
            tts_cache=MemoryTTSCache({"existing": {"_id": "existing"}}),
            tts_locks=MemoryTTSLocks(),
            rate_limits=MemoryRateLimits(),
        )
        synthesize = AsyncMock()
        with (
            patch.object(server, "db", fake_db),
            patch.object(server, "synthesize_tts", synthesize),
            patch.dict(os.environ, {"TTS_CACHE_MAX_ENTRIES": "1"}),
        ):
            with self.assertRaises(HTTPException) as raised:
                await server.generate_tts(
                    server.TTSInput(verse_id="bg-2-47", script="dev"),
                    self.request(),
                )

        self.assertEqual(raised.exception.status_code, 503)
        synthesize.assert_not_awaited()
        self.assertEqual(fake_db.tts_locks.documents, {})

    async def test_missing_requested_script_never_calls_provider(self):
        fake_db = SimpleNamespace(
            verses=StaticVerses({"verse_id": "only-roman", "text": "ascii"}),
            tts_cache=MemoryTTSCache(),
            tts_locks=MemoryTTSLocks(),
            rate_limits=MemoryRateLimits(),
        )
        synthesize = AsyncMock()
        with (
            patch.object(server, "db", fake_db),
            patch.object(server, "synthesize_tts", synthesize),
        ):
            with self.assertRaises(HTTPException) as raised:
                await server.generate_tts(
                    server.TTSInput(verse_id="only-roman", script="dev"),
                    self.request(),
                )
        self.assertEqual(raised.exception.status_code, 422)
        synthesize.assert_not_awaited()

    async def test_rate_limit_returns_retry_after(self):
        fake_db = SimpleNamespace(rate_limits=MemoryRateLimits())
        with patch.object(server, "db", fake_db):
            await server.enforce_rate_limit(scope="test", identity="one", limit=1)
            with self.assertRaises(HTTPException) as raised:
                await server.enforce_rate_limit(scope="test", identity="one", limit=1)
        self.assertEqual(raised.exception.status_code, 429)
        self.assertGreaterEqual(int(raised.exception.headers["Retry-After"]), 1)

    def test_proxy_identity_uses_rightmost_forwarded_address_only_when_enabled(self):
        request = self.request(
            headers={"x-forwarded-for": "spoofed, 198.51.100.7"},
            host="10.0.0.2",
        )
        with patch.dict(os.environ, {"TRUST_PROXY_HEADERS": "true"}):
            self.assertEqual(server.request_client_identity(request), "198.51.100.7")
        with patch.dict(os.environ, {"TRUST_PROXY_HEADERS": "false"}):
            self.assertEqual(server.request_client_identity(request), "10.0.0.2")

    def test_cors_origins_are_trimmed_deduplicated_and_never_wildcard(self):
        with patch.dict(
            os.environ,
            {"CORS_ORIGINS": " https://one.example/ ,https://one.example,http://localhost:3000 "},
        ):
            self.assertEqual(
                server.configured_origins(),
                ["https://one.example", "http://localhost:3000"],
            )
        with patch.dict(os.environ, {"CORS_ORIGINS": "*"}):
            with self.assertRaises(RuntimeError):
                server.configured_origins()

    async def test_untrusted_write_origin_is_rejected(self):
        request = self.request(headers={"origin": "https://evil.example"})
        call_next = AsyncMock()
        response = await server.validate_write_origin(request, call_next)
        self.assertEqual(response.status_code, 403)
        call_next.assert_not_awaited()

    async def test_configured_write_origin_and_cli_request_are_allowed(self):
        call_next = AsyncMock(return_value="ok")
        allowed = self.request(
            headers={"origin": "https://dharmasearch-demo.netlify.app"},
        )
        self.assertEqual(await server.validate_write_origin(allowed, call_next), "ok")
        no_origin = self.request(headers={})
        self.assertEqual(await server.validate_write_origin(no_origin, call_next), "ok")

    async def test_admin_is_opt_in_and_existing_password_is_never_reset(self):
        users = SimpleNamespace(
            find_one=AsyncMock(return_value=None),
            insert_one=AsyncMock(),
            update_one=AsyncMock(),
        )
        with (
            patch.object(server, "db", SimpleNamespace(users=users)),
            patch.dict(os.environ, {"ADMIN_EMAIL": "", "ADMIN_PASSWORD": ""}),
        ):
            await server.seed_admin()
        users.find_one.assert_not_awaited()
        users.insert_one.assert_not_awaited()

        users.find_one = AsyncMock(return_value={"email": "owner@example.com"})
        with (
            patch.object(server, "db", SimpleNamespace(users=users)),
            patch.dict(
                os.environ,
                {"ADMIN_EMAIL": "owner@example.com", "ADMIN_PASSWORD": "new-secure-value"},
            ),
        ):
            await server.seed_admin()
        users.update_one.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
