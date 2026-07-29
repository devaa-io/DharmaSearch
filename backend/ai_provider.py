"""Direct OpenAI integrations used by DharmaSearch.

This module deliberately contains no database code.  Keeping provider calls and
the TTS cache specification here makes the API routes easier to test without
network access.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import unicodedata
from typing import Iterable

from openai import AsyncOpenAI


SUPPORTED_TTS_SCRIPTS = ("en", "dev", "iast", "ml", "ta", "te", "kn")
SUPPORTED_TTS_VOICES = (
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "nova",
    "onyx",
    "sage",
    "shimmer",
    "verse",
)
TTS_RESPONSE_FORMAT = "mp3"
TTS_MIME_TYPE = "audio/mpeg"
TTS_SPEED = 0.9
TTS_INSTRUCTION_VERSION = "sanskrit-pronunciation-v1"
MAX_TTS_CHARACTERS = 4096

_client: AsyncOpenAI | None = None


def get_openai_client() -> AsyncOpenAI:
    """Return one lazily-created async client without logging its credential."""
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        _client = AsyncOpenAI(
            api_key=api_key,
            timeout=float(os.environ.get("OPENAI_TIMEOUT_SECONDS", "60")),
            max_retries=int(os.environ.get("OPENAI_MAX_RETRIES", "1")),
        )
    return _client


async def close_openai_client() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None


def select_tts_text(verse: dict, script: str) -> str:
    """Select exactly the requested representation; never use romanised text."""
    transliterations = verse.get("transliterations") or {}
    if script == "en":
        value = verse.get("translation")
    elif script == "dev":
        value = verse.get("devanagari")
    elif script == "iast":
        value = transliterations.get("iast")
    elif script in {"ml", "ta", "te", "kn"}:
        value = transliterations.get(script)
    else:
        raise ValueError(f"Unsupported script: {script}")

    return unicodedata.normalize("NFC", str(value or "").strip())


def tts_instructions(script: str) -> str:
    if script == "en":
        return "Read this English translation clearly, warmly, and at a measured pace."
    if script == "dev":
        return (
            "Recite this Sanskrit verse from Devanagari carefully, with clear syllables, "
            "natural sandhi, and a calm devotional cadence."
        )
    return (
        "Recite this Sanskrit verse from the supplied transliteration carefully, "
        "with clear syllables and a calm devotional cadence."
    )


def tts_cache_id(
    *,
    verse_id: str,
    script: str,
    voice: str,
    model: str,
    source_text: str,
) -> str:
    specification = {
        "instruction_version": TTS_INSTRUCTION_VERSION,
        "model": model,
        "response_format": TTS_RESPONSE_FORMAT,
        "script": script,
        "source_text_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "speed": TTS_SPEED,
        "verse_id": verse_id,
        "voice": voice,
    }
    canonical = json.dumps(
        specification,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validated_ai_verse_ids(
    response_text: str,
    candidate_ids: Iterable[str],
    *,
    limit: int = 10,
) -> list[str]:
    """Parse, deduplicate, cap, and constrain model output to supplied IDs."""
    text = (response_text or "").strip()
    if "```" in text:
        chunks = text.split("```")
        text = chunks[1] if len(chunks) > 1 else text
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
    try:
        payload = json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError):
        return []

    values = payload.get("verse_ids", []) if isinstance(payload, dict) else payload
    if not isinstance(values, list):
        return []

    candidates = set(candidate_ids)
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str) or value not in candidates or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if len(result) >= limit:
            break
    return result


async def complete_chat(
    *,
    system_message: str,
    user_message: str,
    json_object: bool = False,
    max_tokens: int = 1200,
) -> str:
    kwargs = {
        "model": os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": max_tokens,
    }
    if json_object:
        kwargs["response_format"] = {"type": "json_object"}
    response = await get_openai_client().chat.completions.create(**kwargs)
    return (response.choices[0].message.content or "").strip()


async def synthesize_tts(*, text: str, script: str, voice: str, model: str) -> str:
    response = await get_openai_client().audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        instructions=tts_instructions(script),
        response_format=TTS_RESPONSE_FORMAT,
        speed=TTS_SPEED,
    )
    content = response.content
    if not isinstance(content, (bytes, bytearray)):
        raise RuntimeError("OpenAI returned an invalid audio payload")
    return base64.b64encode(content).decode("ascii")
