import React from 'react';
import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { ReadView } from './components/library/ReadView';
import { ScriptureVerseCard } from './components/library/ScriptureVerseCard';

// These integration-style interactions render the complete reader. Give slow
// CI hosts headroom without removing any waits or behavioural assertions.
jest.setTimeout(15000);

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

const nativeAudio = window.Audio;

function installSpeechSynthesis(voices = []) {
  const listeners = new Set();
  const synth = {
    getVoices: jest.fn(() => voices),
    addEventListener: jest.fn((event, listener) => {
      if (event === 'voiceschanged') listeners.add(listener);
    }),
    removeEventListener: jest.fn((event, listener) => {
      if (event === 'voiceschanged') listeners.delete(listener);
    }),
    speak: jest.fn(),
    cancel: jest.fn(),
  };

  class MockSpeechSynthesisUtterance {
    constructor(text) {
      this.text = text;
    }
  }

  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: synth,
  });
  Object.defineProperty(window, 'SpeechSynthesisUtterance', {
    configurable: true,
    value: MockSpeechSynthesisUtterance,
  });
  return synth;
}

beforeEach(() => {
  // The app now opens on the short-reading feed, so tests that assert on the
  // daily verse must ask for that view explicitly rather than rely on default.
  window.history.replaceState(null, '', '/#today');
  window.localStorage.clear();
  window.scrollTo = jest.fn();
  window.matchMedia = jest.fn().mockReturnValue({ matches: true });
  installSpeechSynthesis();
  global.fetch = jest.fn().mockImplementation(url => Promise.resolve({
    ok: true,
    json: async () => (
      url === '/audio-manifest.json'
        ? { version: 1, clips: [] }
        : scriptureFixture
    ),
  }));
});

afterEach(() => {
  jest.restoreAllMocks();
  Object.defineProperty(window, 'Audio', {
    configurable: true,
    value: nativeAudio,
  });
});

