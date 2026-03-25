# mobile-responsive-nebula-os — Code Notes
_Owner: @6code | Status: DONE_

## web/styles/responsive.css (NEW)

Two `@media` blocks:

1. `max-width: 768px` — mobile
   - `.nebula-desktop`: `overflow: hidden`
   - `.nebula-taskbar`: horizontal wrapping strip pinned to bottom, `transform: none !important`
   - `.nebula-window`: full-viewport fixed overlay (`100vw × 100vh`, `top/left: 0`, `border-radius: 0`)
   - `.nebula-taskbar-btn`: `font-size: 11px`, `padding: 3px 6px`

2. `min-width: 769px and max-width: 1024px` — tablet
   - `.nebula-window`: `max-width: 95vw`, `max-height: 85vh`
   - `.nebula-taskbar-btn`: `font-size: 12px`

## web/App.tsx Modifications

Three class names added (no existing classes removed):
- Root container `<div>`: appended `nebula-desktop`
- Taskbar `<div>` (top bar): appended `nebula-taskbar`
- Per-window taskbar `<button>`: appended `nebula-taskbar-btn`

## web/components/Window.tsx Modification

One class name added to the normal-state window `<div>`:
- Appended `nebula-window` to the Draggable inner div className

## web/index.tsx Modification

CSS import statement added at the top:
```ts
import './styles/responsive.css';
```

## Key Engineering Decision

`!important` is required on `width`, `height`, `top`, `left` for `.nebula-window` because
`Window.tsx` applies these as inline `style={{}}` props (highest specificity in the cascade).
