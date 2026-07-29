#!/usr/bin/env python3
"""Generate idempotent static DharmaSearch verse audio with ElevenLabs.

The API key is read only from ELEVENLABS_API_KEY. It is never accepted as a
command-line argument, written to disk, or included in the generated manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = REPO_ROOT / "dharmasearch-handoff" / "app_data.json"
DEFAULT_OUTPUT = REPO_ROOT / "frontend" / "public" / "audio"
DEFAULT_MANIFEST = REPO_ROOT / "frontend" / "public" / "audio-manifest.json"
DEFAULT_SCRIPTS = ("dev", "en")
SUPPORTED_SCRIPTS = ("en", "dev", "iast", "ml", "ta", "te", "kn")
LANGUAGE_CODES = {
    "en": "en",
    "dev": "hi",
    "iast": "hi",
    "ml": "ml",
    "ta": "ta",
    "te": "te",
    "kn": "kn",
}
DEFAULT_MODEL = "eleven_v3"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_PRICE_PER_1K = Decimal("0.10")


@dataclass(frozen=True)
class Scope:
    selector: str
    scripts: tuple[str, ...]


@dataclass(frozen=True)
class Clip:
    verse_id: str
    text_id: str
    script: str
    text: str
    path: Path

    @property
    def pair(self) -> tuple[str, str]:
        return self.verse_id, self.script


def parse_scope(raw: str) -> Scope:
    selector, separator, script = raw.rpartition(":")
    if not separator:
        selector, script = raw, ""
    selector = selector.strip() or "*"
    scripts = DEFAULT_SCRIPTS if not script else tuple(
        item.strip() for item in script.split(",") if item.strip()
    )
    unknown = sorted(set(scripts) - set(SUPPORTED_SCRIPTS))
    if unknown:
        raise argparse.ArgumentTypeError(
            f"unsupported script(s): {', '.join(unknown)}; choose from {', '.join(SUPPORTED_SCRIPTS)}"
        )
    return Scope(selector=selector, scripts=scripts)


def parse_variant(raw: str) -> str:
    variant = raw.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", variant):
        raise argparse.ArgumentTypeError(
            "variant must contain only lowercase letters, digits, and hyphens"
        )
    return variant


def parse_script_mapping(raw: str) -> tuple[str, str]:
    script, separator, value = raw.partition("=")
    script = script.strip()
    value = value.strip()
    if not separator or script not in SUPPORTED_SCRIPTS or not value:
        raise argparse.ArgumentTypeError(
            "mapping must be SCRIPT=VALUE, where SCRIPT is one of "
            f"{', '.join(SUPPORTED_SCRIPTS)}"
        )
    return script, value


def script_mapping(items: Iterable[tuple[str, str]]) -> dict[str, str]:
    return {script: value for script, value in items}


def voice_for_script(
    script: str,
    voice_map: dict[str, str],
    fallback: str | None,
) -> str | None:
    return voice_map.get(script) or fallback


def script_text(verse: dict, script: str) -> str:
    if script in {"en", "dev", "iast"}:
        return str(verse.get(script) or "").strip()
    return str((verse.get("scripts") or {}).get(script) or "").strip()


def selector_matches(verse: dict, selector: str) -> bool:
    if selector == "*":
        return True
    text_id, separator, chapter = selector.rpartition("/")
    if separator and chapter.isdigit():
        return (
            verse.get("tid") == text_id
            and str(verse.get("ch")) == str(int(chapter))
        )
    return verse.get("tid") == selector or verse.get("id") == selector


def selected_clips(
    data: dict,
    scopes: list[Scope],
    output_dir: Path,
    variant: str | None = None,
) -> tuple[list[Clip], list[str]]:
    verses = [verse for verse in data.get("verses", []) if verse.get("complete")]
    active_scopes = scopes or [Scope("*", DEFAULT_SCRIPTS)]
    clips: dict[tuple[str, str], Clip] = {}
    missing: list[str] = []

    for scope in active_scopes:
        matched = [
            verse for verse in verses
            if selector_matches(verse, scope.selector)
        ]
        if not matched:
            raise ValueError(f"--only selector matched no verified verses: {scope.selector}")
        for verse in matched:
            verse_id = str(verse["id"])
            for script in scope.scripts:
                text = script_text(verse, script)
                if not text:
                    missing.append(f"{verse_id}:{script}")
                    continue
                clip = Clip(
                    verse_id=verse_id,
                    text_id=str(verse.get("tid") or ""),
                    script=script,
                    text=text,
                    path=output_dir
                    / (
                        f"{verse_id}.{script}.{variant}.mp3"
                        if variant
                        else f"{verse_id}.{script}.mp3"
                    ),
                )
                clips[clip.pair] = clip
    return sorted(clips.values(), key=lambda clip: clip.pair), missing


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "clips": []}
    with path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest["clips"] = list(manifest.get("clips") or [])
    return manifest


def reusable_clip(
    clip: Clip,
    manifest: dict,
    model: str,
    voice_id: str | None,
    output_format: str,
    voice_settings: dict,
    seed: int | None,
) -> bool:
    if not clip.path.exists() or not clip.path.stat().st_size:
        return False
    if not voice_id:
        return True
    entry = next(
        (
            item
            for item in manifest.get("clips") or []
            if item.get("verse_id") == clip.verse_id
            and item.get("script") == clip.script
        ),
        None,
    )
    return bool(
        entry
        and entry.get("path") == f"/audio/{clip.path.name}"
        and entry.get("model_id") == model
        and entry.get("voice_id") == voice_id
        and entry.get("output_format") == output_format
        and entry.get("voice_settings") == voice_settings
        and entry.get("seed") == seed
    )


def manifest_entry(
    clip: Clip,
    model: str,
    voice_id: str,
    voice_name: str,
    output_format: str,
    voice_settings: dict,
    seed: int | None,
) -> dict:
    payload = clip.path.read_bytes()
    return {
        "verse_id": clip.verse_id,
        "script": clip.script,
        "path": f"/audio/{clip.path.name}",
        "characters": len(clip.text),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "language_code": LANGUAGE_CODES[clip.script],
        "model_id": model,
        "voice_id": voice_id,
        "voice_name": voice_name or None,
        "output_format": output_format,
        "voice_settings": voice_settings,
        "seed": seed,
    }


def write_manifest(
    path: Path,
    clips: Iterable[Clip],
    model: str,
    voice_map: dict[str, str],
    voice_name_map: dict[str, str],
    fallback_voice_id: str | None,
    fallback_voice_name: str,
    output_format: str,
    voice_settings: dict,
    seed: int | None,
) -> None:
    manifest = load_manifest(path)
    entries = {
        (entry.get("verse_id"), entry.get("script")): entry
        for entry in manifest["clips"]
    }
    for clip in clips:
        if clip.path.exists() and clip.path.stat().st_size:
            voice_id = voice_for_script(
                clip.script, voice_map, fallback_voice_id
            )
            if not voice_id:
                raise ValueError(f"no voice configured for script: {clip.script}")
            voice_name = (
                voice_name_map.get(clip.script) or fallback_voice_name
            )
            entries[clip.pair] = manifest_entry(
                clip,
                model,
                voice_id,
                voice_name,
                output_format,
                voice_settings,
                seed,
            )
    manifest_voice_map = {
        entry["script"]: entry["voice_id"]
        for entry in entries.values()
        if entry.get("script") and entry.get("voice_id")
    }
    manifest_voice_name_map = {
        entry["script"]: entry["voice_name"]
        for entry in entries.values()
        if entry.get("script") and entry.get("voice_name")
    }
    manifest_model_map = {
        entry["script"]: entry["model_id"]
        for entry in entries.values()
        if entry.get("script") and entry.get("model_id")
    }
    unique_voice_ids = set(manifest_voice_map.values())
    unique_voice_names = set(manifest_voice_name_map.values())
    unique_model_ids = set(manifest_model_map.values())
    manifest.update({
        "version": 1,
        "model_id": next(iter(unique_model_ids)) if len(unique_model_ids) == 1 else None,
        "model_map": dict(sorted(manifest_model_map.items())),
        "voice_id": next(iter(unique_voice_ids)) if len(unique_voice_ids) == 1 else None,
        "voice_name": next(iter(unique_voice_names)) if len(unique_voice_names) == 1 else None,
        "voice_map": dict(sorted(manifest_voice_map.items())),
        "voice_name_map": dict(sorted(manifest_voice_name_map.items())),
        "output_format": output_format,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "clips": sorted(
            entries.values(),
            key=lambda entry: (entry["verse_id"], entry["script"]),
        ),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def api_request(
    clip: Clip,
    api_key: str,
    voice_id: str,
    model: str,
    output_format: str,
    retries: int,
    voice_settings: dict,
    seed: int | None,
) -> bytes:
    endpoint = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{urllib.parse.quote(voice_id)}"
        f"?output_format={urllib.parse.quote(output_format)}"
    )
    request_body = {
        "text": clip.text,
        "model_id": model,
        "language_code": LANGUAGE_CODES[clip.script],
        "voice_settings": voice_settings,
        "apply_text_normalization": "auto",
    }
    if seed is not None:
        request_body["seed"] = seed
    body = json.dumps(request_body).encode()

    for attempt in range(retries + 1):
        request = urllib.request.Request(
            endpoint,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
                "xi-api-key": api_key,
                "User-Agent": "DharmaSearch-static-audio/1.0",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                payload = response.read()
                content_type = response.headers.get_content_type()
            if not payload or content_type not in {"audio/mpeg", "audio/mp3", "application/octet-stream"}:
                raise RuntimeError(
                    f"ElevenLabs returned unexpected content ({content_type}, {len(payload)} bytes)"
                )
            return payload
        except urllib.error.HTTPError as error:
            retryable = error.code == 429 or error.code >= 500
            if attempt >= retries or not retryable:
                detail = error.read(500).decode("utf-8", "replace")
                raise RuntimeError(f"ElevenLabs HTTP {error.code}: {detail}") from error
            retry_after = error.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2 ** (attempt + 1)
            time.sleep(delay)
        except urllib.error.URLError as error:
            if attempt >= retries:
                raise RuntimeError(f"ElevenLabs request failed: {error.reason}") from error
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("unreachable")


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    argument_parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    argument_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    argument_parser.add_argument(
        "--only",
        action="append",
        type=parse_scope,
        default=[],
        metavar="TEXT_OR_VERSE[:SCRIPT[,SCRIPT]]",
        help=(
            "repeatable scope, e.g. bhagavad-gita:dev, "
            "bhagavad-gita/2:dev,en, or bg-2-47:en,ml"
        ),
    )
    argument_parser.add_argument("--dry-run", action="store_true")
    argument_parser.add_argument(
        "--adopt-existing-only",
        action="store_true",
        help=(
            "record matching non-empty files in the manifest using the supplied "
            "model, voice, settings, and seed, then exit without API requests"
        ),
    )
    argument_parser.add_argument(
        "--variant",
        type=parse_variant,
        help=(
            "write comparison files as VERSE.SCRIPT.VARIANT.mp3 instead of the "
            "canonical static-audio filename"
        ),
    )
    argument_parser.add_argument(
        "--skip-manifest",
        action="store_true",
        help="do not add generated comparison files to audio-manifest.json",
    )
    argument_parser.add_argument(
        "--allow-bulk",
        action="store_true",
        help="required for a non-dry run without at least one --only scope",
    )
    argument_parser.add_argument("--max-clips", type=int)
    argument_parser.add_argument("--requests-per-minute", type=float, default=6.0)
    argument_parser.add_argument("--model", default=DEFAULT_MODEL)
    argument_parser.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    argument_parser.add_argument("--voice-name", default=os.environ.get("ELEVENLABS_VOICE_NAME", ""))
    argument_parser.add_argument(
        "--voice-map",
        action="append",
        type=parse_script_mapping,
        default=[],
        metavar="SCRIPT=VOICE_ID",
        help=(
            "repeatable per-script voice mapping; takes precedence over --voice-id, "
            "e.g. --voice-map dev=VOICE --voice-map ta=VOICE"
        ),
    )
    argument_parser.add_argument(
        "--voice-name-map",
        action="append",
        type=parse_script_mapping,
        default=[],
        metavar="SCRIPT=NAME",
        help="optional repeatable display names matching --voice-map",
    )
    argument_parser.add_argument("--output-format", default=DEFAULT_OUTPUT_FORMAT)
    argument_parser.add_argument("--stability", type=float, default=0.62)
    argument_parser.add_argument("--similarity-boost", type=float, default=0.78)
    argument_parser.add_argument("--style", type=float, default=0.0)
    argument_parser.add_argument("--speed", type=float, default=0.88)
    speaker_boost = argument_parser.add_mutually_exclusive_group()
    speaker_boost.add_argument(
        "--speaker-boost",
        dest="speaker_boost",
        action="store_true",
        default=True,
    )
    speaker_boost.add_argument(
        "--no-speaker-boost",
        dest="speaker_boost",
        action="store_false",
    )
    argument_parser.add_argument(
        "--seed",
        type=int,
        default=108,
        help="reproducibility seed; use --no-seed to use provider randomness",
    )
    argument_parser.add_argument(
        "--no-seed",
        dest="seed",
        action="store_const",
        const=None,
    )
    argument_parser.add_argument(
        "--price-per-1k",
        type=Decimal,
        default=DEFAULT_PRICE_PER_1K,
        help="list-price estimate only; defaults to $0.10/1K characters for v3",
    )
    argument_parser.add_argument("--retries", type=int, default=3)
    return argument_parser


def main() -> int:
    args = parser().parse_args()
    if args.requests_per_minute <= 0:
        raise SystemExit("--requests-per-minute must be positive")
    if args.max_clips is not None and args.max_clips <= 0:
        raise SystemExit("--max-clips must be positive")
    if args.skip_manifest and not args.variant:
        raise SystemExit("--skip-manifest is only allowed with --variant.")
    if args.adopt_existing_only and args.skip_manifest:
        raise SystemExit("--adopt-existing-only cannot be combined with --skip-manifest.")

    with args.data.open(encoding="utf-8") as handle:
        data = json.load(handle)
    try:
        selected, missing = selected_clips(
            data, args.only, args.output_dir, args.variant
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error

    voice_map = script_mapping(args.voice_map)
    voice_name_map = script_mapping(args.voice_name_map)
    voice_settings = {
        "stability": args.stability,
        "similarity_boost": args.similarity_boost,
        "style": args.style,
        "use_speaker_boost": args.speaker_boost,
        "speed": args.speed,
    }
    manifest = load_manifest(args.manifest)
    resolved_voice_ids = {
        clip.script: voice_for_script(clip.script, voice_map, args.voice_id)
        for clip in selected
    }
    if args.adopt_existing_only:
        adoptable = [
            clip
            for clip in selected
            if clip.path.exists() and clip.path.stat().st_size
        ]
        missing_voice_scripts = sorted(
            {
                clip.script
                for clip in adoptable
                if not resolved_voice_ids[clip.script]
            }
        )
        if missing_voice_scripts:
            raise SystemExit(
                "No voice configured for script(s): "
                + ", ".join(missing_voice_scripts)
            )
        if not adoptable:
            raise SystemExit("No non-empty selected audio files exist to adopt.")
        write_manifest(
            args.manifest,
            adoptable,
            args.model,
            voice_map,
            voice_name_map,
            args.voice_id,
            args.voice_name,
            args.output_format,
            voice_settings,
            args.seed,
        )
        print(f"Existing files adopted: {len(adoptable):,}")
        print(f"Manifest: {args.manifest}")
        print("No API requests made.")
        return 0
    existing = [
        clip
        for clip in selected
        if reusable_clip(
            clip,
            manifest,
            args.model,
            resolved_voice_ids[clip.script],
            args.output_format,
            voice_settings,
            args.seed,
        )
    ]
    pending = [clip for clip in selected if clip not in existing]
    characters = sum(len(clip.text) for clip in pending)
    estimated_cost = Decimal(characters) / Decimal(1000) * args.price_per_1k

    print(f"Verified clips selected: {len(selected):,}")
    print(f"Existing clips skipped: {len(existing):,}")
    print(f"Clips to generate: {len(pending):,}")
    print(f"Characters to generate: {characters:,}")
    print(f"Estimated API cost: ${estimated_cost.quantize(Decimal('0.01'))}")
    print(f"Model: {args.model}")
    print(f"Output format: {args.output_format}")
    print(f"Voice settings: {json.dumps(voice_settings, sort_keys=True)}")
    print(f"Seed: {args.seed if args.seed is not None else 'provider default'}")
    configured_voice_map = {
        script: voice_id
        for script, voice_id in resolved_voice_ids.items()
        if voice_id
    }
    if configured_voice_map:
        print(
            "Voice map: "
            + ", ".join(
                f"{script}={voice_id}"
                for script, voice_id in sorted(configured_voice_map.items())
            )
        )
    if missing:
        print(f"Missing source texts skipped: {len(missing):,}")

    if args.dry_run:
        print("Dry run: no files written and no API requests made.")
        return 0
    if not args.only and not args.allow_bulk:
        raise SystemExit("Refusing an unscoped generation; pass --only or --allow-bulk.")
    if args.max_clips is not None and len(pending) > args.max_clips:
        raise SystemExit(
            f"Refusing to generate {len(pending)} clips; --max-clips is {args.max_clips}."
        )

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("ELEVENLABS_API_KEY is required for generation.")
    missing_voice_scripts = sorted(
        {
            clip.script
            for clip in pending
            if not resolved_voice_ids[clip.script]
        }
    )
    if missing_voice_scripts:
        raise SystemExit(
            "No voice configured for script(s): "
            + ", ".join(missing_voice_scripts)
            + "; pass --voice-map SCRIPT=VOICE_ID or --voice-id."
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    interval = 60.0 / args.requests_per_minute
    completed: list[Clip] = list(existing)
    for index, clip in enumerate(pending, start=1):
        started = time.monotonic()
        print(f"[{index}/{len(pending)}] {clip.verse_id}:{clip.script}")
        payload = api_request(
            clip,
            api_key,
            resolved_voice_ids[clip.script],
            args.model,
            args.output_format,
            args.retries,
            voice_settings,
            args.seed,
        )
        temporary = clip.path.with_suffix(clip.path.suffix + ".tmp")
        temporary.write_bytes(payload)
        temporary.replace(clip.path)
        completed.append(clip)
        if not args.skip_manifest:
            write_manifest(
                args.manifest,
                [clip],
                args.model,
                voice_map,
                voice_name_map,
                args.voice_id,
                args.voice_name,
                args.output_format,
                voice_settings,
                args.seed,
            )
        elapsed = time.monotonic() - started
        if index < len(pending) and elapsed < interval:
            time.sleep(interval - elapsed)

    if not args.skip_manifest:
        write_manifest(
            args.manifest,
            completed,
            args.model,
            voice_map,
            voice_name_map,
            args.voice_id,
            args.voice_name,
            args.output_format,
            voice_settings,
            args.seed,
        )
        print(f"Manifest: {args.manifest}")
    else:
        print("Manifest: unchanged (comparison variant)")
    total_bytes = sum(clip.path.stat().st_size for clip in completed if clip.path.exists())
    print(f"Generated audio size represented in this run: {total_bytes / 1024 / 1024:.2f} MiB")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted; completed clips remain idempotently reusable.", file=sys.stderr)
        raise SystemExit(130)
