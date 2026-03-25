# theme-system — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000061
**Short name:** theme-system
**Project folder:** `docs/project/prj0000061/`
**Branch:** `prj0000061-theme-system`
**Date:** 2026-03-25

## Project Overview

Add a light mode and a retro terminal (green-on-black) theme to NebulaOS.
Use CSS custom properties (variables) on `:root` for the theme colours.
A theme selector dropdown in the NebulaOS toolbar allows switching themes,
with the choice persisted in `localStorage`.

## Goal & Scope

**Goal:** CSS custom-property theme system (dark/light/retro) for NebulaOS
with selector and localStorage persistence.

**In scope:**
- `web/styles/themes.css` — NEW: CSS custom-property theme definitions
- `web/hooks/useTheme.ts` — NEW: useTheme React hook
- `web/components/ThemeSelector.tsx` — NEW: dropdown selector component
- `web/App.tsx` — MODIFY: import themes.css, use useTheme hook, add ThemeSelector
- `web/index.tsx` — MODIFY: import themes.css at top level
- `tests/test_theme_system.py` — NEW: 5 file-content validation tests
- `docs/project/prj0000061/` — 9 project artifacts
- `data/projects.json` — update prj0000061 lane/branch/pr
- `docs/project/kanban.md` — move prj0000061 to Review table

**Out of scope:** Tailwind v3 config migration, system-preference media-query
detection, per-component theme overrides, dark-mode accessibility audit
(see prj0000071)

## Branch Plan

**Expected branch:** `prj0000061-theme-system`
**Scope boundary:**
  - `docs/project/prj0000061/` — all project artifacts
  - `web/styles/themes.css` — theme CSS custom properties
  - `web/hooks/useTheme.ts` — hook
  - `web/components/ThemeSelector.tsx` — component
  - `web/App.tsx` — import + hook + selector wiring
  - `web/index.tsx` — top-level CSS import
  - `tests/test_theme_system.py` — validation tests
  - `data/projects.json` — lane + pr update
  - `docs/project/kanban.md` — lane row update
**Handoff rule:** Tests pass, PR open → hand to @9git reviewer
**Failure rule:** Do not push if tests fail
