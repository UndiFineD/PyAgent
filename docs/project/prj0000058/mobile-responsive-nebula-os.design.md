# mobile-responsive-nebula-os — Design
_Owner: @3design | Status: DONE_

## Architecture Overview

The responsive layer is implemented as a standalone CSS file imported at the application
entry point. Semantic class names are added to JSX elements; no Tailwind classes are
modified or removed.

### New Semantic Class Names

| Class | Element | File |
|---|---|---|
| `nebula-desktop` | Root `<div>` wrapper in `App.tsx` | `web/App.tsx` |
| `nebula-taskbar` | Top-bar / taskbar `<div>` in `App.tsx` | `web/App.tsx` |
| `nebula-taskbar-btn` | Per-window taskbar `<button>` in `App.tsx` | `web/App.tsx` |
| `nebula-window` | Window container `<div>` in `Window.tsx` (normal state) | `web/components/Window.tsx` |

### CSS File Structure

```
web/styles/responsive.css
  @media (max-width: 768px)          ← mobile
    .nebula-desktop  { overflow: hidden }
    .nebula-taskbar  { flex-direction: row; flex-wrap: wrap; bottom: 0; ... }
    .nebula-window   { width: 100vw !important; height: 100vh !important; ... }
    .nebula-taskbar-btn { font-size: 11px; padding: 3px 6px; ... }
  @media (769px..1024px)             ← tablet
    .nebula-window   { max-width: 95vw !important; max-height: 85vh !important }
    .nebula-taskbar-btn { font-size: 12px; ... }
```

### Import Point

`web/index.tsx` — Vite resolves CSS imports in TS/JS entry points, injects into `<head>`.

```ts
import './styles/responsive.css';
```

### Specificity Notes

`!important` is used to override Tailwind inline-style-equivalent values and `style={{}}` props
in Window.tsx (width/height/top/left are set inline). Without `!important`, inline styles
would win in the cascade.
