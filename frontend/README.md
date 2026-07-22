# DharmaSearch React frontend

The root route is the verified, offline-first scripture library. Login, registration and the older connected dashboard remain available at `/login`, `/register` and `/dashboard`.

## Development

```bash
npm ci
npm start
```

Open <http://localhost:3000>. The public route reads `public/scripture-data.json`, so it does not need FastAPI or MongoDB. Configure `REACT_APP_BACKEND_URL` to exercise connected routes.

## Production check

```bash
npm ci
npm run build
python3 -m http.server 8765 --directory build
```

Open <http://localhost:8765>. If that port is busy, choose another one.

Run the non-watch smoke test used by CI with:

```bash
CI=true npm test -- --watchAll=false
```

## Responsive production verification

On 2026-07-22, the production build was served locally and checked with automated Chromium at a 900 CSS-pixel viewport height. At each exact width the public reader rendered, the browser reported zero console errors, and the document had no horizontal overflow:

| Width | Client width | Scroll width | Reader rendered | Console errors |
| ---: | ---: | ---: | :---: | ---: |
| 375 | 375 | 375 | Yes | 0 |
| 768 | 768 | 768 | Yes | 0 |
| 1024 | 1024 | 1024 | Yes | 0 |
| 1440 | 1440 | 1440 | Yes | 0 |

The same pass also verified English search (`royal secret`), Malayalam search (`രാജവിദ്യാ`) with automatic display and highlighting of the matching Malayalam script, manual script switching until the query changes, hash navigation, bookmark persistence, Begin-path progress, and meditation-dialog focus entry, Escape dismissal and focus restoration.

Do not edit `public/scripture-data.json` by hand. Rebuild it from the validated source payload:

```bash
cd ../dharmasearch-handoff
python3 build_app.py
python3 verify_pipeline.py
```
