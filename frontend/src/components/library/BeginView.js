import React, { useState } from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { ScriptureVerseCard } from './ScriptureVerseCard';

export function BeginView({ begin, versesById, completeCount, completedVerseCount, savedIds, onToggleSaved, onCopied, onNavigate }) {
  const [step, setStep] = useState(0);
  const atEnd = step >= begin.length;
  const item = atEnd ? null : begin[step];
  const verse = item ? versesById[item.id] : null;

  const moveTo = nextStep => {
    setStep(nextStep);
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  };

  return (
    <section className="library-view" aria-labelledby="begin-title" data-testid="begin-view">
      <p className="library-eyebrow">Begin · a first path</p>
      <h1 className="library-title" id="begin-title">Start from anywhere</h1>
      <p className="library-lede">
        Five verses chosen because they speak to anyone. Read the plain meaning first, then the scripture itself.
      </p>

      {atEnd ? (
        <div className="begin-complete">
          <p><strong>Keep going</strong>You have walked the first steps. {completeCount} complete works and {completedVerseCount.toLocaleString()} verified verses are waiting.</p>
          <button className="library-button" type="button" onClick={() => onNavigate('explore')}>
            Open the library <ArrowRight aria-hidden="true" />
          </button>
        </div>
      ) : (
        <>
          <aside className="begin-note">
            <strong>{item.title}</strong>
            <span>{item.why}</span>
          </aside>
          {verse && (
            <ScriptureVerseCard
              verse={verse}
              saved={savedIds.has(verse.id)}
              onToggleSaved={onToggleSaved}
              onCopied={onCopied}
            />
          )}
        </>
      )}

      <div className="step-navigation">
        <button
          className="library-button library-button--ghost"
          type="button"
          onClick={() => moveTo(step - 1)}
          disabled={step === 0}
        >
          <ArrowLeft aria-hidden="true" /> Back
        </button>
        <div className="step-dots" role="group" aria-label="Path progress">
          {begin.map((entry, index) => (
            <button
              key={entry.id}
              type="button"
              onClick={() => moveTo(index)}
              aria-label={`Step ${index + 1}`}
              aria-current={step === index ? 'step' : undefined}
            />
          ))}
        </div>
        <button
          className="library-button"
          type="button"
          onClick={() => moveTo(step + 1)}
          disabled={atEnd}
        >
          {step >= begin.length - 1 ? 'Finish' : 'Next'} <ArrowRight aria-hidden="true" />
        </button>
      </div>
    </section>
  );
}
