# DharmaSearch

Search and study Hindu scripture in one place. DharmaSearch serves verses from texts such as the Bhagavad Gita and the Upanishads, with AI-assisted search and explanations, audio playback, bookmarks, reading plans and personal annotations.

"Dharma protects those who protect dharma."

## Features

- Full-text verse search, plus a public sample search that works without an account
- AI search: ask a question in plain language and get relevant verses
- AI explain: request a plain-language explanation of any verse
- Text-to-speech playback for verses
- Daily verse endpoint
- Bookmarks, reading plans with progress tracking, and per-verse annotations
- Account system with JWT access and refresh tokens (cookie or bearer)

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
```

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
