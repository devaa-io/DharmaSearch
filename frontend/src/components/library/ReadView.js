import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpen } from 'lucide-react';
import { ScriptureVerseCard } from './ScriptureVerseCard';
import { useMarkVisibleAsRead } from '../../hooks/useMarkVisibleAsRead';
import { useStoredState } from '../../hooks/useStoredState';

/** Reading a text end to end, as opposed to Explore's search-and-jump.
 *  Only complete texts are offered: the preview groupings are scattered
 *  samples, so "start to finish" would be misleading for them.
 *
 *  Progress is shown as ground covered, never as a target missed: a count of
 *  what has been read and nothing about what has not. `progress` is optional so
 *  the view still renders standalone. */
export function ReadView({
  data,
  savedIds,
  onToggleSaved,
  onCopied,
  onPlayAudio,
  canPlayAudio,
  progress = null,
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

  // Reading a chapter is what should count as reading it, so verses record
  // themselves here on the same terms as the short-session feed.
  const markRead = useCallback(verseId => progress?.markRead(verseId), [progress]);
  const attachVerse = useMarkVisibleAsRead(markRead);

  const chapterRead = progress
    ? chapterVerses.filter(verse => progress.isRead(verse.id)).length
    : 0;

  // Where to go next once this chapter is behind you.
  const nextUnread = progress && activeText
    ? progress.nextUnread(data.verses, activeText.id)
    : null;
  const nextUnreadChapter = nextUnread ? Number(nextUnread.ch ?? 1) : null;

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
            const stats = progress ? progress.progressFor(data.verses, text.id) : null;
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
                {stats && stats.done > 0 && (
                  <span
                    className="text-card__progress"
                    data-testid={`read-progress-${text.id}`}
                  >
                    <span
                      className="text-card__progress-bar"
                      style={{ '--read-pct': `${Math.round(stats.pct * 100)}%` }}
                      aria-hidden="true"
                    />
                    {stats.done === stats.total
                      ? 'all read'
                      : `${stats.done} of ${stats.total} read`}
                  </span>
                )}
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
        <span>
          {chapterVerses.length} {chapterVerses.length === 1 ? 'verse' : 'verses'}
          {progress && chapterRead > 0 && (
            <em className="chapter-context__read" data-testid="read-chapter-progress">
              {chapterRead === chapterVerses.length
                ? ' · all read'
                : ` · ${chapterRead} of ${chapterVerses.length} read`}
            </em>
          )}
        </span>
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
          <div key={verse.id} data-verse-id={verse.id} ref={attachVerse}>
            <ScriptureVerseCard
              verse={verse}
              saved={savedIds.has(verse.id)}
              onToggleSaved={onToggleSaved}
              onCopied={onCopied}
              onPlayAudio={onPlayAudio}
              canPlayAudio={canPlayAudio}
            />
          </div>
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

      {/* Offered, not insisted on: only once this chapter is behind you, and only
          when the next unread verse is somewhere other than here. */}
      {chapterVerses.length > 0
        && chapterRead === chapterVerses.length
        && nextUnreadChapter !== null
        && nextUnreadChapter !== activePosition.ch && (
        <button
          className="library-button"
          type="button"
          onClick={() => goToChapter(nextUnreadChapter)}
          data-testid="read-next-unread"
        >
          Pick up at chapter {nextUnreadChapter}
        </button>
      )}

      {nextChapter === null && (
        <p className="begin-note">
          <strong>You have reached the end of {activeText.name}.</strong>
          <span>Return to all texts to begin another, or sit quietly with what you have read.</span>
        </p>
      )}
    </section>
  );
}
