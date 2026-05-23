# DharmaSearch - Hindu Scripture Quote Finder

## Architecture
- Frontend: React + Tailwind + shadcn/ui, sidebar dashboard
- Backend: FastAPI + MongoDB + emergentintegrations (GPT-5.2 + TTS-1-HD)
- Auth: JWT httpOnly cookies
- Data: 208 verses, 16 texts, 6 reading plans

## All Features
- [x] JWT auth, keyword + AI search, AI explanations
- [x] 16 sacred texts including 7 Kerala-specific
- [x] Browse by text/chapter/verse, daily verse
- [x] Bookmark, copy, share, share as image (4 themes)
- [x] 6 reading plans incl. Karkkidakam 30-day Ramayana
- [x] Custom plan creation + progress tracking
- [x] Malayalam & Hindi transliteration for Kerala texts
- [x] Temple connections (Guruvayur, Padmanabhaswamy, Sabarimala, etc.)
- [x] Interactive landing page with public search preview
- [x] Community annotations with guru tradition tags + upvoting
- [x] Correction/feedback system (user submit -> admin approve -> auto-apply)
- [x] Audio recitation (TTS-1-HD) with 6 voice options + caching

## Known Issues
- EMERGENT_LLM_KEY top-up may need time to propagate (AI + TTS features return graceful 503 until active)
