# theme-system — Options Analysis

_Owner: @2think | Updated: 2026-03-25_

## Problem Statement

NebulaOS ships with a single hard-coded dark colour scheme. Users want light mode
(day-time legibility) and a retro terminal aesthetic. The solution must be easy to
extend and must survive page refreshes.

## Options Considered

### Option A — CSS Class Toggle (body.theme-X)
**Approach:** Apply `.theme-light` / `.theme-retro` class to `<body>`, define per-class
variable overrides.
**Pros:** Already partially in place (`.theme-dark`, `.theme-retro` defined in index.html).
**Cons:** Class on body is less idiomatic for modern design tokens; harder to scope to
sub-trees; existing `--os-*` variables would need renaming.

### Option B — CSS Custom Properties + data-theme attribute ✅ CHOSEN
**Approach:** Define all colour tokens on `:root`; override with `[data-theme="light"]`
and `[data-theme="retro"]` attribute selectors on `<html>`.
**Pros:** Modern, spec-compliant, easy to cascade, compatible with CSS-in-JS and Tailwind
custom properties. `data-theme` on `<html>` is the industry standard (Radix, shadcn/ui,
Bootstrap v5.3+).
**Cons:** Requires renaming existing `--os-*` variables to `--color-*` names or running
both systems in parallel.

### Option C — CSS Modules per theme
**Approach:** Import a different stylesheet for each theme.
**Pros:** Strong isolation.
**Cons:** Bundle size increase; cannot hot-swap without a page reload; overcomplicated.

## Decision

**Option B** chosen. New `--color-*` token names add a semantic layer. The `[data-theme]`
attribute on `documentElement` is set by the `useTheme` hook on every state change.
### Migration Note
The existing `--os-*` variables in `index.html` are preserved for backward compatibility
with existing Tailwind classes (`bg-os-bg`, `text-os-text`). The new `--color-*` tokens
provide an additive layer for any components authored after this release.
