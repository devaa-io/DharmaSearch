import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

const MANIFEST_URL = '/audio-manifest.json';

function pairKey(verseId, script) {
  return `${verseId}:${script}`;
}

export function useStaticAudio() {
  const [clips, setClips] = useState([]);
  const activeRef = useRef(null);

  useEffect(() => {
    let active = true;
    fetch(MANIFEST_URL, { cache: 'no-cache' })
      .then(response => {
        if (!response.ok) throw new Error(`audio manifest returned ${response.status}`);
        return response.json();
      })
      .then(manifest => {
        if (active) setClips(Array.isArray(manifest.clips) ? manifest.clips : []);
      })
      .catch(() => {
        if (active) setClips([]);
      });
    return () => {
      active = false;
      activeRef.current?.stop();
    };
  }, []);

  const clipByPair = useMemo(
    () => new Map(clips.map(clip => [pairKey(clip.verse_id, clip.script), clip])),
    [clips],
  );

  const canPlayAudio = useCallback(
    (verse, script) => clipByPair.has(pairKey(verse.id, script)),
    [clipByPair],
  );

  const onPlayAudio = useCallback((verse, script, abortSignal) => {
    const clip = clipByPair.get(pairKey(verse.id, script));
    if (!clip) return Promise.reject(new Error('No static clip'));

    activeRef.current?.stop();
    const audio = new Audio(clip.path);
    audio.preload = 'auto';

    return new Promise((resolve, reject) => {
      let settled = false;
      const cleanup = () => {
        audio.onended = null;
        audio.onerror = null;
        abortSignal?.removeEventListener('abort', stop);
        if (activeRef.current?.audio === audio) activeRef.current = null;
      };
      const finish = callback => {
        if (settled) return;
        settled = true;
        cleanup();
        callback();
      };
      const stop = () => {
        audio.pause();
        try { audio.currentTime = 0; } catch {
          // Some browsers reject seeking before metadata is available.
        }
        finish(resolve);
      };

      activeRef.current = { audio, stop };
      audio.onended = () => finish(resolve);
      audio.onerror = () => finish(() => reject(new Error('Static audio unavailable')));
      abortSignal?.addEventListener('abort', stop, { once: true });
      if (abortSignal?.aborted) {
        stop();
        return;
      }
      audio.play().catch(error => finish(() => reject(error)));
    });
  }, [clipByPair]);

  return { canPlayAudio, onPlayAudio };
}
