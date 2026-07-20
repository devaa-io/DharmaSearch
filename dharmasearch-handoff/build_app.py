#!/usr/bin/env python3
"""
build_app.py - assemble the deployable DharmaSearch app.

The app is maintained as two parts so the huge inlined data never has to be
hand-edited:
    app_tpl.html   - the template (UI + logic) with a single __DATA__ placeholder
    <payload>.json - the app data payload (texts + verses + chapterMeta + begin)

This script inlines the payload into the template and writes app.html, the
single self-contained file you deploy (rename to index.html on the host).

Usage:
    python build_app.py --template app_tpl.html --data app_data.json --out app.html

Regenerating the data payload from pipeline output is a separate step - see
CLAUDE.md ("Rebuilding the app data"). This script only does the inlining.
"""
import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="app_tpl.html")
    ap.add_argument("--data", default="app_data.json")
    ap.add_argument("--out", default="app.html")
    a = ap.parse_args()

    tpl = Path(a.template).read_text(encoding="utf-8")
    if "__DATA__" not in tpl:
        sys.exit(f"{a.template} has no __DATA__ placeholder - wrong template?")

    # validate the payload is real JSON before inlining
    raw = Path(a.data).read_text(encoding="utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"{a.data} is not valid JSON: {e}")

    for key in ("texts", "verses"):
        if key not in payload:
            sys.exit(f"payload missing required key '{key}'")

    html = tpl.replace("__DATA__", raw)
    Path(a.out).write_text(html, encoding="utf-8")

    kb = Path(a.out).stat().st_size // 1024
    n_complete = sum(1 for t in payload["texts"] if t.get("complete"))
    print(f"Wrote {a.out}  ({kb} KB)")
    print(f"  texts: {len(payload['texts'])}  ({n_complete} complete)")
    print(f"  verses: {len(payload['verses'])}")
    print("Deploy: rename to index.html on your host (Netlify manual deploy or CLI).")

if __name__ == "__main__":
    main()
