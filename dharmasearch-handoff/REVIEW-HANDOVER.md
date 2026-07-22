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
**22 text entries, 7 marked `complete:true`, and 1,338 verse rows.** The row count is
20 lower than the original handover because duplicate previews of now-complete
Upanishads were removed during review.

## How to verify (reproducible)
Every dataset can be regenerated from scratch — this is the core review step:

```bash
cd dharmasearch-handoff
python3 -m pip install --user indic-transliteration requests   # only deps
for t in isha kena katha mundaka prashna mandukya; do
  python3 ingest_pipeline.py --config sources/${t}_config.json --out /tmp/${t}.json
  # must print "Gaps: 0" and exit 0; then diff /tmp/${t}.json against data/${t}-upanishad.json
done
```
(All loaders fetch live from sanskritdocuments.org + Wikisource, so this needs network.
`sanskritdocuments.org` 406s the default requests UA — loaders send a browser UA.)

`build/merge_completed.py` reproducibly synchronizes all seven completed texts from
their canonical datasets; its Upanishad step removes duplicate rows from the legacy
mixed preview.
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
   (archive.org `thirteenprincipa028442mbp`, pp. 391–393) to confirm no wording drift. This is the only
   text whose English is embedded rather than fetched+parsed live.
3. **Duplicate previews (resolved).** The mixed `upanishads` grouping contained previews
   of five now-complete texts, not only Isha. Review removed all 20 duplicate rows while
   retaining previews for Brihadaranyaka, Chandogya, and Taittiriya.
4. **`chapterMeta[<tid>]` `dev` fields are empty** for most new texts (only `tr`/`mean`
   populated). Review confirmed this does not break chapter navigation.
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
- `build/merge_completed.py` — portable, idempotent merger for every completed text;
  validates required fields/counts, synchronizes canonical representations, and removes
  duplicate Upanishad preview rows.
- `app_data.json` — merged payload (22 text entries, 1,338 verse rows). `app.html` — deployable build.
- `_vsn_review/vsn_align5.py` — evidence of the VSN alignment attempts (exploratory).
- `ingest_pipeline.py`, `build_app.py`, `app_tpl.html` — pipeline and static-app core.

## Codex review outcome (2026-07-20)
- Regenerated all six datasets from the live sources with `python3`; every build had
  zero gaps and matched its committed `data/*.json` byte-for-byte.
- Verified Katha's printed numbering in every valli. Vallis 1/2/4/5/6 are contiguous;
  valli 3 alone reads 1–14, 18–20. The loader now asserts that exact sequence before
  applying positional alignment.
- Compared all 12 Mandukya translations with Hume's scan on pp. 391–393. No wording
  drift was found; the handover's former Archive.org identifier pointed to the unrelated
  1927 Vishnu Sahasranama scan and has been corrected above.
- Confirmed empty `chapterMeta.dev` values do not affect navigation: the UI renders
  `tr` and `mean`, and derives selectable chapters from verse rows.
- Added HTTP status checks to every loader. Added a portable all-Upanishads merger and
  removed duplicate preview rows for Isha, Kena, Katha, Mundaka, and Mandukya. The app
  payload now contains 22 text entries and 1,338 verse rows (7 complete texts).
- Added shared dataset/app validation, atomic generated-file writes, safe JSON embedding,
  current-directory-independent loader resolution, regression tests, an offline verifier,
  opt-in live-source comparison, and GitHub Actions coverage for deterministic checks.
- The stronger verifier found the Gita app's generated southern-script rows had ASCII
  periods where the canonical dataset retained danda punctuation. The completed-text
  merger now synchronizes all seven datasets exactly, and the app payload was corrected.
- Product/UI review changed complete verses to lead with Devanagari, restricted daily and
  meditation content to verified rows, made Explore complete-first with explicit filters
  and text context, clarified bookmark/copy actions, improved responsive navigation and
  touch targets, added hash/back navigation, and strengthened script typography.
- Content rendering review found Wikisource inline HTML was splitting transliterated names
  (for example `Nakiketas` → `Na k iketas`) and final-page material was leaking into five
  translations. A block-aware parser now preserves inline words, drops style/script/
  footnote markup, applies explicit end boundaries, and rejects contaminated or implausibly
  long English during validation. The five affected datasets and app payload were rebuilt.
- Vishnu Sahasranama remains blocked. No verified public-domain verse-aligned English
  source was established during review, so neither the unlicensed AI-generated source
  nor uncertain OCR alignment should ship.
