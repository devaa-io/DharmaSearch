import React, { useMemo } from 'react';
import { ScriptureVerseCard } from './ScriptureVerseCard';

/** Bookmarking without a way to browse what's bookmarked is a dead end —
 *  this is that missing screen. Most-recently-saved first. */
export function SavedView({
  savedIds, versesById, onToggleSaved, onCopied, onPlayAudio, canPlayAudio, onNavigate,
}) {
  const verses = useMemo(
    () => [...savedIds].reverse().map(id => versesById[id]).filter(Boolean),
    [savedIds, versesById],
  );

  return (
    <section className="library-view" aria-labelledby="saved-title" data-testid="saved-view">
      <p className="library-eyebrow">Saved · kept on this device</p>
      <h1 className="library-title" id="saved-title">Your saved verses</h1>
      <p className="library-lede">
        {verses.length > 0
          ? `${verses.length} verse${verses.length === 1 ? '' : 's'} bookmarked. Nothing here leaves this device.`
          : 'Nothing saved yet. Tap the bookmark icon on any verse to keep it here.'}
      </p>

      {verses.length === 0 ? (
        <button className="library-button" type="button" onClick={() => onNavigate('explore')}>
          Browse verses
        </button>
      ) : (
        <div data-testid="saved-verses">
          {verses.map(verse => (
            <ScriptureVerseCard
              key={verse.id}
              verse={verse}
              saved
              onToggleSaved={onToggleSaved}
              onCopied={onCopied}
              onPlayAudio={onPlayAudio}
              canPlayAudio={canPlayAudio}
            />
          ))}
        </div>
      )}
    </section>
  );
}
