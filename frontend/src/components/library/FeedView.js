import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, Check, Shuffle, Sparkles } from 'lucide-react';
import { ScriptureVerseCard } from './ScriptureVerseCard';
import { COLLECTIONS, versesForCollection } from '../../lib/collections';
import { dailyIndex } from '../../lib/scripture';
import { useMarkVisibleAsRead } from '../../hooks/useMarkVisibleAsRead';

/** Short-session reading: a scrollable card feed, themed collections, a daily
 *  set and a shuffle. Built for someone with two minutes and no plan, which is
 *  most people most of the time.
 *
 *  Verses are marked read as they scroll past rather than by asking, because
 *  requiring a tap to record something you have plainly just read is friction
 *  for exactly the reader this view exists for.
 */

export function FeedView({
  data, versesById, savedIds, onToggleSaved, onCopied, onPlayAudio, canPlayAudio,
  progress, onNavigate,
}) {
  const complete = useMemo(
    () => data.verses.filter(verse => verse.complete),
    [data.verses],
  );

  // mode: null (menu) | 'daily' | 'shuffle' | collection id
  const [mode, setMode] = useState(null);
  const [shuffleSeed, setShuffleSeed] = useState(0);
  const headingRef = useRef(null);

  const attachCard = useMarkVisibleAsRead(progress.markRead);

  const collection = COLLECTIONS.find(entry => entry.id === mode) || null;

  const verses = useMemo(() => {
    if (mode === 'daily') {
      // Three verses, stable for the day, so returning shows the same set.
      return [0, 11, 23]
        .map(offset => complete[dailyIndex(complete.length, offset)])
        .filter(Boolean);
    }
    if (mode === 'shuffle') {
      const picked = new Set();
      const out = [];
      while (out.length < 8 && picked.size < complete.length) {
        const index = Math.floor(Math.random() * complete.length);
        if (picked.has(index)) continue;
        picked.add(index);
        out.push(complete[index]);
      }
      return out;
    }
    if (collection) return versesForCollection(collection, versesById);
    return [];
  }, [mode, collection, complete, versesById, shuffleSeed]); // eslint-disable-line react-hooks/exhaustive-deps

  const open = useCallback(nextMode => {
    setMode(nextMode);
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, []);

  useEffect(() => {
    if (mode) headingRef.current?.focus({ preventScroll: true });
  }, [mode]);

  // ---- Menu ------------------------------------------------------------- //
  if (!mode) {
    const week = progress.readThisWeek;
    return (
      <section className="library-view" aria-labelledby="feed-heading">
        <p className="library-eyebrow">Short readings</p>
        <h1 className="library-title" id="feed-heading">A few minutes is enough</h1>
        <p className="library-lede library-lede--spaced">
          Readings you can finish. Nothing is timed, nothing expires, and stopping
          halfway costs you nothing.
        </p>

        {progress.totalRead > 0 && (
          <p className="momentum" data-testid="momentum">
            <Sparkles aria-hidden="true" />
            <span>
              <strong>{progress.totalRead.toLocaleString()}</strong> verses read
              {week > 0 && <em> · {week} this week</em>}
            </span>
          </p>
        )}

        <div className="feed-actions">
          <button
            className="feed-action feed-action--primary"
            type="button"
            onClick={() => open('daily')}
            data-testid="feed-daily"
          >
            <strong>Today&rsquo;s three</strong>
            <span>About two minutes. The same three verses all day.</span>
          </button>
          <button
            className="feed-action"
            type="button"
            onClick={() => { setShuffleSeed(seed => seed + 1); open('shuffle'); }}
            data-testid="feed-shuffle"
          >
            <strong><Shuffle aria-hidden="true" /> Surprise me</strong>
            <span>Eight verses at random from all seven texts.</span>
          </button>
        </div>

        <h2 className="feed-section">Start from how you feel</h2>
        <div className="collection-grid">
          {COLLECTIONS.map(entry => {
            const total = entry.verses.length;
            const done = entry.verses.filter(id => progress.isRead(id)).length;
            return (
              <button
                key={entry.id}
                className="collection-card"
                type="button"
                onClick={() => open(entry.id)}
                data-testid={`collection-${entry.id}`}
              >
                <strong>{entry.title}</strong>
                <span>{entry.need}</span>
                <em>
                  {done === 0 && `${total} verses`}
                  {done > 0 && done < total && `${done} of ${total} read`}
                  {done === total && 'read'}
                </em>
              </button>
            );
          })}
        </div>
      </section>
    );
  }

  // ---- Reading a set ---------------------------------------------------- //
  const title = collection
    ? collection.title
    : mode === 'daily' ? 'Today’s three' : 'Eight at random';

  return (
    <section className="library-view" aria-labelledby="feed-heading">
      <button
        className="library-button library-button--ghost"
        type="button"
        onClick={() => setMode(null)}
        data-testid="feed-back"
      >
        <ArrowLeft aria-hidden="true" /> All readings
      </button>

      <p className="library-eyebrow">{mode === 'shuffle' ? 'Shuffle' : 'Reading'}</p>
      <h1 className="library-title" id="feed-heading" ref={headingRef} tabIndex="-1">{title}</h1>
      {collection && <p className="library-lede library-lede--spaced">{collection.why}</p>}

      <div className="feed-stack" data-testid="feed-stack">
        {verses.map((verse, index) => (
          <div key={verse.id} className="feed-slide" data-verse-id={verse.id} ref={attachCard}>
            <p className="feed-counter">{index + 1} of {verses.length}</p>
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

      <div className="feed-end">
        <p><Check aria-hidden="true" /> That&rsquo;s the set.</p>
        {mode === 'shuffle' ? (
          <button
            className="library-button"
            type="button"
            onClick={() => setShuffleSeed(seed => seed + 1)}
            data-testid="feed-again"
          >
            <Shuffle aria-hidden="true" /> Eight more
          </button>
        ) : (
          <button className="library-button" type="button" onClick={() => onNavigate('read')}>
            Read a whole text
          </button>
        )}
      </div>
    </section>
  );
}
