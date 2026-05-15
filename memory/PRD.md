# DharmaSearch - Hindu Scripture Quote Finder

## Architecture
- Frontend: React + Tailwind + shadcn/ui, sidebar dashboard
- Backend: FastAPI + MongoDB + emergentintegrations (GPT-5.2)
- Auth: JWT httpOnly cookies
- Data: 208 verses, 16 texts, 6 reading plans

## 16 Sacred Texts
Bhagavad Gita, Ramayana, Devi Mahatmyam, Upanishads, Yoga Sutras, Mahabharata, Vedas, Hanuman Chalisa, Puranas, Srimad Bhagavatam, Narayaneeyam, Adhyatma Ramayanam, Lalita Sahasranama, Vishnu Sahasranama, Soundarya Lahari, Vivekachudamani

## All Features
- [x] JWT auth, keyword + AI search, AI explanations
- [x] Browse 16 texts by text/chapter/verse
- [x] Bookmark, copy, share, share as image (4 themes)
- [x] Daily verse of the day
- [x] 6 reading plans including Karkkidakam 30-day Ramayana
- [x] Custom reading plan creation + progress tracking
- [x] Malayalam & Hindi transliteration for Kerala texts
- [x] Temple connections (Guruvayur, Padmanabhaswamy, Sabarimala, etc.)
- [x] Interactive landing page with public search preview
- [x] Sample verse cards expandable without signup

## Known Issues
- EMERGENT_LLM_KEY needs balance for AI features

## Backlog
P0: Activate LLM key | P1: Expand verses, add Tamil/Telugu/Kannada | P2: Dark mode, TTS, community
