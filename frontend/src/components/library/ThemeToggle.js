import React from 'react';
import { Monitor, Moon, Sun } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';

const ICONS = { light: Sun, dark: Moon, system: Monitor };
const LABELS = {
  light: 'Light theme active. Switch to dark.',
  dark: 'Dark theme active. Switch to match system.',
  system: 'Matching system theme. Switch to light.',
};

export function ThemeToggle() {
  const { theme, cycleTheme } = useTheme();
  const Icon = ICONS[theme];

  return (
    <button
      className="theme-toggle"
      type="button"
      onClick={cycleTheme}
      aria-label={LABELS[theme]}
      title={LABELS[theme]}
      data-testid="theme-toggle"
    >
      <Icon aria-hidden="true" />
    </button>
  );
}
