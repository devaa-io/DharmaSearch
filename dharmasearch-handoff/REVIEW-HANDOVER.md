# DharmaSearch scripture pipeline — peer-review handover for Codex

**Author:** Claude (Sonnet/Opus sessions, 2026-07-18 → 2026-07-20)
**Branch:** `dharmasearch-scripture-pipeline`
**Reviewer:** Codex

## Why this exists
This directory is the content pipeline that supplements DharmaSearch (the FastAPI +
React + Mongo app in `backend/` and `frontend/`). It ingests Hindu scripture from
authoritative online sources into the app's data payload. Read `CLAUDE.md` in this
directory first — it defines the two hard rules that govern every decision here:

1. **No text ships half done.** Every verse must carry all 7 fields: `dev` (Devanagari),
   `iast`, `en` (English), and the four southern scripts `ml`/`ta`/`te`/`kn`.
   `ingest_pipeline.py`'s gap gate exits non-zero if any field is empty. `--allow-gaps`
   must never be used for a real build.
2. **Transliteration is script-to-script from Devanagari only.** `ml/ta/te/kn` and `iast`
   are generated *by the pipeline* from clean Unicode Devanagari — never from romanised
   ASCII (which is lossy). Loaders must source real Devanagari, and English translations
   must be public-domain / license-cleared.

## What to review
Seven texts were completed end-to-end this session (Bhagavad Gita predates it). Each has
a `loaders/<t>.py`, a `sources/<t>_config.json`, a `data/<t>.json` output, and a merged
entry in `app_data.json` (rebuilt into `app.html`).

| Text | Verses | Structure | Devanagari source | English (licensing) |
|------|-------:|-----------|-------------------|---------------------|
| Isha | 18 | flat | sanskritdocuments `iisha.html` | Müller, SBE Vol.1, 1879 — PD (d.1900) |
| Kena | 35 | 4 khandas | sanskritdocuments `kena.html` | Müller, SBE Vol.1 — PD |
| Katha | 120 | 6 vallis | sanskritdocuments `katha.html` | Müller, SBE Vol.15, 1884 — PD |
| Mundaka | 64 | 3 mundakas × 2 khandas | sanskritdocuments `mundaka.html` | Müller, SBE Vol.15 — PD |
| Prashna | 67 | 6 prashnas | sanskritdocuments `prashna.html` | Müller, SBE Vol.15 — PD |
| Mandukya | 12 | flat | sanskritdocuments `maandu.html` | Hume, 1921 — PD (pre-1929 US pub) |

Total added this session: **316 verses**. With the Gita (701), `app_data.json` now has
**22 texts, 7 marked `complete:true`, 1358 verses.**

## How to verify (reproducible)
Every dataset can be regenerated from scratch — this is the core review step:

```bash
cd dharmasearch-handoff
pip install --user indic-transliteration requests   # only deps
for t in isha kena katha mundaka prashna mandukya; do
  python ingest_pipeline.py --config sources/${t}_config.json --out /tmp/${t}.json
  # must print "Gaps: 0" and exit 0; then diff /tmp/${t}.json against data/${t}-upanishad.json
done
```
(All loaders fetch live from sanskritdocuments.org + Wikisource, so this needs network.
`sanskritdocuments.org` 406s the default requests UA — loaders send a browser UA.)

`build/merge_*.py` show exactly how each `data/*.json` was merged into `app_data.json`
(idempotent; each backs up before writing and strips prior rows for its `tid`).
`build_app.py` inlines `app_data.json` into `app_tpl.html` → `app.html` and only writes
if the payload is valid JSON.

## Specific things to scrutinise (highest-risk first)
1. **Katha positional alignment** (`loaders/katha.py`, `_fetch_english`). Müller's printed
   verse numbers in Katha valli 3 are non-contiguous (…14, then 18–20 for the same 17
   verses — an edition quirk). The loader aligns English to Devanagari **positionally**
   within each valli rather than by printed number. Verify this assumption holds for all 6
   vallis, not just valli 3 — a wrong count in any valli would silently shift verses.
