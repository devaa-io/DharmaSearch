import React, { useMemo } from 'react';
import { ScriptureVerseCard } from './ScriptureVerseCard';
import { dailyIndex } from '../../lib/scripture';

export function TodayView({ texts, completeVerses, savedIds, onToggleSaved, onCopied, onNavigate }) {
  const verse = completeVerses[dailyIndex(completeVerses.length)];
  const shortVerses = useMemo(
    () => completeVerses.filter(item => item.en.length > 20 && item.en.length < 150),
    [completeVerses],
  );
  const saying = shortVerses[dailyIndex(shortVerses.length, 7)];
  const date = new Intl.DateTimeFormat(undefined, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  }).format(new Date());

  return (
    <section className="library-view" aria-labelledby="today-title" data-testid="today-view">
      <p className="library-eyebrow">Today · {date}</p>
      <h1 className="library-title" id="today-title">A verse for today</h1>
      <p className="library-lede">
        Begin with the original. Move through its scripts. Sit with the English when you are ready.
      </p>
      <div className="trust-strip" aria-label="Library summary">
        <span><strong>{texts.filter(text => text.complete).length}</strong> complete texts</span>
        <span><strong>{completeVerses.length.toLocaleString()}</strong> verified verses</span>
        <span><strong>6 scripts</strong> + English</span>
      </div>

      <ScriptureVerseCard
        verse={verse}
        saved={savedIds.has(verse.id)}
        onToggleSaved={onToggleSaved}
        onCopied={onCopied}
      />

      <blockquote className="daily-saying">
        “{saying.en}”
        <cite>{saying.tn}</cite>
      </blockquote>

      <p className="library-eyebrow">Where would you like to start?</p>
      <div className="library-doors">
        <button type="button" onClick={() => onNavigate('begin')} data-testid="today-begin">
          <strong>Begin</strong>
          <span>New here? Follow a short path in plain English, with no prior knowledge needed.</span>
        </button>
        <button type="button" onClick={() => onNavigate('explore')} data-testid="today-explore">
          <strong>Explore</strong>
          <span>Search every verse in six scripts, or read a complete work section by section.</span>
        </button>
        <button type="button" onClick={() => onNavigate('meditate')} data-testid="today-meditate">
          <strong>Meditate</strong>
          <span>Choose a quiet interval. Read what surfaces, breathe, and let the rest pass.</span>
        </button>
      </div>
    </section>
  );
}
