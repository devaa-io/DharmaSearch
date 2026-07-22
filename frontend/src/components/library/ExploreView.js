import React, { useDeferredValue, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Search } from 'lucide-react';
import { searchBlob } from '../../lib/scripture';
import { ScriptureVerseCard } from './ScriptureVerseCard';

const PAGE_SIZE = 25;

export function ExploreView({ data, savedIds, onToggleSaved, onCopied }) {
  const { texts, verses, chapterMeta = {} } = data;
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query.trim());
  const [libraryFilter, setLibraryFilter] = useState('complete');
  const [activeTextId, setActiveTextId] = useState(null);
  const [activeChapter, setActiveChapter] = useState(null);
  const [page, setPage] = useState(0);

  const textCounts = useMemo(() => {
    const counts = new Map();
    verses.forEach(verse => counts.set(verse.tid, (counts.get(verse.tid) || 0) + 1));
    return counts;
  }, [verses]);

  const chaptersByText = useMemo(() => {
    const chapters = new Map();
    verses.forEach(verse => {
      if (verse.ch == null) return;
      if (!chapters.has(verse.tid)) chapters.set(verse.tid, new Set());
      chapters.get(verse.tid).add(verse.ch);
    });
    return new Map([...chapters].map(([textId, values]) => (
      [textId, [...values].sort((left, right) => left - right)]
    )));
  }, [verses]);

  const activeText = texts.find(text => text.id === activeTextId);
  const activeTextChapters = chaptersByText.get(activeTextId) || [];
  const normalizedQuery = deferredQuery.toLocaleLowerCase();

  const results = useMemo(() => {
    let matches = verses;
    if (activeTextId) matches = matches.filter(verse => verse.tid === activeTextId);
    if (normalizedQuery) matches = matches.filter(verse => searchBlob(verse).includes(normalizedQuery));
    if (!normalizedQuery && activeTextId && activeChapter != null) {
      matches = matches.filter(verse => verse.ch === activeChapter);
    }
    return matches;
  }, [activeChapter, activeTextId, normalizedQuery, verses]);

  const filteredTexts = texts.filter(text => (
    libraryFilter === 'all' || (libraryFilter === 'complete' ? text.complete : !text.complete)
  ));
  const shouldShowResults = Boolean(normalizedQuery || activeTextId);
  const pageCount = Math.max(1, Math.ceil(results.length / PAGE_SIZE));
  const safePage = Math.min(page, pageCount - 1);
  const visibleResults = shouldShowResults
    ? results.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE)
    : [];
  const completeCount = texts.filter(text => text.complete).length;
  const previewCount = texts.length - completeCount;
  const completedVerseCount = verses.filter(verse => verse.complete).length;

  const chooseFilter = filter => {
    setLibraryFilter(filter);
    setActiveTextId(null);
    setActiveChapter(null);
    setPage(0);
  };

  const chooseText = textId => {
    if (activeTextId === textId) {
      setActiveTextId(null);
      setActiveChapter(null);
    } else {
      const chapters = chaptersByText.get(textId) || [];
      setActiveTextId(textId);
      setActiveChapter(chapters.length > 1 ? chapters[0] : null);
    }
    setQuery('');
    setPage(0);
  };

  const updateQuery = event => {
    setQuery(event.target.value);
    setPage(0);
  };

  const changePage = nextPage => {
    setPage(nextPage);
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  };

  const countLabel = normalizedQuery
    ? `${results.length} verse${results.length === 1 ? '' : 's'}${activeText ? ` in ${activeText.name}` : ' across all texts'}`
    : activeText
      ? `${activeText.name}${activeChapter != null ? ` · Chapter ${activeChapter}` : ''} · ${results.length} verses`
      : 'Pick a text below, or search in any language';

  return (
    <section className="library-view" aria-labelledby="explore-title" data-testid="explore-view">
      <p className="library-eyebrow">Explore · the full library</p>
      <h1 className="library-title" id="explore-title">Search the scriptures</h1>
      <p className="library-lede library-lede--spaced">
        Read {completeCount} complete works or search {verses.length.toLocaleString()} passages across every available script. {completedVerseCount.toLocaleString()} have passed the full zero-gap check.
      </p>

      <label className="library-search" htmlFor="scripture-search">
        <span className="sr-only">Search verses in any language</span>
        <Search aria-hidden="true" />
        <input
          id="scripture-search"
          type="search"
          value={query}
          onChange={updateQuery}
          placeholder="Search in English or any script — dharma, धर्म, ധര്‍മ്മം, fear…"
          autoComplete="off"
          data-testid="scripture-search"
        />
      </label>
      <p className="library-count" aria-live="polite">{countLabel}</p>

      {!normalizedQuery && (
        <div className="library-catalogue">
          <div className="library-tools">
            <h2>The library</h2>
            <div className="library-filters" role="group" aria-label="Filter library">
              {[
                ['complete', 'Complete', completeCount],
                ['all', 'All', texts.length],
                ['preview', 'Preview', previewCount],
              ].map(([id, label, count]) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => chooseFilter(id)}
                  aria-pressed={libraryFilter === id}
                  data-testid={`library-filter-${id}`}
                >
                  {label} <span>{count}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="text-grid">
            {filteredTexts.map(text => (
              <button
                key={text.id}
                className="text-card"
                type="button"
                onClick={() => chooseText(text.id)}
                aria-pressed={activeTextId === text.id}
                data-testid={`text-${text.id}`}
              >
                <strong>{text.name}</strong>
                <span>{text.lang} · {textCounts.get(text.id) || 0} verses</span>
                <em className={text.complete ? 'is-complete' : ''}>{text.complete ? 'Complete' : 'Preview'}</em>
              </button>
            ))}
          </div>
        </div>
      )}

      {activeText && !normalizedQuery && (
        <div className="text-context">
          <div className="text-context__description">
            <h2>{activeText.name}</h2>
            <p>{activeText.desc}</p>
          </div>
          {activeTextChapters.length > 1 && (
            <div className="chapter-picker" role="group" aria-label={`Chapters of ${activeText.name}`}>
              {activeTextChapters.map(chapter => (
                <button
                  key={chapter}
                  type="button"
                  onClick={() => { setActiveChapter(chapter); setPage(0); }}
                  aria-pressed={activeChapter === chapter}
                >
                  Ch {chapter}
                </button>
              ))}
            </div>
          )}
          {chapterMeta[activeTextId]?.[activeChapter] && (
            <div className="chapter-context">
              <strong>Section {activeChapter} · {chapterMeta[activeTextId][activeChapter].tr}</strong>
              <span>{chapterMeta[activeTextId][activeChapter].mean}</span>
            </div>
          )}
        </div>
      )}

      {shouldShowResults && (
        <div className="verse-results" data-testid="scripture-results">
          {visibleResults.length > 0 ? visibleResults.map(verse => (
            <ScriptureVerseCard
              key={verse.id}
              verse={verse}
              query={deferredQuery}
              saved={savedIds.has(verse.id)}
              onToggleSaved={onToggleSaved}
              onCopied={onCopied}
            />
          )) : (
            <p className="library-empty">No verses match “{deferredQuery}”. Try a broader word or another script.</p>
          )}
        </div>
      )}

      {shouldShowResults && pageCount > 1 && (
        <nav className="result-pagination" aria-label="Search result pages">
          <button
            className="library-button library-button--ghost"
            type="button"
            onClick={() => changePage(safePage - 1)}
            disabled={safePage === 0}
          >
            <ArrowLeft aria-hidden="true" /> Previous
          </button>
          <span>Page {safePage + 1} / {pageCount}</span>
          <button
            className="library-button library-button--ghost"
            type="button"
            onClick={() => changePage(safePage + 1)}
            disabled={safePage >= pageCount - 1}
          >
            Next <ArrowRight aria-hidden="true" />
          </button>
        </nav>
      )}
    </section>
  );
}
