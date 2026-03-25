# theme-system — Architecture Design

_Owner: @3design | Updated: 2026-03-25_

## Architecture Overview

```
web/
├── styles/
│   └── themes.css          ← CSS custom-property definitions
├── hooks/
│   └── useTheme.ts         ← state + localStorage + data-theme side-effect
├── components/
│   └── ThemeSelector.tsx   ← controlled <select> dropdown
└── App.tsx                 ← imports themes.css, useTheme(); renders ThemeSelector
```

## CSS Token Design

All colour tokens are namespaced `--color-*` to avoid collision with the
legacy `--os-*` tokens in `index.html`.

| Token | Purpose |
|---|---|
| `--color-bg` | Page/desktop background |
| `--color-surface` | Window / card surface |
| `--color-border` | Border colour |
| `--color-accent` | Primary interactive accent |
| `--color-text` | Body text |
| `--color-text-muted` | Secondary / muted text |
| `--color-taskbar-bg` | Taskbar background (semi-transparent) |
| `--color-window-bg` | Window chrome bg |
| `--color-window-header` | Window title-bar bg |
| `--color-btn-bg` | Button default background |
| `--color-btn-hover` | Button hover background |

## Hook Contract

```typescript
export type Theme = 'dark' | 'light' | 'retro';

export function useTheme(): {
  theme: Theme;
  setTheme: (t: Theme) => void;
}
```

Side-effects of `setTheme`:
1. Updates React state.
2. Writes `localStorage.setItem('nebula-theme', theme)`.
3. Calls `document.documentElement.setAttribute('data-theme', theme)`.

## Component Contract

`ThemeSelector` renders a single `<select>` with three `<option>` elements:
- value `dark` → "Dark"
- value `light` → "Light"  
- value `retro` → "Retro Terminal"

It calls `useTheme()` internally to read and write the current theme.

## Persistence

Storage key: `nebula-theme` (consistent with other NebulaOS storage keys prefixed
`nebula-`). Default value: `'dark'`.
