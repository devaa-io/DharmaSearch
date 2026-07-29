import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpen } from 'lucide-react';
import { ScriptureVerseCard } from './ScriptureVerseCard';
import { useStoredState } from '../../hooks/useStoredState';

/** Reading a text end to end, as opposed to Explore's search-and-jump.
 *  Only complete texts are offered: the preview groupings are scattered
 *  samples, so "start to finish" would be misleading for them. */
export function ReadView({
  data,
  savedIds,
  onToggleSaved,
  onCopied,
  onPlayAudio,
  canPlayAudio,
}) {
  // The saved position is a bookmark, not the screen state. Read always opens
  // on the catalogue so a returning reader can choose whether to resume.
  const [savedPosition, setSavedPosition] = useStoredState('ds_reading', null);
  const [openPosition, setOpenPosition] = useState(null);
  const focusChapterOnChangeRef = useRef(false);
  const focusCatalogueOnReturnRef = useRef(false);
  const chapterHeadingRef = useRef(null);
  const catalogueHeadingRef = useRef(null);

  const readableTexts = useMemo(
    () => data.texts.filter(text => text.complete),
    [data.texts],
  );

  const chaptersByText = useMemo(() => {
    const chapters = new Map();
    data.verses.forEach(verse => {
      if (!verse.complete) return;
      if (!chapters.has(verse.tid)) chapters.set(verse.tid, new Set());
      const chapter = Number(verse.ch ?? 1);
      chapters.get(verse.tid).add(Number.isFinite(chapter) ? chapter : 1);
    });
    return new Map([...chapters].map(([tid, values]) => [tid, [...values].sort((a, b) => a - b)]));
  }, [data.verses]);

  const normalizePosition = useCallback(candidate => {
    if (!candidate || typeof candidate.tid !== 'string') return null;
    const chapters = chaptersByText.get(candidate.tid);
    if (!chapters?.length || !readableTexts.some(text => text.id === candidate.tid)) return null;

    const requestedChapter = Number(candidate.ch);
    if (!Number.isFinite(requestedChapter)) return { tid: candidate.tid, ch: chapters[0] };
    if (chapters.includes(requestedChapter)) return { tid: candidate.tid, ch: requestedChapter };

    // Data can change between releases. Keep a valid text bookmark useful by
    // clamping a stale chapter to the nearest chapter that still exists.
    const nearestChapter = chapters.reduce((nearest, chapter) => (
      Math.abs(chapter - requestedChapter) < Math.abs(nearest - requestedChapter)
        ? chapter
        : nearest
    ), chapters[0]);
    return { tid: candidate.tid, ch: nearestChapter };
  }, [chaptersByText, readableTexts]);

  const resumePosition = useMemo(
    () => normalizePosition(savedPosition),
    [normalizePosition, savedPosition],
  );
  const activePosition = useMemo(
    () => normalizePosition(openPosition),
    [normalizePosition, openPosition],
  );
  const activeText = activePosition
    ? readableTexts.find(text => text.id === activePosition.tid)
    : null;
  const chapters = activeText ? (chaptersByText.get(activeText.id) || []) : [];
  const chapterIndex = activeText ? chapters.indexOf(activePosition.ch) : -1;

  const chapterVerses = useMemo(() => {
    if (!activeText || !activePosition) return [];
    return data.verses
      .filter(verse => (
        verse.complete
        && verse.tid === activeText.id
        && Number(verse.ch ?? 1) === activePosition.ch
      ))
      .sort((a, b) => a.vn - b.vn);
  }, [activePosition, activeText, data.verses]);

  const chapterName = data.chapterMeta?.[activeText?.id]?.[String(activePosition?.ch)]?.tr
    || chapterVerses[0]?.cn
    || '';

  const openText = useCallback(textId => {
    const firstPosition = normalizePosition({ tid: textId, ch: (chaptersByText.get(textId) || [1])[0] });
    if (!firstPosition) return;
    focusChapterOnChangeRef.current = true;
    setOpenPosition(firstPosition);
    setSavedPosition(firstPosition);
  }, [chaptersByText, normalizePosition, setSavedPosition]);

  const resumeReading = useCallback(() => {
    if (!resumePosition) return;
    focusChapterOnChangeRef.current = true;
    setOpenPosition(resumePosition);
    // This also heals an old or malformed chapter value after data changes.
    setSavedPosition(resumePosition);
  }, [resumePosition, setSavedPosition]);

  const goToChapter = useCallback(nextChapter => {
    if (!activeText) return;
    const nextPosition = normalizePosition({ tid: activeText.id, ch: nextChapter });
    if (!nextPosition) return;
    focusChapterOnChangeRef.current = true;
    setOpenPosition(nextPosition);
    setSavedPosition(nextPosition);
  }, [activeText, normalizePosition, setSavedPosition]);

  const returnToCatalogue = useCallback(() => {
    focusCatalogueOnReturnRef.current = true;
    setOpenPosition(null);
  }, []);

  // Moving between chapters should feel like turning a page, not staying put.
  useEffect(() => {
    if (!activeText || !activePosition) {
      if (focusCatalogueOnReturnRef.current) {
        focusCatalogueOnReturnRef.current = false;
        catalogueHeadingRef.current?.focus({ preventScroll: true });
      }
      return;
    }
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
    if (focusChapterOnChangeRef.current) {
      focusChapterOnChangeRef.current = false;
      chapterHeadingRef.current?.focus({ preventScroll: true });
    }
  }, [activePosition, activeText]);

  // ---- Library: choose something to read -------------------------------- //
  if (!activeText) {
    const resume = resumePosition
      ? readableTexts.find(text => text.id === resumePosition.tid)
      : null;
    return (
      <section className="library-view" aria-labelledby="read-heading">
        <p className="library-eyebrow">Read</p>
        <h1
          className="library-title"
          id="read-heading"
          ref={catalogueHeadingRef}
          tabIndex="-1"
        >
          Read a text from beginning to end
        </h1>
        <p className="library-lede library-lede--spaced">
          Take a whole text at your own pace, chapter by chapter. Your place is kept on this
          device, so you can stop anywhere and pick the thread back up.
        </p>

        {resume && (
          <button
            className="resume-card"
            type="button"
            onClick={resumeReading}
            data-testid="read-resume"
          >
            <BookOpen aria-hidden="true" />
            <span>
              <strong>Continue {resume.name}</strong>
              <em>Chapter {resumePosition.ch}</em>
            </span>
          </button>
        )}

        <div className="text-grid">
          {readableTexts.map(text => {
            const count = (chaptersByText.get(text.id) || []).length;
            return (
              <button
                key={text.id}
                className="text-card"
                type="button"
                onClick={() => openText(text.id)}
                data-testid={`read-text-${text.id}`}
              >
                <strong>{text.name}</strong>
                <span>{text.tv} verses · {count} {count === 1 ? 'section' : 'sections'}</span>
                <em className="is-complete">complete</em>
              </button>
            );
          })}
        </div>
      </section>
    );
  }

  // ---- Reading ---------------------------------------------------------- //
  const previousChapter = chapterIndex > 0 ? chapters[chapterIndex - 1] : null;
  const nextChapter = chapterIndex > -1 && chapterIndex < chapters.length - 1
    ? chapters[chapterIndex + 1]
    : null;

  return (
    <section className="library-view" aria-labelledby="read-heading">
      <button
        className="library-button library-button--ghost"
        type="button"
        onClick={returnToCatalogue}
        data-testid="read-back"
      >
        <ArrowLeft aria-hidden="true" /> All texts
      </button>

      <p className="library-eyebrow">Reading</p>
      <h1 className="library-title" id="read-heading">{activeText.name}</h1>

      <div className="chapter-context">
        <h2 ref={chapterHeadingRef} tabIndex="-1">
          {chapters.length > 1 ? `Chapter ${activePosition.ch} of ${chapters.length}` : 'Complete text'}
          {chapterName ? ` · ${chapterName}` : ''}
        </h2>
        <span>{chapterVerses.length} {chapterVerses.length === 1 ? 'verse' : 'verses'}</span>
      </div>

      {chapters.length > 1 && (
        <div className="chapter-picker" role="group" aria-label={`Chapters of ${activeText.name}`}>
          {chapters.map(chapter => (
            <button
              key={chapter}
              type="button"
              onClick={() => goToChapter(chapter)}
              aria-pressed={chapter === activePosition.ch}
            >
              {chapter}
            </button>
          ))}
        </div>
      )}

      <div data-testid="read-verses">
        {chapterVerses.map(verse => (
          <ScriptureVerseCard
            key={verse.id}
            verse={verse}
            saved={savedIds.has(verse.id)}
            onToggleSaved={onToggleSaved}
            onCopied={onCopied}
            onPlayAudio={onPlayAudio}
            canPlayAudio={canPlayAudio}
          />
        ))}
      </div>

      <div className="step-navigation">
        <button
          className="library-button"
          type="button"
          onClick={() => goToChapter(previousChapter)}
          disabled={previousChapter === null}
          data-testid="read-prev"
        >
          <ArrowLeft aria-hidden="true" /> Previous
        </button>
        <button
          className="library-button"
          type="button"
          onClick={() => goToChapter(nextChapter)}
          disabled={nextChapter === null}
          data-testid="read-next"
        >
          Next <ArrowRight aria-hidden="true" />
        </button>
      </div>

      {nextChapter === null && (
        <p className="begin-note">
          <strong>You have reached the end of {activeText.name}.</strong>
          <span>Return to all texts to begin another, or sit quietly with what you have read.</span>
        </p>
      )}
    </section>
  );
}
