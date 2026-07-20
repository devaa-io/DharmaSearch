# DharmaSearch - content build

Complete, gap-free scripture datasets and the app that reads them.

## What's here
- `app.html` - the DharmaSearch app (Today / Begin / Explore / Meditate).
  Ships with the COMPLETE Bhagavad Gita: 701 verses, 18 chapters, each in
  Devanagari, IAST, Malayalam, Tamil, Telugu, Kannada + English. Other 15
  texts are marked "preview" until run through the pipeline.
- `ingest_pipeline.py` - the reusable pipeline that builds any text to the
  same standard. Script-to-script transliteration from correct Devanagari;
  a hard gap gate that fails the build if any verse is missing any field.
- `loaders/gita.py`, `sources/gita.json` - worked example (reproduces the Gita).
- `data/gita.json` - the complete Gita dataset the pipeline produced.

## Reproduce the Gita
    pip install indic-transliteration requests
    python ingest_pipeline.py --config sources/gita.json --out data/gita.json

## Add another text
1. Write `loaders/<text>.py` with `def load() -> list[dict]` returning raw
   verses (each with a Devanagari field). Source from sanskritdocuments.org /
   GRETIL - see the sourcing notes at the bottom of ingest_pipeline.py.
2. Write `sources/<text>.json` mapping the raw keys.
3. `python ingest_pipeline.py --config sources/<text>.json --out data/<text>.json`
4. Build fails on any gap. Fix source, rerun, until zero gaps.

Run this on your own infra (laptop/Render) where the network reaches the
scholarly archives - the chat sandbox could only reach the Gita's GitHub dataset.
