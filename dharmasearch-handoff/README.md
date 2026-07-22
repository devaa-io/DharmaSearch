# DharmaSearch content build

Complete, gap-free scripture datasets for the self-contained prototype, plus a
validated public JSON asset ready for frontend consumers.

## Current payload

`app.html` contains seven complete texts: the Bhagavad Gita (701 verses) and six
principal Upanishads—Isha, Kena, Katha, Mundaka, Prashna, and Mandukya (316
verses). Each completed verse contains Devanagari, generated IAST, Malayalam,
Tamil, Telugu, Kannada, and a license-cleared English translation. The remaining
text groupings are clearly marked as previews.

## Requirements

```bash
python3 -m pip install -r requirements.txt
```

## Verify everything

The default verification is offline and deterministic. It validates every committed
dataset, all app counts and complete-text fields, unique IDs, and whether both
`app.html` and `../frontend/public/scripture-data.json` match the canonical payload:

```bash
python3 verify_pipeline.py
python3 -m unittest discover -s tests -v
```

Before publishing new source material, also reproduce every dataset from its live
upstream source:

```bash
python3 verify_pipeline.py --live
```

## Reproduce a dataset

Run from this directory. For example:

```bash
python3 ingest_pipeline.py \
  --config sources/katha_config.json \
  --out /tmp/katha.json
diff /tmp/katha.json data/katha-upanishad.json
```

The command exits non-zero if any verse lacks one of the seven required
representations or duplicates an existing chapter/verse identity. Loader paths are
resolved from the source config, so the command works from any current directory.
Never use `--allow-gaps` for a release build.

## Rebuild the app payload

After regenerating any completed datasets:

```bash
python3 build/merge_completed.py
python3 build_app.py --template app_tpl.html --data app_data.json --out app.html
```

The merger is idempotent, backs up `app_data.json`, validates counts and required
fields, synchronizes every completed app row from its canonical dataset, writes
atomically, and removes duplicated low-fidelity rows for completed texts from the
legacy mixed Upanishads preview. App generation performs the same payload validation
and safely escapes source text before embedding it in HTML. The same command writes
the compact validated frontend asset, keeping both generated artifacts synchronized
with the canonical payload.

## Add another text

1. Write `loaders/<text>.py` exposing `load() -> list[dict]`. Source genuine
   Unicode Devanagari and license-cleared English.
2. Add `sources/<text>_config.json` describing the field mapping.
3. Run the ingestion pipeline until it reports zero gaps.
4. Add the completed dataset to the app merger, rebuild `app.html`, and verify
   the app payload counts.

See `CLAUDE.md` for the non-negotiable data rules and `REVIEW-HANDOVER.md` for
source notes, review results, and blocked texts.
