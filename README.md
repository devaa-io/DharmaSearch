# DharmaSearch

Search and study Hindu scripture in one place. DharmaSearch serves verses from texts such as the Bhagavad Gita and the Upanishads, with AI-assisted search and explanations, audio playback, bookmarks, reading plans and personal annotations.

"Dharma protects those who protect dharma."

## Features

- 16 sacred texts with 264 seeded verses, including Kerala-specific texts, browsable by text, chapter and verse
- Keyword search ranked by relevance, plus AI search in plain language and per-verse AI explanations
- Transliterations in Malayalam, Hindi, Tamil, Telugu and Kannada
- Audio recitation through text-to-speech, with multiple voices and caching
- Six reading plans with progress tracking, including a Karkkidakam 30-day Ramayana plan
- Bookmarks, copy, share, and share-as-image with selectable themes
- Community annotations with guru tradition tags and upvoting
- Corrections workflow: users submit, an admin approves, the fix auto-applies
- Daily verse endpoint, and a public sample search that works without an account
- Account system with JWT access and refresh tokens (httpOnly cookie or bearer)

## Stack

| Layer    | Tech |
|----------|------|
| Backend  | FastAPI, Motor (async MongoDB), PyJWT, bcrypt |
| Frontend | React |
| Database | MongoDB |

## Getting started

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:

```
MONGO_URL=mongodb://localhost:27017
DB_NAME=dharmasearch
JWT_SECRET=change-me
EMERGENT_LLM_KEY=your-key        # powers AI search, explanations and TTS
ADMIN_EMAIL=you@example.com      # admin account for the corrections workflow
ADMIN_PASSWORD=change-me
```

The AI features go through the `emergentintegrations` client; without `EMERGENT_LLM_KEY` the core search and reading features still work.

Run it:

```bash
uvicorn server:app --reload --port 8001
```

### Frontend

```bash
cd frontend
yarn install
yarn start
```

## API overview

All routes are prefixed with `/api`.

| Area | Routes |
|------|--------|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/logout`, `/auth/refresh`, `GET /auth/me` |
| Public | `GET /public/sample-verses`, `GET /public/search` |
| Scriptures | `GET /scriptures`, `/scriptures/{text}/chapters`, `/scriptures/{text}/chapters/{n}/verses`, `/scriptures/{text}/verses/{id}` |
| Study | `GET /search`, `POST /ai-search`, `POST /ai-explain`, `POST /tts`, `GET /daily-verse` |
| Personal | Bookmarks, plans and annotations CRUD |

## Status

Working prototype with seeded scripture data in `backend/scripture_data.py`. Expanding text coverage and refining the AI explanations are the current focus.
