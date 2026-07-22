import React, { useEffect, useMemo, useState } from 'react';
import { Bookmark, Check, Copy } from 'lucide-react';
import { LANGUAGE_NAMES, scriptsFor } from '../../lib/scripture';

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

export function ScriptureVerseCard({ verse, query = '', saved, onToggleSaved, onCopied }) {
  const availableScripts = useMemo(() => scriptsFor(verse), [verse]);
  const [activeScript, setActiveScript] = useState(availableScripts[0]?.code || 'roman');
  const [copying, setCopying] = useState(false);
  const normalizedQuery = query.trim().toLocaleLowerCase();
  const matchingScript = availableScripts.find(script => (
    normalizedQuery && script.text.toLocaleLowerCase().includes(normalizedQuery)
  ));
  const matchingScriptCode = matchingScript?.code;
  const selectedScript = availableScripts.find(script => script.code === activeScript) || availableScripts[0];

  useEffect(() => {
    if (matchingScriptCode) setActiveScript(matchingScriptCode);
  }, [matchingScriptCode, normalizedQuery]);

  const copyVerse = async () => {
    const source = selectedScript?.text || verse.dev || verse.roman || '';
    const chapter = verse.ch != null ? ` — Chapter ${verse.ch}` : '';
    const copy = `${verse.tn}${chapter}, Verse ${verse.vn}\n\n${source}\n\n${verse.en}\n\n(via DharmaSearch)`;
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

  return (
    <article className="scripture-card" data-testid={`verse-${verse.id}`}>
      <div className="scripture-card__actions">
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

      {selectedScript && (
        <p className="scripture-card__original" data-script={selectedScript.code}>
          <HighlightedText text={selectedScript.text} query={query} />
        </p>
      )}

      {availableScripts.length > 1 && (
        <div className="script-picker" role="group" aria-label={`Script for ${verse.tn} verse ${verse.vn}`}>
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

      <p className="scripture-card__label">English translation</p>
      <p className="scripture-card__translation">
        <HighlightedText text={verse.en} query={query} />
      </p>
      {verse.temple && <p className="scripture-card__temple">◇ {verse.temple}</p>}
    </article>
  );
}
