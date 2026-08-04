# DharmaSearch - context for Claude Code

Read this first. It captures where the project is and the rules that must not be broken.

## What this is
A Hindu-scripture reading and study app, given away free (owner decision,
2026-07-31). See the free-app section below before adding anything that earns.
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
- **Thirteen texts are COMPLETE (3,495 verses):** Bhagavad Gita (701); Isha, Kena,
  Katha, Mundaka, Prashna and Mandukya Upanishads (316); Vishnu Sahasranama
  (108), Soundarya Lahari (100), Lalita Sahasranama (1000), Hanuman Chalisa
  (42), Narayaneeyam (1033), and Patanjali's Yoga Sutras (195). Every completed row has all seven
  representations and passes the zero-gap gate.
- **The other 9 text groupings are PREVIEW only** - small seeded samples from the
  original `content-export/`, marked "preview" in the app. Completed Upanishads are
  removed from the legacy mixed `upanishads` preview to avoid duplicate search results.

## THIS IS A FREE APP, and four texts depend on it staying that way
Owner decision, 2026-07-31: DharmaSearch is free. No paid tier, no adverts,
nothing sold. That is not a preference, it is the legal basis on which four of
the twelve texts ship.

Soundarya Lahari, Lalita Sahasranama, Hanuman Chalisa and Narayaneeyam draw
their Devanagari from sanskritdocuments.org, whose per-file terms read: "to be
used for personal study and research. The file is not to be copied or reposted
for promotion of any website or individuals or for commercial purpose without
permission." A free reader is neither commercial use nor promotion of a
website, and is squarely the personal study and research they permit.

**If anyone ever adds a paid tier or adverts, those four must come out**, or be
re-sourced, or be used with written permission. Ads count as commercial.

- Sources are credited in the app's About view (`AboutView.js`, `.sources`).
  Keep that current. It is both the decent thing and part of why this is fine.
- Vishnu Sahasranama does not depend on this: it is Swami Krishnananda / The
  Divine Life Society end to end and never touched sanskritdocuments.
- **Sanskrit Wikisource is not a drop-in replacement**, if anyone tries to
  remove the dependency that way. Checked properly on 2026-07-31: its
  Narayaneeyam has 1,028 verses to our 1,033, six cantos differ in length, and
  even among equal-length cantos 566 of 971 verses differ in wording. It is a
  different recension. Its Lalita has no verse numbers at all and is the
  stotram rather than the namavali; its Soundarya Lahari is a scanned-PDF
  transclusion; Hanuman Chalisa is absent entirely.
- **Verse numbering follows the source tradition, not our parsing convenience.**
  Hanuman Chalisa keeps its 2 dohas in section 1 and its 40 chaupais numbered
  1-40 in section 2, so any verse can be cited against a printed edition. Where
  a translation covers two verses at once, both keep their own number and share
  the translation with an inline note; never collapse verses to match a source's
  formatting.

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
- Tier 1 (short, one loader each): DONE - Hanuman Chalisa, Vishnu Sahasranama, Lalita
  Sahasranama, Soundarya Lahari, Narayaneeyam, principal Upanishads.
- Tier 2 (large but bounded): DONE - Yoga Sutras (195). Remaining: Devi
  Mahatmyam (~700), Vivekachudamani (~580), Purana selections, Adhyatma Ramayanam.
- Tier 3 (every verse, batched): Ramayana (~24,000), Mahabharata (~100,000).

## App features already built (don't rebuild)
Four modes: Today (verse+saying of day), Begin (guided beginner path), Explore
(multi-script search + chapter navigation + pagination + bookmarks + copy), Meditate
(silent drifting-word window). Reading-size control, About/roadmap, localStorage
bookmarks (guarded), mobile-responsive, accessible. Design: palm-leaf/manuscript
aesthetic (leaf #e8dcc0, vermilion #b6321f, gold #9a7526; Cormorant Garamond + Spectral
+ IBM Plex Mono).

## Monetisation: SETTLED, and the answer is no
Superseded 2026-07-31. There is no paid tier, no free/paid split, and no ads.
The whole library is free, including the complete multi-script texts that an
earlier draft of this file had earmarked as the paid tier.

Do not reintroduce a paywall or ads without re-reading the free-app section
above: four of the twelve texts ship on the basis that this app is
non-commercial, and adding either would put them in breach.