2. **Mandukya English is manually transcribed** (`loaders/mandukya.py`, `ENGLISH` dict).
   Hume's 1921 text came from archive.org OCR; the 12 verses were hand-cleaned of OCR
   noise. Please diff the dict against the raw scan
   (archive.org `in.ernet.dli.2015.1291`) to confirm no wording drift. This is the only
   text whose English is embedded rather than fetched+parsed live.
3. **Isha appears twice in the app.** The mixed `upanishads` preview grouping still holds
   a low-fidelity Isha preview (`tid=upanishads`, `id=isha-1…`), while the new complete
   `isha-upanishad` text is separate. Non-destructive by design, but a dedupe (remove Isha
   from the preview grouping) is a pending cleanup — flag if you think it should happen now.
4. **`chapterMeta[<tid>]` `dev` fields are empty** for the new texts (only `tr`/`mean`
   populated). The app tolerates this; confirm it doesn't break chapter navigation.
5. **Section-splitting regexes rely on Wikisource's rendered HTML** (e.g. "Khanda" renders
   as "Kha nd a", valli headers as "Vallî"). Loaders normalise these. If Wikisource
   re-renders, a loader could silently under-count — the `!= expected` asserts in each
   `_fetch_*` are the guard; verify those asserts cover every section.

## Blocked / not done — needs a decision
**Vishnu Sahasranama (verse-level): BLOCKED — do not assume it can be finished as-is.**
Devanagari (108 verses, `sanskritdocuments vsahasranew.html`), IAST and 4 scripts are all
clean. The blocker is English: mapping 1000 name-meanings onto the 108 verses.
- The only clean **public-domain** English (Ananthakrishna Sastry, 1927, archive.org
  `in.ernet.dli.2015.1291`) is OCR'd and the OCR corrupts the *names themselves*
  ("Viśva" → `Vi<^va`), defeating automated name→verse alignment. Five matching strategies
  were tried — see `_vsn_review/vsn_align5.py` (final attempt, consonant-skeleton method).
- The one clean *typed* verse-grouped English (GitHub `deerao75/vishnusahasranama`) is
  disqualified twice: **no license** (all-rights-reserved) and its meanings are
  **AI-generated** (Google AI Studio app) — unusable on accuracy + licensing grounds. Its
  Devanagari field is also Kannada-contaminated (43/108 clean).
- **Reviewer input wanted:** is there an authoritative, public-domain, *verse-aligned*
  (not per-name) English VSN source? If not, the realistic options are (a) ship VSN
  name-level (1000 entries) rather than verse-level, or (b) leave it out. It should **not**
  be forced with an unverifiable source.

**Remaining Tier-1 texts (per `CLAUDE.md`), not yet started:** Soundarya Lahari
(Devanagari confirmed present: `doc_devii/saundaryalahari.html`; PD English candidate:
Arthur Avalon/Woodroffe 1916), Lalita Sahasranama (same 1000-name shape/risk as VSN),
Narayaneeyam, Hanuman Chalisa (no confirmable PD English found — flagged earlier).
**Remaining principal Upanishads:** Aitareya (embedded in a larger Aranyaka on Wikisource
— isolate 2.4–2.6), Chandogya (~627v, large), Taittiriya / Svetasvatara / Brihadaranyaka /
Maitrayana (Müller SBE Vol.15 versions are **redlinks** on Wikisource — need a different PD
source, proofread if OCR).

## File inventory
- `loaders/*.py` — one per text, each exposes `load() -> list[dict]`.
- `sources/*_config.json` — field mappings the pipeline consumes.
- `data/*.json` — pipeline outputs (zero-gap datasets).
- `build/merge_*.py` — how each dataset was merged into `app_data.json` (katha/mandukya/
  mundaka/prashna present; isha/kena used the identical pattern, scripts not retained).
- `app_data.json` — merged payload (22 texts, 1358 verses). `app.html` — deployable build.
- `_vsn_review/vsn_align5.py` — evidence of the VSN alignment attempts (exploratory).
- `ingest_pipeline.py`, `build_app.py`, `app_tpl.html` — unchanged pipeline core.
