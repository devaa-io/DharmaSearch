import { useCallback, useMemo } from 'react';
import { useStoredState } from './useStoredState';

/** Reading progress, deliberately built as momentum rather than pressure.
 *
 *  We record WHEN a verse was read, never a streak that can break. There is no
 *  score to lose and no penalty for a gap, because a reader who misses a week
 *  should feel invited back rather than in debt — and the text this app carries
 *  argues against attachment to outcome in the first place.
 *
 *  Stored as { verseId: timestamp } so we can answer "what did you read this
 *  week" without keeping a separate log.
 */
export function useProgress() {
  const [read, setRead] = useStoredState('ds_read', {});

  const markRead = useCallback(verseId => {
    if (!verseId) return;
    setRead(current => (current[verseId] ? current : { ...current, [verseId]: Date.now() }));
  }, [setRead]);

  const toggleRead = useCallback(verseId => {
    if (!verseId) return;
    setRead(current => {
      const next = { ...current };
      if (next[verseId]) delete next[verseId];
      else next[verseId] = Date.now();
      return next;
    });
  }, [setRead]);

  const isRead = useCallback(verseId => Boolean(read[verseId]), [read]);

  const totalRead = useMemo(() => Object.keys(read).length, [read]);

  const readThisWeek = useMemo(() => {
    const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
    return Object.values(read).filter(at => at >= cutoff).length;
  }, [read]);

  /** Per-text counts, for progress rings. */
  const progressFor = useCallback((verses, textId) => {
    const inText = verses.filter(verse => verse.tid === textId && verse.complete);
    const done = inText.filter(verse => read[verse.id]).length;
    return { done, total: inText.length, pct: inText.length ? done / inText.length : 0 };
  }, [read]);

  /** The next unread verse of a text, so "continue" always has somewhere to go. */
  const nextUnread = useCallback((verses, textId) => {
    const inText = verses
      .filter(verse => verse.tid === textId && verse.complete)
      .sort((a, b) => (a.ch - b.ch) || (a.vn - b.vn));
    return inText.find(verse => !read[verse.id]) || null;
  }, [read]);

  return { read, markRead, toggleRead, isRead, totalRead, readThisWeek, progressFor, nextUnread };
}
