# DharmaSearch

DharmaSearch is an offline-first scripture reader and multilingual search experience, with optional connected features for accounts, AI-assisted study, audio, reading plans and community notes.

The public React library currently includes 22 text groupings and 1,338 passages. Seven works are complete and release-gated: the Bhagavad Gita plus the Isha, Kena, Katha, Mundaka, Prashna and Mandukya Upanishads. Their 1,017 verified verses include Devanagari, IAST, Malayalam, Tamil, Telugu, Kannada and English.

"Dharma protects those who protect dharma."

## Features

### Public reader

- Offline-first Today, Begin, Explore, Meditate and About views at `/`
- Multilingual search across original text, transliteration, English and southern scripts
- Complete-text and chapter navigation with preview content clearly distinguished
- Local bookmarks, script selection, copyable citations and reading-size controls
- No account, API or database required for public reading

### Optional connected features

- Keyword and AI-assisted search, per-verse explanations and text-to-speech audio
- Six reading plans with progress tracking
- Account-backed bookmarks, community annotations and corrections workflow
- JWT access and refresh tokens using an httpOnly cookie or bearer token

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18, Create React App, CRACO |
| Backend | FastAPI, Motor (async MongoDB), PyJWT, bcrypt |
| Database | MongoDB |
| Content pipeline | Python, deterministic validation and generated JSON |

## Run the public reader

```bash
cd frontend
npm ci
npm start
```

Open <http://localhost:3000>. The public library works without the backend. Set `REACT_APP_BACKEND_URL` only when testing login or connected dashboard features.

## Run the connected backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn server:app --reload --port 8001
```

Review `backend/.env.example` before starting. MongoDB is required for connected features. AI search, explanations and TTS additionally require the configured LLM integration key; core public reading and search remain local.

## Verify a production build

```bash
cd frontend
npm ci
CI=true npm test -- --watchAll=false
npm run build
python3 -m http.server 8765 --directory build
```

Open <http://localhost:8765>. Use the root URL, not `/app.html`; `app.html` belongs to the separate self-contained prototype.

## Rebuild and verify scripture data

```bash
cd dharmasearch-handoff
python3 -m pip install -r requirements.txt
python3 build/merge_completed.py
python3 build_app.py
python3 verify_pipeline.py
python3 -m unittest discover -s tests -v
```

`build_app.py` updates both the standalone `app.html` and the React asset at `frontend/public/scripture-data.json`. For a reproducibility audit against current upstream sources, run `python3 verify_pipeline.py --live`.

## API overview

All backend routes are prefixed with `/api`.

| Area | Routes |
|------|--------|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/logout`, `/auth/refresh`, `GET /auth/me` |
| Public | `GET /public/sample-verses`, `GET /public/search` |
| Scriptures | `GET /scriptures`, `/scriptures/{text}/chapters`, `/scriptures/{text}/chapters/{n}/verses`, `/scriptures/{text}/verses/{id}` |
| Study | `GET /search`, `POST /ai-search`, `/ai-explain`, `/tts`, `GET /daily-verse` |
| Personal | Bookmarks, plans and annotations CRUD |

See [REVIEW-HANDOVER.md](dharmasearch-handoff/REVIEW-HANDOVER.md) for content provenance, review findings and blocked texts.
