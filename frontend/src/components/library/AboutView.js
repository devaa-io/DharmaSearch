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

      <div className="sources">
        <h2>Where these texts come from</h2>
        <p>
          DharmaSearch is free. Nothing here is sold and there are no adverts. The scriptures
          are not ours; they are carried here so they can be read.
        </p>
        <dl>
          <dt>Original Devanagari</dt>
          <dd>
            <a href="https://sanskritdocuments.org/" target="_blank" rel="noopener noreferrer">sanskritdocuments.org</a>,
            prepared over many years by volunteers and offered for personal study and research.
          </dd>

          <dt>Bhagavad Gita</dt>
          <dd>Verse text and translation from the openly licensed <a href="https://github.com/gita/gita" target="_blank" rel="noopener noreferrer">gita/gita</a> dataset.</dd>

          <dt>Upanishads, in English</dt>
          <dd>Max M&uuml;ller, <em>Sacred Books of the East</em> (1879 and 1884), and Robert Ernest Hume (1921). Both long in the public domain.</dd>

          <dt>Vishnu Sahasranama</dt>
          <dd>Devanagari, transliteration and name meanings by Swami Krishnananda, <a href="https://www.swami-krishnananda.org/" target="_blank" rel="noopener noreferrer">The Divine Life Society</a>.</dd>

          <dt>Soundarya Lahari, Lalita Sahasranama, Hanuman Chalisa, Narayaneeyam</dt>
          <dd>English translations by P. R. Ramachander, hosted at <a href="https://www.celextel.org/" target="_blank" rel="noopener noreferrer">Celextel&rsquo;s Vedanta Spiritual Library</a>.</dd>

          <dt>Yoga Sutras, in English</dt>
          <dd>Charles Johnston&rsquo;s 1912 interpretation, preserved by <a href="https://www.gutenberg.org/ebooks/2526" target="_blank" rel="noopener noreferrer">Project Gutenberg</a>.</dd>

          <dt>Malayalam, Tamil, Telugu and Kannada</dt>
          <dd>Generated here by script-to-script transliteration from the Devanagari, never from romanised text, so vowel length and retroflexes survive intact.</dd>
        </dl>
        <p className="sources__thanks">
          Our thanks to everyone above. If you maintain one of these sources and would like
          something changed or removed, please get in touch and we will act on it.
        </p>
      </div>

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
