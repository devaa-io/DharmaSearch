import { useCallback, useEffect, useState } from 'react';
import { useStoredState } from './useStoredState';

const THEMES = ['light', 'dark', 'system'];

function systemPrefersDark() {
  return typeof window !== 'undefined'
    && window.matchMedia?.('(prefers-color-scheme: dark)').matches;
}

/** Reading preference: 'light' | 'dark' | 'system', persisted across visits.
 *  Resolves 'system' against the OS preference and stays in sync if that
 *  preference changes while the app is open. */
export function useTheme() {
  const [theme, setStoredTheme] = useStoredState('ds_theme', 'system');
  const [systemDark, setSystemDark] = useState(systemPrefersDark);

  useEffect(() => {
    const media = window.matchMedia?.('(prefers-color-scheme: dark)');
    if (!media) return undefined;
    const onChange = event => setSystemDark(event.matches);
    // Real browsers support addEventListener; older WebKit supports only the
    // deprecated addListener; this project's jsdom test environment supports
    // neither, so system-preference changes just aren't observed there.
    if (typeof media.addEventListener === 'function') {
      media.addEventListener('change', onChange);
      return () => media.removeEventListener('change', onChange);
    }
    if (typeof media.addListener === 'function') {
      media.addListener(onChange);
      return () => media.removeListener(onChange);
    }
    return undefined;
  }, []);

  const resolvedTheme = theme === 'system' ? (systemDark ? 'dark' : 'light') : theme;

  const cycleTheme = useCallback(() => {
    setStoredTheme(current => THEMES[(THEMES.indexOf(current) + 1) % THEMES.length]);
  }, [setStoredTheme]);

  return { theme, resolvedTheme, setTheme: setStoredTheme, cycleTheme };
}
