# Verse deep-links

2026-07-30. Approved by Devan ("continue as you see best fit") after design
discussion. Chosen direction: focused verse page as the link target, with
one-tap continuation into chapter context ("Both" option).

## Problem

No verse in the app has a stable address. Hash routing covers views (#read)
but not positions, so a verse someone loved cannot be linked, shared, or
returned to except by scrolling. This is both a reader-experience gap and the
missing foundation for any future sharing/SEO work.

## Design

### Route and page

- New route `/v/:verseId` in App.js.
- `VersePage` loads data via the existing `useScriptureData`, looks the verse
  up by id in a `versesById` map. Verse ids are opaque strings; never parsed,
  only looked up.
- Found: a context line (text name, chapter name), the full
  `ScriptureVerseCard` with the same shared props ScriptureLibraryPage wires
  (bookmarks, copy toast, audio), and two actions: "Read this chapter" and
  "Copy link".
- Unknown id: a gentle not-found state linking to the library. No error tone.
- Data loading and load-failure states mirror ScriptureLibraryPage's.

### Continue into context

- "Read this chapter" writes `{tid, ch}` to `ds_reading` (the exact resume
  mechanism ReadView already uses), sets a one-shot sessionStorage key
  `ds_jump` = verseId, and navigates to `/#read`.
- ReadView on mount consumes `ds_jump` (read + remove): opens that position
  directly instead of the catalogue, scrolls to the verse element, applies a
  brief highlight that fades. Momentum, not alarm.
- Verse elements in ReadView get `id` anchors derived from verse id.

### Sharing from anywhere

- `ScriptureVerseCard` gains a share action beside copy/bookmark: builds
  `${origin}/v/${verse.id}`, uses the Web Share API when available, clipboard
  otherwise, and reports through the card's existing toast channel.

### Read-marking

- The focused verse page marks the verse read via the shared
  `useMarkVisibleAsRead`, consistent with Feed and Read.

## Constraints honoured

- Momentum, never pressure: no counters or prompts added to the verse page.
- Privacy: no tracking; everything remains on-device.
- Netlify SPA redirect already serves any path; no config change needed.
- Stacked on `feat/chapter-progress` (PR #9) because it reuses that branch's
  shared hook and ReadView wiring.

## Testing

- Route renders a known verse's card.
- Unknown id shows the not-found state.
- Share action produces the expected URL.
- `ds_jump` consumption opens the right chapter in ReadView.
- No existing test modified.

## Rejected alternatives

- Hash-only `#v/...` routing: cheaper now, dead end for OG/SEO, fiddly
  back-button semantics with two hash meanings.
- Netlify prerendering for per-verse OG tags now: separate project; build it
  once links exist and are actually being shared.
