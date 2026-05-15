# DharmaSearch - Hindu Scripture Quote Finder

## Problem Statement
Create an app to find and pinpoint quotes from Hindu sacred texts including Ramayana, Bhagavad Gita, Devi Mahatmyam, and all major Hindu scriptures.

## Architecture
- **Frontend**: React + Tailwind CSS + shadcn/ui, sidebar dashboard layout
- **Backend**: FastAPI + MongoDB + emergentintegrations (OpenAI GPT-5.2)
- **Auth**: JWT httpOnly cookies
- **Data**: 180 curated verses across 9 sacred texts

## What's Been Implemented (May 15, 2026)

### Iteration 1 - MVP
- JWT auth (register/login/logout)
- 3 texts: Bhagavad Gita, Ramayana, Devi Mahatmyam (107 verses)
- Keyword search, AI search, AI explanations
- Browse by text/chapter/verse
- Bookmarks, daily verse, copy/share

### Iteration 2 - UI Overhaul & Expansion
- Added 6 more texts: Upanishads, Yoga Sutras, Mahabharata, Vedas, Hanuman Chalisa, Puranas (180 verses total)
- Complete UI overhaul: asymmetric landing page, sidebar dashboard, cleaner verse cards
- Share as Image feature with 4 themes (Dark, Light, Night, Parchment)
- Canvas-based image generation for social sharing
- Better error handling for AI features (graceful 503)
- Default to keyword search while AI key is inactive

## 9 Sacred Texts
1. Bhagavad Gita (18 chapters)
2. Ramayana (7 Kandas)
3. Devi Mahatmyam (13 chapters)
4. Upanishads (8 texts: Isha, Kena, Katha, Mundaka, Mandukya, Chandogya, Brihadaranyaka, Taittiriya)
5. Yoga Sutras of Patanjali (4 Padas)
6. Mahabharata (5 Parvas)
7. Vedas (4 Vedas: Rig, Yajur, Sama, Atharva)
8. Hanuman Chalisa (40 verses)
9. Puranas (4 texts: Vishnu, Shiva, Bhagavata, Garuda)

## Known Issues
- EMERGENT_LLM_KEY needs balance for AI search & explanations

## Backlog
### P0 - Activate LLM key for AI features
### P1 - Expand verse database to 500+ per text, add Thirukkural
### P2 - Dark mode, audio (TTS), community annotations
