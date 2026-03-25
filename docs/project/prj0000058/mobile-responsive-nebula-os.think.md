# mobile-responsive-nebula-os — Think / Analysis
_Owner: @2think | Status: DONE_

## Existing NebulaOS Shell Analysis

The NebulaOS frontend (`web/App.tsx`, `web/components/Window.tsx`) uses **Tailwind CSS utility
classes** exclusively. There are no semantic class names like `.window` or `.taskbar` —
all styling is applied via inline className strings such as:

```
"fixed top-0 left-0 right-0 h-12 bg-os-header/90 backdrop-blur-md ..."
```

A CSS media-query file cannot target Tailwind utility classes portably (they may be
purged or renamed). The correct approach is to add semantic class names to the React
components and target those in the responsive CSS.

## Approach Considered

| Option | Pros | Cons |
|---|---|---|
| Tailwind `sm:` / `md:` breakpoint prefixes | Zero extra files | Requires editing every className string; couples breakpoints to component rendering |
| Custom CSS + semantic class names | Clean separation; testable as file content | Requires adding class names to JSX elements |
| CSS-in-JS (styled-components / emotion) | Scoped styles | Heavy dependency, not in current stack |

## Decision: Custom CSS + Semantic Class Names

- Add `nebula-desktop`, `nebula-taskbar`, `nebula-taskbar-btn`, `nebula-window` class names to JSX
- Create `web/styles/responsive.css` with `@media` rules targeting those names
- Import the CSS in `web/index.tsx` (Vite handles CSS imports from JS/TS entry points)
- This approach is framework-agnostic, tree-shakeable, and easy to validate in Python tests

## CSS Strategy

### Mobile (≤768 px)
- Taskbar moves to bottom, wraps items horizontally
- All windows become `fixed`, width/height `100vw`/`100vh`
- Taskbar buttons shrink (11 px, tighter padding)

### Tablet (769–1024 px)
- Windows constrained to `max-width: 95vw`, `max-height: 85vh`
- Taskbar buttons slightly smaller (12 px)
