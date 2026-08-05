import React from 'react';
import { Bookmark } from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';

const NAV_ITEMS = [
  ['feed', 'Read a little'],
  ['today', 'Today'],
  ['begin', 'Begin'],
  ['read', 'Read'],
  ['explore', 'Explore'],
  ['meditate', 'Meditate'],
  ['canon', 'Lineage'],
  ['concepts', 'Concepts'],
  ['about', 'About'],
];

export function LibraryHeader({ activeView, onNavigate, savedCount = 0 }) {
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
        <button
          className="theme-toggle"
          type="button"
          onClick={() => onNavigate('saved')}
          aria-label={savedCount > 0 ? `Saved verses (${savedCount})` : 'Saved verses'}
          aria-current={activeView === 'saved' ? 'page' : undefined}
          data-testid="library-saved-link"
        >
          <Bookmark aria-hidden="true" fill={activeView === 'saved' ? 'currentColor' : 'none'} />
        </button>
        <ThemeToggle />
      </div>
    </header>
  );
}
