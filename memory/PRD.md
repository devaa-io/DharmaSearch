# DharmaSearch - Hindu Scripture Quote Finder

## Problem Statement
Create an app that allows users to find and pinpoint quotes or scriptures from Hindu texts including the Ramayana, Bhagavad Gita, and Devi Mahatmyam.

## Architecture
- **Frontend**: React + Tailwind CSS + shadcn/ui components
- **Backend**: FastAPI + MongoDB + emergentintegrations (OpenAI GPT-5.2)
- **Auth**: JWT httpOnly cookies (register, login, logout, refresh)
- **Data**: 107 curated verses across 3 sacred texts

## User Personas
1. **Spiritual Seeker**: Searches for verses about specific topics (duty, dharma, soul)
2. **Student of Hinduism**: Browses texts chapter by chapter for structured study
3. **Casual User**: Gets daily inspiration from Verse of the Day

## Core Requirements
- [x] JWT authentication (register/login/logout)
- [x] Scripture database: Bhagavad Gita (18 chapters), Ramayana (7 Kandas), Devi Mahatmyam (13 chapters)
- [x] Keyword search across all texts
- [x] AI-powered semantic search (GPT-5.2)
- [x] AI verse explanations (GPT-5.2)
- [x] Browse by text > chapter > verse
- [x] Bookmark/save favorite verses
- [x] Copy & share verse quotes
- [x] Daily verse (deterministic by date)
- [x] Beautiful, reverent UI with Cormorant Garamond & Manrope fonts

## What's Been Implemented (May 15, 2026)
- Full backend with auth, scripture CRUD, search, AI endpoints
- 107 seeded verses across 3 texts
- Landing page with hero section and features
- Auth pages (login/register)
- Dashboard with 4 tabs: Daily Verse, AI Search, Browse Texts, Saved
- Verse cards with bookmark, copy, share, AI explain
- Error handling for AI services (graceful 503)

## Known Issues
- EMERGENT_LLM_KEY needs balance top-up for AI features to work

## Prioritized Backlog
### P0 (Critical)
- Ensure LLM key is active for AI search & explain

### P1 (High)
- Add more verses to the database (expand to 500+ per text)
- Add text search index optimization

### P2 (Nice to have)
- Password reset flow
- User profile page
- Social sharing with OG image cards
- Verse audio (TTS)
- Dark mode
- Sanskrit transliteration toggle
