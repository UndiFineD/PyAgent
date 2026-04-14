import React from 'react';
import { useTheme, Theme } from '../hooks/useTheme';

const THEME_OPTIONS: { value: Theme; label: string }[] = [
  { value: 'dark', label: 'Dark' },
  { value: 'light', label: 'Light' },
  { value: 'retro', label: 'Retro Terminal' },
];

export function ThemeSelector() {
  const { theme, setTheme } = useTheme();

  return (
    <select
      value={theme}
      onChange={(e) => setTheme(e.target.value as Theme)}
      className="text-xs rounded px-2 py-1 bg-os-window border border-os-border text-os-text cursor-pointer focus:outline-none focus:ring-1 focus:ring-os-accent"
      aria-label="Select theme"
    >
      {THEME_OPTIONS.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}
