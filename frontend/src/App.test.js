import React from 'react';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { ScriptureVerseCard } from './components/library/ScriptureVerseCard';

const scriptureFixture = {
  texts: [
    {
      id: 'gita',
      name: 'Bhagavad Gita',
      lang: 'Sanskrit',
      desc: 'A dialogue on action, knowledge and devotion.',
      complete: true,
    },
  ],
  verses: [
    {
      id: 'gita-2-55',
      tid: 'gita',
      tn: 'Bhagavad Gita',
      ch: 2,
      cn: 'The Yoga of Knowledge',
      vn: 55,
      dev: 'प्रजहाति यदा कामान्',
      iast: 'prajahāti yadā kāmān',
      en: 'Steadfast wisdom arises when the mind releases every selfish desire.',
      scripts: { ml: 'രാജവിദ്യാ രാജഗുഹ്യം പവിത്രമിദമുത്തമമ്' },
      kw: ['wisdom'],
      complete: true,
    },
  ],
  begin: [{ id: 'gita-2-55', title: 'Begin here', why: 'A clear first step.' }],
  chapterMeta: {},
};

beforeEach(() => {
  window.history.replaceState(null, '', '/');
  window.localStorage.clear();
  window.scrollTo = jest.fn();
  window.matchMedia = jest.fn().mockReturnValue({ matches: true });
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => scriptureFixture,
  });
});

afterEach(() => {
  jest.restoreAllMocks();
});

test('loads the public reader and searches scripture from Explore', async () => {
  const user = userEvent.setup();
  render(<App />);

  expect(await screen.findByRole('heading', { name: 'A verse for today' })).toBeVisible();
  expect(screen.getByText('Steadfast wisdom arises when the mind releases every selfish desire.')).toBeVisible();
  expect(global.fetch).toHaveBeenCalledWith('/scripture-data.json');

  const primaryNavigation = screen.getByRole('navigation', { name: 'Primary navigation' });
  await user.click(within(primaryNavigation).getByRole('button', { name: 'Explore' }));

  expect(await screen.findByRole('heading', { name: 'Search the scriptures' })).toBeVisible();
  expect(window.location.hash).toBe('#explore');

  await user.type(screen.getByRole('searchbox', { name: 'Search verses in any language' }), 'steadfast wisdom');

  const results = await screen.findByTestId('scripture-results');
  expect(within(results).getByTestId('verse-gita-2-55')).toHaveTextContent(
    'Steadfast wisdom arises when the mind releases every selfish desire.',
  );
  expect(screen.getByText('1 verse across all texts')).toBeVisible();

  const search = screen.getByRole('searchbox', { name: 'Search verses in any language' });
  await user.clear(search);
  await user.type(search, 'രാജവിദ്യാ');

  const malayalamCard = await screen.findByTestId('verse-gita-2-55');
  expect(within(malayalamCard).getByText('രാജവിദ്യാ', { selector: 'mark' })).toBeVisible();
  expect(within(malayalamCard).getByText(/രാജഗുഹ്യം/).closest('[data-script]')).toHaveAttribute('data-script', 'ml');
  expect(within(malayalamCard).getByRole('button', { name: 'Malayalam' })).toHaveAttribute('aria-pressed', 'true');

  const writeText = jest.spyOn(navigator.clipboard, 'writeText').mockResolvedValue();
  await user.click(within(malayalamCard).getByRole('button', { name: 'Copy verse' }));
  const copiedText = writeText.mock.calls[0][0];
  expect(copiedText).toContain('രാജവിദ്യാ രാജഗുഹ്യം പവിത്രമിദമുത്തമമ്');
  expect(copiedText).not.toContain('प्रजहाति यदा कामान्');
});

test('meditation traps focus and restores it after Escape', async () => {
  const user = userEvent.setup();
  window.history.replaceState(null, '', '/#meditate');
  render(<App />);

  const beginSitting = await screen.findByRole('button', { name: 'Begin sitting' });
  await user.click(beginSitting);

  const dialog = await screen.findByRole('dialog', { name: 'Meditation session' });
  expect(dialog).toBeVisible();
  expect(within(dialog).getByRole('button', { name: 'End session' })).toHaveFocus();

  await user.keyboard('{Escape}');

  expect(screen.queryByRole('dialog', { name: 'Meditation session' })).not.toBeInTheDocument();
  expect(beginSitting).toHaveFocus();
});

test('shows and copies a Chapter 0 citation', async () => {
  const user = userEvent.setup();
  const verse = { ...scriptureFixture.verses[0], id: 'gita-0-55', ch: 0, cn: 'Prelude' };
  render(
    <ScriptureVerseCard
      verse={verse}
      saved={false}
      onToggleSaved={jest.fn()}
      onCopied={jest.fn()}
    />,
  );

  expect(screen.getByText(/Chapter 0 · Prelude/)).toBeVisible();

  const writeText = jest.spyOn(navigator.clipboard, 'writeText').mockResolvedValue();
  await user.click(screen.getByRole('button', { name: 'Copy verse' }));

  expect(writeText).toHaveBeenCalledWith(expect.stringContaining('Bhagavad Gita — Chapter 0, Verse 55'));
});
