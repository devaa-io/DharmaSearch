import React from 'react';
import { Link } from 'react-router-dom';

export function AboutView({ texts, verses, readingSize, onReadingSize }) {
  const verseCounts = new Map();
  verses.forEach(verse => verseCounts.set(verse.tid, (verseCounts.get(verse.tid) || 0) + 1));
  const completeCount = texts.filter(text => text.complete).length;

  return (
    <section className="library-view" aria-labelledby="about-title" data-testid="about-view">
      <p className="library-eyebrow">About · what is here and what is coming</p>
      <h1 className="library-title" id="about-title">An honest map</h1>
      <p className="library-lede">
        Every complete text ships with Devanagari, IAST, Malayalam, Tamil, Telugu, Kannada and an English translation. The build refuses a release when any required verse or field is missing.
      </p>

      <div className="roadmap" aria-label="Scripture completion roadmap">
        {texts.map(text => (
          <div className="roadmap__row" key={text.id}>
            <span>{text.name} <small>· {verseCounts.get(text.id) || 0} verses{text.complete ? '' : ' (sample)'}</small></span>
            <strong className={text.complete ? 'is-complete' : ''}>{text.complete ? 'Complete' : 'In pipeline'}</strong>
          </div>
        ))}
      </div>
      <p className="pipeline-note">
        {completeCount} of {texts.length} texts are complete. Remaining works stay clearly marked as previews until they pass the same zero-gap checks.
      </p>

      <div className="reading-controls">
        <span>Reading size</span>
        <button
          type="button"
          onClick={() => onReadingSize(Math.max(0.85, readingSize - 0.1))}
          aria-label="Smaller reading text"
        >A−</button>
        <button
          type="button"
          onClick={() => onReadingSize(Math.min(1.5, readingSize + 0.1))}
          aria-label="Larger reading text"
        >A+</button>
      </div>

      <aside className="connected-note">
        <div>
          <strong>Want connected features?</strong>
          <p>Accounts, reading plans, audio and explanations remain available in the connected dashboard.</p>
        </div>
        <Link className="library-button" to="/login">Sign in</Link>
      </aside>
    </section>
  );
}
