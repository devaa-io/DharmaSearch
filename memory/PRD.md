# DharmaSearch - Hindu Scripture Quote Finder (Publish-Ready)

## Architecture
- Frontend: React + Tailwind + shadcn/ui, sidebar dashboard
- Backend: FastAPI + MongoDB + emergentintegrations (GPT-5.2 + TTS-1-HD)
- Auth: JWT httpOnly cookies
- Data: 264 verses, 16 texts, 6 reading plans

## All Features
- [x] JWT auth, keyword + AI search, AI explanations
- [x] 16 sacred texts (9 general + 7 Kerala-specific)
- [x] 264 verses with multi-word search ranked by relevance
- [x] Browse by text/chapter/verse with verse counts
- [x] 5 Indian language transliterations: Malayalam, Hindi, Tamil, Telugu, Kannada
- [x] Temple connections to Kerala temples
- [x] Bookmark, copy, share, share as image (4 themes)
- [x] 6 reading plans incl. Karkkidakam 30-day Ramayana
- [x] Audio recitation (TTS-1-HD, 6 voices, cached)
- [x] Community annotations with guru tradition tags + upvoting
- [x] Corrections/feedback (user submit -> admin approve -> auto-apply)
- [x] Interactive landing page with public search preview
- [x] Daily verse of the day

## Pending: EMERGENT_LLM_KEY activation for AI Search, AI Explain, TTS
