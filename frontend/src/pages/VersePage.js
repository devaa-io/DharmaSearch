import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { AlertCircle, BookOpen, LoaderCircle, Link as LinkIcon } from 'lucide-react';
import { ScriptureVerseCard } from '../components/library/ScriptureVerseCard';
import { useMarkVisibleAsRead } from '../hooks/useMarkVisibleAsRead';
import { useProgress } from '../hooks/useProgress';
import { useScriptureData } from '../hooks/useScriptureData';
import { useStaticAudio } from '../hooks/useStaticAudio';
import { useStoredState } from '../hooks/useStoredState';

/** A verse at its own address: /v/:verseId.
 *
 *  The landing for shared links, and the answer to "I can never find that
 *  verse again". Shows the full card, then offers the chapter it lives in —
 *  the link is an invitation into the text, not a dead end.
 *
 *  Verse ids are opaque strings. They are looked up, never parsed.
 */
export function VersePage() {
  const { verseId } = useParams();
  const navigate = useNavigate();
  const { data, error } = useScriptureData();
  const [saved, setSaved] = useStoredState('ds_saved', []);
  const [toast, setToast] = useState('');
  const { canPlayAudio, onPlayAudio } = useStaticAudio();
  const progress = useProgress();
  const attachCard = useMarkVisibleAsRead(progress.markRead);

  const verse = useMemo(
    () => data?.verses.find(candidate => candidate.id === verseId) || null,
    [data, verseId],
  );

  useEffect(() => {
    if (!toast) return undefined;
    const timeout = window.setTimeout(() => setToast(''), 1600);
    return () => window.clearTimeout(timeout);
  }, [toast]);

  const savedIds = useMemo(() => new Set(saved), [saved]);
  const toggleSaved = useCallback(id => {
    setSaved(current => {
      const next = new Set(current);
      if (next.has(id)) {
        next.delete(id);
        setToast('Removed from bookmarks');
      } else {
        next.add(id);
        setToast('Bookmarked');
      }
      return [...next];
    });
  }, [setSaved]);

  const openChapter = useCallback(() => {
    if (!verse) return;
    // The same resume mechanism ReadView uses, plus a one-shot jump marker it
    // consumes on mount to land on this exact verse.
    try {
      window.localStorage.setItem(
        'ds_reading',
        JSON.stringify({ tid: verse.tid, ch: Number(verse.ch ?? 1) }),
      );
      window.sessionStorage.setItem('ds_jump', verse.id);
    } catch {
      // Storage blocked: Read still opens, just at the catalogue.
    }
    navigate('/#read');
  }, [navigate, verse]);

  const copyLink = useCallback(async () => {
    const url = `${window.location.origin}/v/${verseId}`;
    try {
      await navigator.clipboard.writeText(url);
      setToast('Link copied');
    } catch {
      setToast('Copy unavailable');
    }
  }, [verseId]);

  if (error) {
    return (
      <main className="library-state" data-testid="verse-page-error">
        <AlertCircle aria-hidden="true" />
        <h1>The scripture library could not be loaded.</h1>
        <p>{error.message}. Refresh this page to try again.</p>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="library-state" data-testid="verse-page-loading">
        <LoaderCircle className="is-spinning" aria-hidden="true" />
        <p>Opening the verse…</p>
      </main>
    );
  }

  if (!verse) {
    return (
      <main className="library-state" data-testid="verse-page-missing">
        <BookOpen aria-hidden="true" />
        <h1>This verse is not here yet.</h1>
        <p>
          The link may be old, or the text it points to has not been added.
          The library itself is always open.
        </p>
        <button className="library-button" type="button" onClick={() => navigate('/')}>
          Open the library
        </button>
      </main>
    );
  }

  return (
    <div className="library-app verse-page">
      <header className="library-header">
        <div className="library-header__inner">
          <button className="library-brand" type="button" onClick={() => navigate('/')}>
            Dharma<span>Search</span>
          </button>
        </div>
      </header>

      <main className="library-shell">
        <section className="library-view" aria-labelledby="verse-heading">
          <p className="library-eyebrow">A verse from {verse.tn}</p>
          <h1 className="library-title" id="verse-heading">
            {verse.ch != null ? `Chapter ${verse.ch}, ` : ''}Verse {verse.vn}
          </h1>

          <div data-verse-id={verse.id} ref={attachCard}>
            <ScriptureVerseCard
              verse={verse}
              saved={savedIds.has(verse.id)}
              onToggleSaved={toggleSaved}
              onCopied={setToast}
              onPlayAudio={onPlayAudio}
              canPlayAudio={canPlayAudio}
            />
          </div>

          <div className="verse-page__actions">
            <button
              className="library-button"
              type="button"
              onClick={openChapter}
              data-testid="verse-open-chapter"
            >
              <BookOpen aria-hidden="true" /> Read this chapter
            </button>
            <button
              className="library-button library-button--ghost"
              type="button"
              onClick={copyLink}
              data-testid="verse-copy-link"
            >
              <LinkIcon aria-hidden="true" /> Copy link
            </button>
          </div>
        </section>
      </main>

      <footer className="library-footer">
        <div>
          DharmaSearch — original text, transliteration and translation.<br />
          <span>Private by default: reading, search, bookmarks and meditation stay on this device.</span>
        </div>
      </footer>

      <div className={toast ? 'library-toast is-visible' : 'library-toast'} role="status" aria-live="polite">
        {toast}
      </div>
    </div>
  );
}
