# DharmaSearch

DharmaSearch is an offline-first scripture reader and multilingual search experience, with optional connected features for accounts, audio, explanations, reading plans and community notes.

The public React app currently includes 22 text entries and 1,338 passages. Seven works are complete and release-gated: the Bhagavad Gita plus the Isha, Kena, Katha, Mundaka, Prashna and Mandukya Upanishads. Their 1,017 verses include Devanagari, IAST, Malayalam, Tamil, Telugu, Kannada and English.

## Run the app

```bash
cd frontend
npm install
npm start
```

Open <http://localhost:3000>. The public library works without the backend. Set `REACT_APP_BACKEND_URL` and run the FastAPI/Mongo service only when testing login or connected dashboard features.

## Verify a production build

```bash
cd frontend
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

See [REVIEW-HANDOVER.md](dharmasearch-handoff/REVIEW-HANDOVER.md) for provenance, review findings and blocked texts.
