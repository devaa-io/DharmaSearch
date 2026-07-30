import React, { useState } from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { ScriptureVerseCard } from './ScriptureVerseCard';

export function BeginView({
  begin,
  versesById,
  completeCount,
  completedVerseCount,
  savedIds,
  onToggleSaved,
  onCopied,
  onNavigate,
  onPlayAudio,
  canPlayAudio,
}) {
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
      <p className="library-lede library-lede--spaced">
        Five verses chosen because they speak to anyone. Read the plain meaning first, then the scripture itself.
      </p>

      {/* Newcomers land on lines like "Arjuna said..." with no idea who is speaking.
          A few sentences of framing costs nothing and removes that disorientation. */}
      <aside className="begin-context">
        <h2>If you are new to this</h2>
        <p>
          Most of what follows comes from the <strong>Bhagavad Gita</strong>, a conversation
          held on a battlefield. <strong>Arjuna</strong> is a warrior who lays down his bow,
          unable to fight a war against his own family. <strong>Krishna</strong>, his
          charioteer and friend, answers him — and what begins as advice about one battle
          becomes a discussion of duty, grief, action and the self.
        </p>
        <p>
          You do not need to know the story to read it. The questions Arjuna asks are
          ordinary ones: what do I do when I am afraid, what is worth doing, what in me
          lasts. The <strong>Upanishads</strong> here are older and quieter, less a story
          than a series of attempts to describe what cannot quite be said.
        </p>
      </aside>

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
              onPlayAudio={onPlayAudio}
              canPlayAudio={canPlayAudio}
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
