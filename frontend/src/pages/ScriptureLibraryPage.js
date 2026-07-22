import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AlertCircle, LoaderCircle } from 'lucide-react';
import { AboutView } from '../components/library/AboutView';
import { BeginView } from '../components/library/BeginView';
import { ExploreView } from '../components/library/ExploreView';
import { LibraryHeader } from '../components/library/LibraryHeader';
import { MeditateView } from '../components/library/MeditateView';
import { TodayView } from '../components/library/TodayView';
import { useScriptureData } from '../hooks/useScriptureData';
import { useStoredState } from '../hooks/useStoredState';

const VIEWS = new Set(['today', 'begin', 'explore', 'meditate', 'about']);

function viewFromHash() {
  const candidate = window.location.hash.slice(1);
  return VIEWS.has(candidate) ? candidate : 'today';
}

export function ScriptureLibraryPage() {
  const { data, error } = useScriptureData();
  const [activeView, setActiveView] = useState(viewFromHash);
  const [saved, setSaved] = useStoredState('ds_saved', []);
  const [readingSize, setReadingSize] = useStoredState('ds_fs', 1);
  const [toast, setToast] = useState('');
  const completeVerses = useMemo(
    () => data?.verses.filter(verse => verse.complete) || [],
    [data],
  );
  const versesById = useMemo(
    () => Object.fromEntries((data?.verses || []).map(verse => [verse.id, verse])),
    [data],
  );

  useEffect(() => {
    const onHashChange = () => setActiveView(viewFromHash());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  useEffect(() => {
    if (!toast) return undefined;
    const timeout = window.setTimeout(() => setToast(''), 1600);
    return () => window.clearTimeout(timeout);
  }, [toast]);

  const navigate = useCallback(view => {
    if (!VIEWS.has(view)) return;
    window.history.pushState(null, '', `#${view}`);
    setActiveView(view);
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  }, []);

  const savedIds = useMemo(() => new Set(saved), [saved]);
  const toggleSaved = useCallback(verseId => {
    setSaved(current => {
      const next = new Set(current);
      if (next.has(verseId)) {
        next.delete(verseId);
        setToast('Removed from bookmarks');
      } else {
        next.add(verseId);
        setToast('Bookmarked');
      }
      return [...next];
    });
  }, [setSaved]);

  if (error) {
    return (
      <main className="library-state" data-testid="library-error">
        <AlertCircle aria-hidden="true" />
        <h1>The scripture library could not be loaded.</h1>
        <p>{error.message}. Rebuild the generated asset and refresh this page.</p>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="library-state" data-testid="library-loading">
        <LoaderCircle className="is-spinning" aria-hidden="true" />
        <p>Opening the library…</p>
      </main>
    );
  }

  const sharedVerseProps = {
    savedIds,
    onToggleSaved: toggleSaved,
    onCopied: setToast,
  };

  return (
    <div className="library-app" style={{ '--reading-scale': readingSize }}>
      <a className="skip-link" href="#library-main">Skip to content</a>
      <LibraryHeader activeView={activeView} onNavigate={navigate} />
      <main className="library-shell" id="library-main">
        {activeView === 'today' && (
          <TodayView
            texts={data.texts}
            completeVerses={completeVerses}
            onNavigate={navigate}
            {...sharedVerseProps}
          />
        )}
        {activeView === 'begin' && (
          <BeginView
            begin={data.begin}
            versesById={versesById}
            completeCount={data.texts.filter(text => text.complete).length}
            completedVerseCount={completeVerses.length}
            onNavigate={navigate}
            {...sharedVerseProps}
          />
        )}
        {activeView === 'explore' && <ExploreView data={data} {...sharedVerseProps} />}
        {activeView === 'meditate' && <MeditateView completeVerses={completeVerses} />}
        {activeView === 'about' && (
          <AboutView
            texts={data.texts}
            verses={data.verses}
            readingSize={readingSize}
            onReadingSize={setReadingSize}
          />
        )}
      </main>
      <footer className="library-footer">
        <div>
          DharmaSearch — original text, transliteration and translation. {data.texts.filter(text => text.complete).length} complete texts, with more built through a zero-gap pipeline.<br />
          <span>Private by default: reading, search, bookmarks and meditation stay on this device.</span>
        </div>
      </footer>
      <div className={toast ? 'library-toast is-visible' : 'library-toast'} role="status" aria-live="polite">
        {toast}
      </div>
    </div>
  );
}
