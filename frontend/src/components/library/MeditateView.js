import React, { useEffect, useMemo, useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';

export function MeditateView({ completeVerses }) {
  const [minutes, setMinutes] = useState(10);
  const [remainingSeconds, setRemainingSeconds] = useState(0);
  const [fragmentIndex, setFragmentIndex] = useState(0);
  const [completed, setCompleted] = useState(false);
  const active = remainingSeconds > 0;

  const fragments = useMemo(() => {
    const items = [];
    completeVerses.forEach(verse => {
      if (verse.en.length < 90) items.push(verse.en);
      const romanWords = (verse.roman || '').trim().split(/\s+/);
      if (romanWords.length >= 3 && romanWords.length <= 8) items.push(verse.roman);
    });
    return items;
  }, [completeVerses]);

  useEffect(() => {
    if (!active) return undefined;
    const countdown = window.setInterval(() => {
      setRemainingSeconds(current => {
        if (current <= 1) {
          setCompleted(true);
          return 0;
        }
        return current - 1;
      });
    }, 1000);
    const rotate = window.setInterval(() => {
      setFragmentIndex(current => (current + 1) % fragments.length);
    }, 6500);
    return () => {
      window.clearInterval(countdown);
      window.clearInterval(rotate);
    };
  }, [active, fragments.length]);

  const begin = () => {
    setCompleted(false);
    setFragmentIndex(Math.floor(Math.random() * fragments.length));
    setRemainingSeconds(minutes * 60);
  };

  const close = () => {
    setRemainingSeconds(0);
    setCompleted(false);
  };

  const time = `${Math.floor(remainingSeconds / 60)}:${String(remainingSeconds % 60).padStart(2, '0')}`;

  return (
    <Dialog.Root open={active || completed} onOpenChange={open => { if (!open) close(); }}>
      <section className="library-view meditation-intro" aria-labelledby="meditate-title" data-testid="meditate-view">
        <p className="library-eyebrow">Meditate · silent & still</p>
        <h1 className="library-title" id="meditate-title">A little time in quiet</h1>
        <p className="library-lede">
          Fragments of scripture surface slowly on a dark screen. Nothing to do but read what arrives, and let it pass.
        </p>
        <div className="meditation-length" role="group" aria-label="Session length">
          {[5, 10, 20].map(option => (
            <button
              key={option}
              type="button"
              onClick={() => setMinutes(option)}
              aria-pressed={minutes === option}
            >
              {option} min
            </button>
          ))}
        </div>
        <Dialog.Trigger asChild>
          <button className="library-button" type="button" onClick={begin} data-testid="begin-meditation">
            Begin sitting
          </button>
        </Dialog.Trigger>
      </section>

      <Dialog.Portal>
        <Dialog.Overlay className="meditation-overlay" />
        <Dialog.Content className="meditation-stage">
          <Dialog.Title className="sr-only">Meditation session</Dialog.Title>
          <Dialog.Description className="sr-only">A timed scripture meditation session</Dialog.Description>
          <Dialog.Close asChild>
            <button className="meditation-exit" type="button">End session</button>
          </Dialog.Close>
          {completed ? (
            <div className="meditation-complete">
              <strong>Be still.</strong>
              <span>Your sitting is complete</span>
              <Dialog.Close asChild>
                <button type="button">Return</button>
              </Dialog.Close>
            </div>
          ) : (
            <>
              <p key={fragmentIndex} className="meditation-fragment">{fragments[fragmentIndex]}</p>
              <time className="meditation-timer">{time}</time>
            </>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
