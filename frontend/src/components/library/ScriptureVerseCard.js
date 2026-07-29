import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Bookmark, Check, Copy, Square, Volume2 } from 'lucide-react';
import { LANGUAGE_NAMES, SPEECH_LANGS, scriptsFor } from '../../lib/scripture';

const CONTENT_LANGS = {
  en: 'en',
  dev: 'sa-Deva',
  iast: 'sa-Latn',
  roman: 'sa-Latn',
  ml: 'sa-Mlym',
  ta: 'sa-Taml',
  te: 'sa-Telu',
  kn: 'sa-Knda',
  hi: 'hi-Deva',
};

let subscribedSynth = null;
let cachedVoices = [];
const voiceSubscribers = new Set();

function readVoices(synth) {
  try {
    return synth?.getVoices() || [];
  } catch {
    return [];
  }
}

function publishVoices() {
  cachedVoices = readVoices(subscribedSynth);
  voiceSubscribers.forEach(subscriber => subscriber(cachedVoices));
}

/** All verse cards share one browser-level voiceschanged listener. */
function subscribeToVoices(subscriber) {
  voiceSubscribers.add(subscriber);
  const synth = typeof window !== 'undefined' ? window.speechSynthesis : null;

  if (synth !== subscribedSynth) {
    subscribedSynth?.removeEventListener?.('voiceschanged', publishVoices);
    subscribedSynth = synth;
    subscribedSynth?.addEventListener?.('voiceschanged', publishVoices);
    // A changed engine means every mounted card needs the new snapshot.
    publishVoices();
  } else {
    // Mounting another card only hydrates that card. Republishing to all
    // existing cards here would turn a list of n verses into n² updates.
    subscriber(cachedVoices);
  }
  return () => {
    voiceSubscribers.delete(subscriber);
    if (!voiceSubscribers.size) {
      subscribedSynth?.removeEventListener?.('voiceschanged', publishVoices);
      subscribedSynth = null;
      cachedVoices = [];
    }
  };
}

function HighlightedText({ text, query }) {
  if (!query) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const parts = String(text).split(new RegExp(`(${escaped})`, 'ig'));
  return parts.map((part, index) => (
    part.toLocaleLowerCase() === query.toLocaleLowerCase()
      ? <mark key={`${part}-${index}`}>{part}</mark>
      : part
  ));
}

/** Installed speech voices. getVoices() is empty until the engine loads, so we
 *  also listen for voiceschanged rather than reading it once. */
function useVoices() {
  const synth = typeof window !== 'undefined' ? window.speechSynthesis : null;
  const [voices, setVoices] = useState(() => readVoices(synth));

  useEffect(() => subscribeToVoices(setVoices), [synth]);

  return voices;
}

// SpeechSynthesis is global and cannot cancel an individual utterance. Track
// the playback we own so an unmount never cancels audio started elsewhere.
let activeBrowserPlayback = null;

