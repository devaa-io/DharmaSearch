# UX modernization pass

2026-07-30. Owner's framing: the live site "feels very 90s... not modern or
for the modern user." Reviewed every main view at desktop and mobile widths
before diagnosing. Owner authorized implementation directly ("fix the bugs
and do the spec as you think best fit") rather than a further design
back-and-forth.

## What's actually dated, and why

The palm-leaf/manuscript aesthetic itself (warm parchment, Cormorant
Garamond, vermilion/gold) is not the problem and is not being changed. Five
concrete, structural things are:

1. **Mobile nav cuts off mid-word with no affordance.** `.library-nav` is
   already `overflow-x: auto`, correctly scrollable - but nothing hints that.
   A user sees "RE" truncated at the edge and reads it as broken.
2. **Chapter picker is 3 rows of chrome before any scripture.** 18 identical
   bordered boxes, `flex-wrap: wrap`, all equal visual weight, no distinction
   for read/unread/current beyond the active one.
3. **No depth.** `--shadow` exists (`0 12px 34px rgba(66,45,23,0.09)`) but at
   9% opacity against a cream background it reads as flat. Every surface -
   nav item, card, pill, button - is a hairline border with no elevation
   hierarchy, so nothing signals which surface sits "above" another.
4. **Motion exists but is minimal.** One `library-fade` (350ms opacity+
   translateY) fires on the whole view container on switch. No staggered
   reveal, no per-item entrance, nothing on scroll.
5. **Script-switcher visual weight.** 7 equal-weight bordered boxes per verse
   card (English/Devanagari/IAST/Malayalam/Tamil/Telugu/Kannada), spelled out
   in full, repeated on every card down the page.

## Fixes

### 1. Scroll-fade affordance (bug fix)
A CSS `mask-image` gradient on any horizontally-scrolling row, fading the
trailing ~32px to transparent when there's more to scroll. Pure CSS, no JS.
Applied to `.library-nav` (mobile) and the picker rows once they scroll
(below).

### 2. Chapter picker -> single-row horizontal strip
`flex-wrap: wrap` -> `flex-wrap: nowrap; overflow-x: auto` with the same
fade-mask. Collapses ~3 rows to one compact row without inventing a new
interaction (still every chapter, still one tap away, still visually
consistent with the rest of the app's "row of chips" language). Button
styling unchanged.

### 3. Depth
- `--shadow` opacity raised from the current low value to something actually
  perceptible against `--card`/`--leaf`, plus a second, tighter shadow layer
  for a resting-elevation look specifically on `.scripture-card` and
  `.text-card`/`.collection-card` (ambient + contact shadow, not just one
  soft blur).
- The all-around 1px border on `.scripture-card` is dropped in favour of the
  shadow doing that job; the colored left-edge accent (vermilion/gold) stays
  - it's a genuine signature, not generic chrome, so it's kept and slightly
  reinforced now that the surrounding border is gone.
- Icon buttons (`bookmark`, `copy`, `share`) get a hover lift (translateY +
  shadow) instead of only a border-color change.

### 4. One staggered entrance, CSS-only
Card grids (`.collection-grid`, `.text-grid`, `.feed-stack`, chapter verse
lists) get a per-item fade+rise on mount, staggered via `nth-child`
`animation-delay` up to a cap (~8 items get distinct delays, the rest share
the last one, so a 47-verse chapter doesn't make the reader wait). Reuses the
existing `library-fade` keyframe shape (opacity+translateY), doesn't
introduce a new motion language. Respects `prefers-reduced-motion` via the
same media query pattern already used elsewhere in this file.

### 5. Script-switcher: lighter, not smaller
Kept as full labels (removing them would hurt findability for someone
looking for their specific script) but reduced the resting visual weight:
lighter border colour and background tint for inactive buttons, tighter
padding, so the active selection reads clearly as the one heavy element in
the row instead of seven equal boxes.

## What isn't changing
- No new fonts, no palette change, no layout restructuring beyond the
  chapter-picker row collapse. This is a refinement pass, not a redesign -
  the manuscript aesthetic is the identity, not the problem.
- No interaction paradigm changes (no dropdowns replacing chip rows, no
  bottom tab bar replacing the top nav) - lower risk, addresses the actual
  complaints (broken affordance, flatness, no motion, chrome-heavy chapter
  nav) without a rebuild.

## Verification
Browser-checked at 375/1440 after implementation: scroll-fade visible and
functional, chapter picker single-row, cards show visible elevation, entrance
animation runs and respects reduced-motion, script-switcher is legible with
one clear active state. Existing test suite must still pass unmodified.
