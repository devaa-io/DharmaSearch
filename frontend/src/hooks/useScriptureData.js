import { useEffect, useState } from 'react';

let scriptureDataPromise;

function loadScriptureData() {
  if (!scriptureDataPromise) {
    const base = process.env.PUBLIC_URL || '';
    scriptureDataPromise = fetch(`${base}/scripture-data.json`).then(async response => {
      if (!response.ok) {
        throw new Error(`Scripture library returned HTTP ${response.status}`);
      }
      const payload = await response.json();
      if (!Array.isArray(payload.texts) || !Array.isArray(payload.verses)) {
        throw new Error('Scripture library has an invalid shape');
      }
      return payload;
    });
  }
  return scriptureDataPromise;
}

export function useScriptureData() {
  const [state, setState] = useState({ data: null, error: null });

  useEffect(() => {
    let active = true;
    loadScriptureData().then(
      data => active && setState({ data, error: null }),
      error => active && setState({ data: null, error }),
    );
    return () => { active = false; };
  }, []);

  return state;
}
