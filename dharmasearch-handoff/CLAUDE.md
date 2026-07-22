# DharmaSearch - context for Claude Code

Read this first. It captures where the project is and the rules that must not be broken.

## What this is
A Hindu-scripture reading and study app being shaped into a monetisable product.
The backing repo is a FastAPI + React + MongoDB app; this directory adds a content
pipeline and a static reading app that presents the scriptures.

Product goals:
- Take newcomers on a guided journey (not a flat list), while giving the devoted deep search.
- Show every verse as original text + transliteration + English translation.
- Scripts in scope: Devanagari, IAST, Malayalam, Tamil, Telugu, Kannada, English.
- A verse-of-the-day, saying-of-the-day, and a silent visual meditation window.

## The one rule that cannot be broken
**No text ships half done.** Every verse of a released text must carry every field:
devanagari, iast, english, ml, ta, te, kn. This is enforced mechanically by the
gap gate in `ingest_pipeline.py` - a build FAILS (non-zero exit) if any verse is
missing any field. Do not add `--allow-gaps` to a release build.

**Transliteration is script-to-script only.** Generate Malayalam/Tamil/Telugu/Kannada
by transliterating from correct Devanagari (lossless). NEVER transliterate from the
ASCII/romanised text - it lacks vowel-length and sibilant/retroflex information, so it
produces wrong sacred text (proven: "kaman" -> कमन् when it must be कामान्). If a source
lacks Devanagari, find a better source; do not guess.

## Current state
- **Seven texts are COMPLETE:** Bhagavad Gita (701 verses) plus Isha, Kena, Katha,
  Mundaka, Prashna, and Mandukya Upanishads (316 verses). Every completed row has
  all seven representations and passes the zero-gap gate.
- **The other 15 text groupings are PREVIEW only** - small seeded samples from the
  original `content-export/`, marked "preview" in the app. Completed Upanishads are
  removed from the legacy mixed `upanishads` preview to avoid duplicate search results.

## Why the rest weren't finished in the chat session
The chat sandbox could only reach GitHub raw + package mirrors. The authoritative
sources for the other texts live in archives it could not reach. Claude Code on a
machine with open network access CAN reach them - that's the main reason this work
moved here.

## File map (this directory)
- `app_tpl.html`     - the app: UI + logic, with a single `__DATA__` placeholder.
- `app_data.json`    - the app data payload (texts + verses + chapterMeta + begin path).
- `build_app.py`     - inlines app_data.json into app_tpl.html -> app.html (deploy this).
- `verify_pipeline.py` - deterministic offline verification; add `--live` to refetch
  and compare every configured upstream source.
- `pipeline_validation.py` - shared release-invariant checks used by ingestion,
  merging, app generation, tests, and CI.
- `app.html`         - generated, deployable single file (rename to index.html on host).
- `ingest_pipeline.py` - the reusable pipeline (source -> 7 representations -> gap gate).
- `loaders/gita.py`  - worked loader example (reproduces the Gita).
- `sources/gita_config.json` - worked config example.
- `data/bhagavad-gita.json`  - the complete Gita dataset the pipeline produced.
- `README.md`        - quick usage.

## How to complete another text (the core loop)
1. Write `loaders/<text>.py` exposing `def load() -> list[dict]`, returning raw verses
   each with a Devanagari field. Source from an authoritative edition (see below).
2. Write `sources/<text>.json` mapping the raw keys (see sources/gita_config.json).
3. Run: `python3 ingest_pipeline.py --config sources/<text>_config.json --out data/<text>.json`
4. If it reports gaps, the build FAILS and lists them. Fix the source/loader, rerun,
   until zero gaps. Only a zero-gap dataset is allowed into the app.

## Rebuilding the app data (after adding texts)
The app payload (`app_data.json`) is assembled from the per-text `data/*.json` files
plus chapter metadata and the "begin" path. When you add a completed text:
1. Add it to the completed-text merger and merge its `data/<text>.json` into
   `app_data.json` in the app's verse shape:
   `{id,tid,tn,ch,cn,vn,complete:true,roman(=iast),dev,iast,en,scripts:{ml,ta,te,kn}}`
   and flip that text's `complete` flag to true (with its real verse count).
2. `python3 build/merge_completed.py`
3. `python3 build_app.py --template app_tpl.html --data app_data.json --out app.html`
4. `python3 verify_pipeline.py --live`
5. Deploy app.html (rename to index.html).
(If you prefer, have the app fetch app_data.json at runtime instead of inlining - fine
for a hosted site, avoids the ~2.2MB single file.)

## Sourcing notes (targets with clean Devanagari)
- sanskritdocuments.org - Upanishads, all major stotras (Vishnu/Lalita Sahasranama,
  Soundarya Lahari, Hanuman Chalisa), Narayaneeyam. Best starting point.
- GRETIL (gretil.sub.uni-goettingen.de) - critical editions incl. the FULL Ramayana
  and Mahabharata, verse by verse.
- bhagavata.org - complete Srimad Bhagavatam by canto.
Always confirm licensing of any English translation you bundle (public-domain Swami
translations are safe; some modern ones are not).

## Scope decisions already made by the owner
- Complete coverage per text, all chapters/verses, no gaps ("shouldn't be half done").
- Accepts this is a phased, multi-week content project across all 16 texts.
- **Ramayana & Mahabharata: EVERY single verse** (owner accepts months-long ingestion),
  not just core verses per chapter. Run these in chapter/parva batches; the gap gate
  guarantees each batch is whole. Source from the GRETIL critical editions.

## Tiers (rough effort order)
- Tier 1 (short, one loader each): Hanuman Chalisa, Vishnu Sahasranama, Lalita
  Sahasranama, Soundarya Lahari, Narayaneeyam, principal Upanishads.
- Tier 2 (large but bounded): Devi Mahatmyam (~700), Yoga Sutras (~196),
  Vivekachudamani (~580), Purana selections, Adhyatma Ramayanam.
- Tier 3 (every verse, batched): Ramayana (~24,000), Mahabharata (~100,000).

## App features already built (don't rebuild)
Four modes: Today (verse+saying of day), Begin (guided beginner path), Explore
(multi-script search + chapter navigation + pagination + bookmarks + copy), Meditate
(silent drifting-word window). Reading-size control, About/roadmap, localStorage
bookmarks (guarded), mobile-responsive, accessible. Design: palm-leaf/manuscript
aesthetic (leaf #e8dcc0, vermilion #b6321f, gold #9a7526; Cormorant Garamond + Spectral
+ IBM Plex Mono).

## Monetisation (open, for later)
Free hook = meditation window + daily verse + beginner path. Paid tier = complete
multi-script texts + deeper study features. The owner hasn't fixed the model yet
(donations / one-off unlock / subscription).