test('loads the public reader and searches scripture from Explore', async () => {
  const user = userEvent.setup({ delay: null });
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
  const user = userEvent.setup({ delay: null });
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
  const user = userEvent.setup({ delay: null });
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

test('Read starts at the catalogue, preserves a resume point, and pages accessibly', async () => {
  const user = userEvent.setup({ delay: null });
  const readData = {
    texts: [{
      id: 'test-text',
      name: 'Test Text',
      complete: true,
      tv: 2,
    }],
    verses: [
      {
        ...scriptureFixture.verses[0],
        id: 'test-text-1-1',
        tid: 'test-text',
        tn: 'Test Text',
        ch: 1,
        vn: 1,
        cn: 'First',
      },
      {
        ...scriptureFixture.verses[0],
        id: 'test-text-2-1',
        tid: 'test-text',
        tn: 'Test Text',
        ch: 2,
        vn: 1,
        cn: 'Second',
      },
    ],
    chapterMeta: {
      'test-text': {
        1: { tr: 'First' },
        2: { tr: 'Second' },
      },
    },
  };
  window.localStorage.setItem('ds_reading', JSON.stringify({ tid: 'test-text', ch: 99 }));

  render(
    <ReadView
      data={readData}
      savedIds={new Set()}
      onToggleSaved={jest.fn()}
      onCopied={jest.fn()}
    />,
  );

  expect(screen.getByRole('heading', { name: 'Read a text from beginning to end' })).toBeVisible();
  expect(screen.getByTestId('read-resume')).toHaveTextContent('Continue Test Text');
  expect(screen.getByTestId('read-resume')).toHaveTextContent('Chapter 2');

  await user.click(screen.getByTestId('read-text-test-text'));
  const firstChapter = screen.getByRole('heading', { name: 'Chapter 1 of 2 · First' });
  expect(firstChapter).toBeVisible();
  expect(firstChapter).toHaveFocus();

  await user.click(screen.getByTestId('read-next'));
  const secondChapter = screen.getByRole('heading', { name: 'Chapter 2 of 2 · Second' });
  expect(secondChapter).toHaveFocus();
  expect(JSON.parse(window.localStorage.getItem('ds_reading'))).toEqual({
    tid: 'test-text',
    ch: 2,
  });

  await user.click(screen.getByTestId('read-back'));
  expect(screen.getByRole('heading', { name: 'Read a text from beginning to end' })).toHaveFocus();
  expect(screen.getByTestId('read-resume')).toHaveTextContent('Chapter 2');
  expect(window.localStorage.getItem('ds_reading')).not.toBe('null');

  await user.click(screen.getByTestId('read-resume'));
  expect(screen.getByRole('heading', { name: 'Chapter 2 of 2 · Second' })).toHaveFocus();
});

test('speech controls share voice discovery and hide unsupported scripts', async () => {
  const user = userEvent.setup({ delay: null });
  const englishVoice = { lang: 'en-GB', name: 'English' };
  const hindiVoice = { lang: 'hi-IN', name: 'Hindi' };
  const synth = installSpeechSynthesis([englishVoice, hindiVoice]);
  const verses = Array.from({ length: 6 }, (_, index) => ({
    ...scriptureFixture.verses[0],
    id: `gita-2-${55 + index}`,
    vn: 55 + index,
  }));

  render(
    <>
      {verses.map(verse => (
        <ScriptureVerseCard
          key={verse.id}
          verse={verse}
          saved={false}
          onToggleSaved={jest.fn()}
          onCopied={jest.fn()}
        />
      ))}
    </>,
  );

  expect(synth.addEventListener).toHaveBeenCalledTimes(1);
  // One initial read per card plus one shared read when the browser listener
  // attaches: mounting more cards must not republish/read voices quadratically.
  expect(synth.getVoices).toHaveBeenCalledTimes(verses.length + 1);
  const firstCard = screen.getByTestId('verse-gita-2-55');
  expect(within(firstCard).getByRole('button', { name: 'Listen in English' })).toBeVisible();
  expect(within(firstCard).getByText(scriptureFixture.verses[0].en)).toHaveAttribute('lang', 'en');

  await user.click(within(firstCard).getByRole('button', { name: 'Malayalam' }));
  expect(within(firstCard).queryByRole('button', { name: /Listen in Malayalam/ })).not.toBeInTheDocument();
  expect(within(firstCard).getByText(/രാജവിദ്യാ/).closest('[data-script]')).toHaveAttribute('lang', 'sa-Mlym');
  expect(
    within(firstCard).getByText(
      scriptureFixture.verses[0].en,
      { selector: '.scripture-card__translation' },
    ),
  ).toBeVisible();

  await user.click(within(firstCard).getByRole('button', { name: 'Devanagari' }));
  expect(within(firstCard).getByText(scriptureFixture.verses[0].dev)).toHaveAttribute('lang', 'sa-Deva');
  await user.click(within(firstCard).getByRole('button', { name: 'Listen in Devanagari' }));
  const devanagariUtterance = synth.speak.mock.calls[0][0];
  expect(devanagariUtterance.text).toBe(scriptureFixture.verses[0].dev);
  expect(devanagariUtterance.voice).toBe(hindiVoice);
  expect(devanagariUtterance.lang).toBe('hi-IN');
  act(() => devanagariUtterance.onend());

  await user.click(within(firstCard).getByRole('button', { name: 'English' }));
  await user.click(within(firstCard).getByRole('button', { name: 'Listen in English' }));
  expect(synth.speak).toHaveBeenCalledTimes(2);
  expect(within(firstCard).getByRole('button', { name: 'Stop reading aloud' })).toBeVisible();

  act(() => synth.speak.mock.calls[1][0].onend());
  expect(within(firstCard).getByRole('button', { name: 'Listen in English' })).toBeVisible();
});

test('custom audio receives an AbortSignal and Stop aborts only that playback', async () => {
  const user = userEvent.setup({ delay: null });
  let playbackSignal;
  const onPlayAudio = jest.fn((verse, script, signal) => {
    playbackSignal = signal;
    return new Promise(resolve => signal.addEventListener('abort', resolve, { once: true }));
  });

  render(
    <ScriptureVerseCard
      verse={scriptureFixture.verses[0]}
      saved={false}
      onToggleSaved={jest.fn()}
      onCopied={jest.fn()}
      onPlayAudio={onPlayAudio}
    />,
  );

  await user.click(screen.getByRole('button', { name: 'Listen in English' }));
  expect(onPlayAudio).toHaveBeenCalledWith(scriptureFixture.verses[0], 'en', expect.any(AbortSignal));
  expect(playbackSignal.aborted).toBe(false);

  await user.click(screen.getByRole('button', { name: 'Stop reading aloud' }));
  expect(playbackSignal.aborted).toBe(true);
  await waitFor(() => {
    expect(screen.getByRole('button', { name: 'Listen in English' })).toBeVisible();
  });
});

test('the reader plays a manifest clip and preserves browser-voice hiding for missing clips', async () => {
  const user = userEvent.setup({ delay: null });
  const audioInstances = [];

  class MockAudio {
    constructor(src) {
      this.src = src;
      this.currentTime = 12;
      this.preload = '';
      this.onended = null;
      this.onerror = null;
      this.play = jest.fn().mockResolvedValue();
      this.pause = jest.fn();
      audioInstances.push(this);
    }
  }

  Object.defineProperty(window, 'Audio', {
    configurable: true,
    value: MockAudio,
  });
  global.fetch.mockImplementation(url => Promise.resolve({
    ok: true,
    json: async () => (
      url === '/audio-manifest.json'
        ? {
          version: 1,
          clips: [{
            verse_id: 'gita-2-55',
            script: 'en',
            path: '/audio/gita-2-55.en.mp3',
          }],
        }
        : scriptureFixture
    ),
  }));

  render(<App />);
  const card = await screen.findByTestId('verse-gita-2-55');
  const listen = await within(card).findByRole('button', { name: 'Listen in English' });
  await user.click(listen);

  expect(audioInstances).toHaveLength(1);
  expect(audioInstances[0].src).toBe('/audio/gita-2-55.en.mp3');
  expect(audioInstances[0].preload).toBe('auto');
  expect(audioInstances[0].play).toHaveBeenCalledTimes(1);
  expect(within(card).getByRole('button', { name: 'Stop reading aloud' })).toBeVisible();

  await user.click(within(card).getByRole('button', { name: 'Stop reading aloud' }));
  expect(audioInstances[0].pause).toHaveBeenCalledTimes(1);
  expect(audioInstances[0].currentTime).toBe(0);

  await user.click(within(card).getByRole('button', { name: 'Malayalam' }));
  expect(within(card).queryByRole('button', { name: /Listen in Malayalam/ })).not.toBeInTheDocument();
});
