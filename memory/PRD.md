# DharmaSearch - Hindu Scripture Quote Finder

## Problem Statement
Find and pinpoint quotes from Hindu sacred texts. Expanded to 16 texts with Kerala-specific scriptures, reading plans, transliteration, and temple connections.

## Architecture
- Frontend: React + Tailwind CSS + shadcn/ui, sidebar dashboard
- Backend: FastAPI + MongoDB + emergentintegrations (OpenAI GPT-5.2)
- Auth: JWT httpOnly cookies
- Data: 208 curated verses across 16 sacred texts, 5 reading plans

## 16 Sacred Texts
### Original 9
1. Bhagavad Gita (18 ch) 2. Ramayana (7 Kandas) 3. Devi Mahatmyam (13 ch) 4. Upanishads (8 texts) 5. Yoga Sutras (4 Padas) 6. Mahabharata (5 Parvas) 7. Vedas (4 Vedas) 8. Hanuman Chalisa 9. Puranas (4 texts)

### Kerala-specific 7 (new in iteration 3)
10. Srimad Bhagavatam 11. Narayaneeyam 12. Adhyatma Ramayanam 13. Lalita Sahasranama 14. Vishnu Sahasranama 15. Soundarya Lahari 16. Vivekachudamani

## Features Implemented
- [x] JWT auth, keyword search, AI search (GPT-5.2), AI explanations
- [x] Browse 16 texts by text/chapter/verse
- [x] Bookmark, copy, share quotes
- [x] Share as Image (4 themes: Dark, Light, Night, Parchment)
- [x] Daily verse of the day
- [x] 5 pre-built reading plans (7 Days of Gita, Upanishad Intro, Kerala Devotion, Yoga Path, Divine Feminine)
- [x] Custom reading plan creation
- [x] Plan progress tracking (mark days complete)
- [x] Malayalam & Hindi transliteration for Kerala texts
- [x] Temple connections (Guruvayur, Padmanabhaswamy, Sabarimala, Chottanikkara, etc.)
- [x] Sidebar dashboard layout, asymmetric landing page

## Known Issues
- EMERGENT_LLM_KEY needs balance for AI features

## Backlog
### P0 - Activate LLM key for AI features
### P1 - Expand verse database, add Tamil/Telugu/Kannada transliterations
### P2 - Dark mode, audio (TTS), community annotations, email reminders for plans