export function ScriptureVerseCard({ verse, query = '', saved, onToggleSaved, onCopied, onPlayAudio }) {
  const availableScripts = useMemo(() => scriptsFor(verse), [verse]);
  // English leads unless the reader switches away from it.
  const [activeScript, setActiveScript] = useState(availableScripts[0]?.code || 'en');
  const [copying, setCopying] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const playbackRef = useRef(null);
  const mountedRef = useRef(false);

  const normalizedQuery = query.trim().toLocaleLowerCase();
  const matchingScript = availableScripts.find(script => (
    normalizedQuery && script.text.toLocaleLowerCase().includes(normalizedQuery)
  ));
  const matchingScriptCode = matchingScript?.code;
  const selectedScript = availableScripts.find(script => script.code === activeScript) || availableScripts[0];

  useEffect(() => {
    if (matchingScriptCode) setActiveScript(matchingScriptCode);
  }, [matchingScriptCode, normalizedQuery]);

  const voices = useVoices();
  const speechLang = SPEECH_LANGS[selectedScript?.code];
  const voice = useMemo(() => {
    if (!speechLang || !voices.length) return null;
    const base = speechLang.split('-')[0];
    return voices.find(v => v.lang === speechLang)
      || voices.find(v => (v.lang || '').replace('_', '-').toLowerCase().startsWith(base))
      || null;
  }, [voices, speechLang]);

  // Backend audio wins when supplied; otherwise fall back to the browser voice.
  // If neither is available for this script, the control is hidden rather than
  // offered and broken.
  const canSpeak = Boolean(onPlayAudio) || Boolean(voice);

  const finishPlayback = useCallback(playback => {
    if (playbackRef.current !== playback) return;
    playbackRef.current = null;
    if (mountedRef.current) setSpeaking(false);
  }, []);

  const stopSpeaking = useCallback(() => {
    const playback = playbackRef.current;
    if (!playback) return;
    playbackRef.current = null;

    if (playback.kind === 'custom') {
      playback.controller.abort();
    } else if (activeBrowserPlayback === playback) {
      activeBrowserPlayback = null;
      playback.synth.cancel();
    }

    if (mountedRef.current) setSpeaking(false);
  }, []);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      stopSpeaking();
    };
  }, [stopSpeaking]);

  // Switching language mid-playback should not keep reading the previous one.
  const previousScriptRef = useRef(selectedScript?.code);
  useEffect(() => {
    if (previousScriptRef.current !== selectedScript?.code) {
      previousScriptRef.current = selectedScript?.code;
      stopSpeaking();
    }
  }, [selectedScript?.code, stopSpeaking]);

  const toggleAudio = async () => {
    if (speaking) { stopSpeaking(); return; }
    if (!selectedScript?.text) return;

    if (onPlayAudio) {
      const playback = {
        kind: 'custom',
        controller: new AbortController(),
      };
      playbackRef.current = playback;
      setSpeaking(true);
      try {
        // Existing two-argument callbacks remain compatible; enhanced players
        // can observe the third-argument AbortSignal to implement Stop.
        await onPlayAudio(verse, selectedScript.code, playback.controller.signal);
      } catch {
        if (!playback.controller.signal.aborted && playbackRef.current === playback) {
          onCopied?.('Audio unavailable');
        }
      } finally {
        finishPlayback(playback);
      }
      return;
    }

    const synth = window.speechSynthesis;
    if (!synth || !voice) return;
    if (activeBrowserPlayback) {
      const previousPlayback = activeBrowserPlayback;
      activeBrowserPlayback = null;
      previousPlayback.synth.cancel();
      previousPlayback.finish();
    }

    const Utterance = window.SpeechSynthesisUtterance || globalThis.SpeechSynthesisUtterance;
    if (!Utterance) return;
    const utterance = new Utterance(selectedScript.text);
    utterance.voice = voice;
    utterance.lang = voice.lang;
    utterance.rate = 0.85;                    // measured, closer to recitation
    const playback = {
      kind: 'browser',
      synth,
      utterance,
      finish: () => {
        if (activeBrowserPlayback === playback) activeBrowserPlayback = null;
        finishPlayback(playback);
      },
    };
    utterance.onend = playback.finish;
    utterance.onerror = playback.finish;
    playbackRef.current = playback;
    activeBrowserPlayback = playback;
    setSpeaking(true);
    try {
      synth.speak(utterance);
    } catch {
      playback.finish();
      onCopied?.('Audio unavailable');
    }
  };

  const copyVerse = async () => {
    const source = selectedScript?.text || verse.dev || verse.roman || '';
    const chapter = verse.ch != null ? ` — Chapter ${verse.ch}` : '';
    const heading = `${verse.tn}${chapter}, Verse ${verse.vn}`;
    // Avoid printing the English twice when English is the selected script.
    const body = selectedScript?.code === 'en' ? verse.en : `${source}\n\n${verse.en}`;
    const copy = `${heading}\n\n${body}\n\n(via DharmaSearch)`;
    setCopying(true);
    try {
      await navigator.clipboard.writeText(copy);
      onCopied('Verse copied');
    } catch {
      onCopied('Copy unavailable');
    } finally {
      setCopying(false);
    }
  };

  const languageName = LANGUAGE_NAMES[selectedScript?.code] || 'this verse';

  return (
    <article className="scripture-card" data-testid={`verse-${verse.id}`}>
      <div className="scripture-card__actions">
        {canSpeak && (
          <button
            className={speaking ? 'icon-button is-active' : 'icon-button'}
            type="button"
            onClick={toggleAudio}
            aria-label={speaking ? 'Stop reading aloud' : `Listen in ${languageName}`}
            title={speaking ? 'Stop' : `Listen in ${languageName}`}
            data-testid={`listen-${verse.id}`}
          >
            {speaking ? <Square aria-hidden="true" /> : <Volume2 aria-hidden="true" />}
          </button>
        )}
        <button
          className={saved ? 'icon-button is-active' : 'icon-button'}
          type="button"
          onClick={() => onToggleSaved(verse.id)}
          aria-label={saved ? 'Remove verse bookmark' : 'Bookmark verse'}
          aria-pressed={saved}
          title={saved ? 'Remove bookmark' : 'Bookmark'}
          data-testid={`bookmark-${verse.id}`}
        >
          <Bookmark aria-hidden="true" />
        </button>
        <button
          className="icon-button"
          type="button"
          onClick={copyVerse}
          aria-label="Copy verse"
          title="Copy verse"
          disabled={copying}
          data-testid={`copy-${verse.id}`}
        >
          {copying ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
        </button>
      </div>

      <p className="scripture-card__meta">
        <strong>{verse.tn}</strong>
        {verse.ch != null ? ` · Chapter ${verse.ch}${verse.cn ? ` · ${verse.cn}` : ''}` : ''}
        {` · Verse ${verse.vn}`}
        {!verse.complete && <span> · preview</span>}
      </p>

      {availableScripts.length > 1 && (
        <div className="script-picker" role="group" aria-label={`Language for ${verse.tn} verse ${verse.vn}`}>
          {availableScripts.map(script => (
            <button
              key={script.code}
              type="button"
              onClick={() => setActiveScript(script.code)}
              aria-pressed={activeScript === script.code}
            >
              {LANGUAGE_NAMES[script.code]}
            </button>
          ))}
        </div>
      )}

      {selectedScript && (
        <p
          className="scripture-card__original"
          data-script={selectedScript.code}
          lang={CONTENT_LANGS[selectedScript.code]}
        >
          <HighlightedText text={selectedScript.text} query={query} />
        </p>
      )}

      {/* Reading an original script? Keep the English in view underneath. */}
      {selectedScript?.code !== 'en' && verse.en && (
        <>
          <p className="scripture-card__label">English translation</p>
          <p className="scripture-card__translation" lang="en">
            <HighlightedText text={verse.en} query={query} />
          </p>
        </>
      )}

      {verse.temple && <p className="scripture-card__temple">◇ {verse.temple}</p>}
    </article>
  );
}
