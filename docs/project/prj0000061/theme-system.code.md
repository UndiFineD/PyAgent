# theme-system — Code Notes

_Owner: @6code | Updated: 2026-03-25_

## Implementation Notes

### themes.css
Defines 11 CSS custom properties across 3 theme contexts:
- `:root` — dark (default, loaded on every page)
- `[data-theme="light"]` — light blue/white palette
- `[data-theme="retro"]` — green-on-black terminal palette

The `:root` block ensures dark theme is the default even before JavaScript runs
(no flash of wrong theme on first paint for dark-preferring users).

### useTheme.ts
Uses `useState` with a lazy initializer to read `localStorage` synchronously
during the first render (avoids FOUT). The `useEffect` fires on every `theme`
change to:
1. Set `document.documentElement.setAttribute('data-theme', theme)` — triggers CSS
2. Write to `localStorage` for persistence

### ThemeSelector.tsx
Simple controlled `<select>` using `useTheme()` internally. Styled minimally for
compatibility with both light and dark contexts using inline Tailwind utilities.

### App.tsx changes
- Added `import './styles/themes.css'`
- Replaced `useState<Theme['id']>('dark')` with `const { theme, setTheme } = useTheme()`
- Added `<ThemeSelector />` to the taskbar right-side controls
- Removed the `document.body.className` effect (replaced by data-theme in useTheme)

### index.tsx changes
- Added `import './styles/themes.css'` at top level for Vite CSS tree-shaking

## Security Notes
- No user input is evaluated. Theme values are validated by TypeScript type system to
  `'dark' | 'light' | 'retro'` literals — safe for use as HTML attributes.
- localStorage ← written only with the three valid literal values.
