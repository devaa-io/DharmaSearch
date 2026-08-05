import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { CONCEPTS } from '../../lib/concepts';

/** Every concept must have at least one citation that resolves against the
 *  live corpus. A concept whose verses aren't in this build (yet) drops
 *  silently rather than showing a dead /v/:id link. */
export function ConceptsView({ versesById }) {
  const concepts = useMemo(() => CONCEPTS
    .map(concept => ({
      ...concept,
      citedVerses: concept.cites.map(id => versesById[id]).filter(Boolean),
    }))
    .filter(concept => concept.citedVerses.length > 0), [versesById]);

  return (
    <section className="library-view" aria-labelledby="concepts-title" data-testid="concepts-view">
      <p className="library-eyebrow">Concepts · grounded in the text</p>
      <h1 className="library-title" id="concepts-title">A short glossary</h1>
      <p className="library-lede">
        Ideas that recur across the library, each pointing back to specific verses rather than
        standing alone. Tap a citation to read it in context.
      </p>

      <div className="concept-grid">
        {concepts.map(concept => (
          <article className="concept-card" key={concept.id}>
            <div className="concept-term">
              <h2>{concept.term}</h2>
              <span className="concept-sanskrit">{concept.sanskrit}</span>
            </div>
            <p className="concept-body">{concept.body}</p>
            <div className="concept-cites">
              {concept.citedVerses.map(verse => (
                <Link
                  key={verse.id}
                  className="cite-pill"
                  to={`/v/${verse.id}`}
                  data-testid={`concept-cite-${verse.id}`}
                >
                  {verse.tn} {verse.ch != null ? `${verse.ch}.` : ''}{verse.vn}
                </Link>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
