import React from 'react';

const NAV_ITEMS = [
  ['today', 'Today'],
  ['begin', 'Begin'],
  ['explore', 'Explore'],
  ['meditate', 'Meditate'],
  ['about', 'About'],
];

export function LibraryHeader({ activeView, onNavigate }) {
  return (
    <header className="library-header">
      <div className="library-header__inner">
        <button
          className="library-brand"
          type="button"
          onClick={() => onNavigate('today')}
          aria-label="DharmaSearch home"
          data-testid="library-brand"
        >
          Dharma<span>Search</span>
        </button>
        <nav className="library-nav" aria-label="Primary navigation">
          {NAV_ITEMS.map(([id, label]) => (
            <button
              key={id}
              className="library-nav__item"
              type="button"
              onClick={() => onNavigate(id)}
              aria-current={activeView === id ? 'page' : undefined}
              data-testid={`library-nav-${id}`}
            >
              {label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
