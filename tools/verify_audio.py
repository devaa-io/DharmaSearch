#!/usr/bin/env python3
"""Verify DharmaSearch static narration against a canonical spec.

Exists because the previous Gita Chapter 2 generation was described in its PR
as "audited and approved" with no automated check behind that claim, and the
model that actually shipped (eleven_v3) was not the one approved
(eleven_multilingual_v2) - silently, for every Devanagari clip, until this was
traced by hand. This script makes that class of drift impossible to miss:
every clip is checked against an explicit spec, not trusted because a commit
message said so.

What this can and cannot verify:
  - CAN verify: the right model/voice/settings/seed were used, the file on
    disk matches what the manifest claims (hash, size), the file is a real
    MP3 and not an empty/HTML/truncated response, every verse that should
    have a clip does, and the clip's recorded character count still matches
    the live verse text (catches audio going stale after a text edit).
  - CANNOT verify: whether it actually sounds right. That takes a human ear.
    Use --sample to get a small, spread-out set of clips worth listening to.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = REPO_ROOT / "dharmasearch-handoff" / "app_data.json"
DEFAULT_MANIFEST = REPO_ROOT / "frontend" / "public" / "audio-manifest.json"
DEFAULT_AUDIO_DIR = REPO_ROOT / "frontend" / "public" / "audio"

# Bytes-per-second for the fixed CBR format ElevenLabs returns here.
# mp3_44100_128 = 128 kbps constant bitrate.
BYTES_PER_SECOND = {"mp3_44100_128": 128_000 / 8}

# The canonical, approved spec per script. Anything in the manifest that
# doesn't match this exactly is a defect, not a style choice.
SPEC = {
    "dev": {
        "model_id": "eleven_multilingual_v2",
        "voice_id": "7u0hdhvWJRrAxXOSMYpp",
        "voice_settings": {
            "stability": 0.62, "similarity_boost": 0.78, "style": 0.0,
            "use_speaker_boost": True, "speed": 0.88,
        },
        "seed": 108,
    },
    "en": {
        "model_id": "eleven_multilingual_v2",
        "voice_id": "7u0hdhvWJRrAxXOSMYpp",
        "voice_settings": {
            "stability": 0.57, "similarity_boost": 0.75, "style": 0.0,
            "use_speaker_boost": True, "speed": 1.0,
        },
        "seed": None,
    },
}


def is_valid_mp3(path: Path) -> bool:
    with path.open("rb") as handle:
        head = handle.read(4)
    if head[:3] == b"ID3":
        return True
    return len(head) >= 2 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0


def verify(data_path: Path, manifest_path: Path, audio_dir: Path, only_text: str | None) -> list[str]:
    problems: list[str] = []

    data = json.loads(data_path.read_text(encoding="utf-8"))
    verses = {
        v["id"]: v for v in data["verses"]
        if v.get("complete") and (only_text is None or v.get("tid") == only_text)
    }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    clips_by_key = {(c["verse_id"], c["script"]): c for c in manifest["clips"]}

    for verse_id, verse in sorted(verses.items()):
        for script in ("dev", "en"):
            key = (verse_id, script)
            clip = clips_by_key.get(key)
            if clip is None:
                problems.append(f"MISSING  {verse_id}:{script} has no manifest entry")
                continue

            spec = SPEC[script]
            if clip.get("model_id") != spec["model_id"]:
                problems.append(
                    f"MODEL    {verse_id}:{script} model_id={clip.get('model_id')!r}, "
                    f"expected {spec['model_id']!r}"
                )
            if clip.get("voice_id") != spec["voice_id"]:
                problems.append(f"VOICE    {verse_id}:{script} voice_id mismatch")
            if clip.get("voice_settings") != spec["voice_settings"]:
                problems.append(
                    f"SETTINGS {verse_id}:{script} {clip.get('voice_settings')} != {spec['voice_settings']}"
                )
            if clip.get("seed") != spec["seed"]:
                problems.append(f"SEED     {verse_id}:{script} seed={clip.get('seed')!r}, expected {spec['seed']!r}")

            expected_text = str(verse.get(script) or "").strip()
            if clip.get("characters") != len(expected_text):
                problems.append(
                    f"STALE    {verse_id}:{script} manifest characters={clip.get('characters')}, "
                    f"live text is {len(expected_text)} chars - regenerate after this edit"
                )

            file_path = audio_dir / Path(clip["path"]).name
            if not file_path.exists():
                problems.append(f"NOFILE   {verse_id}:{script} {clip['path']} does not exist on disk")
                continue
            payload = file_path.read_bytes()
            if not payload:
                problems.append(f"EMPTY    {verse_id}:{script} {clip['path']} is a zero-byte file")
                continue
            actual_hash = hashlib.sha256(payload).hexdigest()
            if actual_hash != clip.get("sha256"):
                problems.append(f"HASH     {verse_id}:{script} file on disk does not match manifest sha256")
            if not is_valid_mp3(file_path):
                problems.append(f"NOTMP3   {verse_id}:{script} {clip['path']} has no ID3/MPEG signature")

            bps = BYTES_PER_SECOND.get(clip.get("output_format"))
            if bps and expected_text:
                duration = len(payload) / bps
                chars_per_sec = len(expected_text) / duration if duration else 0
                if not (1.5 <= chars_per_sec <= 25):
                    problems.append(
                        f"PACING   {verse_id}:{script} {duration:.1f}s for {len(expected_text)} chars "
                        f"({chars_per_sec:.1f} chars/sec) - listen to this one"
                    )

    return problems


def sample(manifest_path: Path, audio_dir: Path, count: int, seed: int) -> list[dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_chapter: dict[str, list[dict]] = {}
    for clip in manifest["clips"]:
        parts = clip["verse_id"].split("-")
        ch = parts[1] if len(parts) > 2 else "0"
        by_chapter.setdefault(ch, []).append(clip)

    rng = random.Random(seed)
    chapters = sorted(by_chapter, key=lambda c: int(c) if c.isdigit() else 0)
    picks = []
    idx = 0
    while len(picks) < count and chapters:
        ch = chapters[idx % len(chapters)]
        pool = by_chapter[ch]
        if pool:
            picks.append(pool.pop(rng.randrange(len(pool))))
        idx += 1
        if all(not v for v in by_chapter.values()):
            break
    return picks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    parser.add_argument("--only", help="restrict to one text id, e.g. bhagavad-gita")
    parser.add_argument("--sample", type=int, metavar="N", help="print N clip paths spread across chapters for manual listening, then exit")
    parser.add_argument("--sample-seed", type=int, default=42)
    args = parser.parse_args()

    if args.sample:
        picks = sample(args.manifest, args.audio_dir, args.sample, args.sample_seed)
        print(f"{len(picks)} clips to listen to, spread across chapters:\n")
        for clip in picks:
            print(f"  {args.audio_dir / Path(clip['path']).name}")
            print(f"    {clip['verse_id']}:{clip['script']}  model={clip['model_id']}  {clip['characters']} chars")
        return 0

    problems = verify(args.data, args.manifest, args.audio_dir, args.only)
    if problems:
        print(f"AUDIO VERIFY FAILED: {len(problems)} problem(s)\n")
        for line in problems:
            print(" ", line)
        return 1
    print("Audio verify OK: every clip matches its spec, hash, and live source text.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
