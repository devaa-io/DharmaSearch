import React, { useMemo } from 'react';
import { CANON } from '../../lib/canon';

function statusFor(text) {
  if (!text) return { complete: false, label: 'not yet catalogued' };
  if (text.complete) return { complete: true, label: `complete · ${text.tv} verses` };
  return { complete: false, label: `in pipeline · ${text.tv} verses` };
}

export function CanonView({ texts }) {
  const textsById = useMemo(
    () => Object.fromEntries(texts.map(text => [text.id, text])),
    [texts],
  );
  const completeCount = texts.filter(text => text.complete).length;

  return (
    <section className="library-view" aria-labelledby="canon-title" data-testid="canon-view">
      <p className="library-eyebrow">Context · where this library sits</p>
      <h1 className="library-title" id="canon-title">Where This Fits</h1>
      <p className="library-lede">
        Bhāratīya scripture is vast — this library holds a careful slice of it.
        {' '}{completeCount} of {texts.length} catalogued texts are complete and zero-gap
        verified; the rest are marked as previews or not yet begun.
      </p>

      <div className="canon-tree">
        {CANON.map(division => (
          <div className="canon-division" key={division.id}>
            <div className="canon-division__head">
              <span className="canon-division__label">{division.label}</span>
              <span className="canon-division__note">{division.note}</span>
            </div>
            {division.groups.map(group => (
              <div className="canon-group" key={group.id}>
                <div className="canon-group__head">
                  <span className="canon-group__label">{group.label}</span>
                  {group.note && <span className="canon-group__note">{group.note}</span>}
                </div>
                <div className="roadmap">
                  {group.textIds.map(textId => {
                    const text = textsById[textId];
                    const status = statusFor(text);
                    return (
                      <div className="roadmap__row" key={textId}>
                        <span>{text ? text.name : textId}</span>
                        <strong className={status.complete ? 'is-complete' : ''}>{status.label}</strong>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <p className="canon-footer">
        Structure follows the traditional Śruti / Smṛti / Darśana division. Counts reflect the
        live build.
      </p>
    </section>
  );
}
