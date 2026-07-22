#!/usr/bin/env python3
"""
build_app.py - assemble the deployable DharmaSearch app.

The app is maintained as two parts so the huge inlined data never has to be
hand-edited:
    app_tpl.html   - the template (UI + logic) with a single __DATA__ placeholder
    <payload>.json - the app data payload (texts + verses + chapterMeta + begin)

This script inlines the payload into the template and writes app.html. It also
writes the same validated payload as a public data asset for frontend consumers,
so the generated artifacts cannot silently drift apart.

Usage:
    python3 build_app.py --template app_tpl.html --data app_data.json --out app.html

Regenerating the data payload from pipeline output is a separate step - see
CLAUDE.md ("Rebuilding the app data"). This script only does the inlining.
"""
import argparse
import json
import sys
from pathlib import Path

from pipeline_io import write_text_atomic
from pipeline_validation import ValidationError, validate_app_payload


PLACEHOLDER = "__DATA__"
BASE = Path(__file__).resolve().parent
DEFAULT_REACT_DATA = BASE.parent / "frontend" / "public" / "scripture-data.json"


def render_html(template: str, raw_payload: str) -> str:
    """Inline JSON without allowing source text to terminate the script element."""
    count = template.count(PLACEHOLDER)
    if count != 1:
        raise ValueError(f"template must contain exactly one {PLACEHOLDER} placeholder; found {count}")
    # In an HTML script element, a case-insensitive ``</script`` sequence ends the
    # element even when it occurs inside a JavaScript string. Escaping every less-than
    # sign is JSON-safe and also prevents comment/tag interpretation.
    safe_payload = raw_payload.replace("<", "\\u003c")
    return template.replace(PLACEHOLDER, safe_payload)


def render_react_payload(payload: dict) -> str:
    """Serialize the validated payload deterministically for the React app."""
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="app_tpl.html")
    ap.add_argument("--data", default="app_data.json")
    ap.add_argument("--out", default="app.html")
    ap.add_argument(
        "--react-data",
        default=str(DEFAULT_REACT_DATA),
        help="validated JSON asset for React; pass an empty string to skip",
    )
    a = ap.parse_args()

    tpl = Path(a.template).read_text(encoding="utf-8")
    # validate the payload is real JSON before inlining
    raw = Path(a.data).read_text(encoding="utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"{a.data} is not valid JSON: {e}")

    try:
        validate_app_payload(payload)
        html = render_html(tpl, raw)
    except (ValidationError, ValueError) as error:
        sys.exit(str(error))

    write_text_atomic(Path(a.out), html)

    if a.react_data:
        write_text_atomic(Path(a.react_data), render_react_payload(payload))

    kb = Path(a.out).stat().st_size // 1024
    n_complete = sum(1 for t in payload["texts"] if t.get("complete"))
    print(f"Wrote {a.out}  ({kb} KB)")
    print(f"  texts: {len(payload['texts'])}  ({n_complete} complete)")
    print(f"  verses: {len(payload['verses'])}")
    if a.react_data:
        print(f"  React data: {a.react_data}")
    print("Deploy: rename to index.html on your host (Netlify manual deploy or CLI).")

if __name__ == "__main__":
    main()
