# pm-swot-risk-ui — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-26_

## Project Identity
**Project ID:** prj0000078
**Short name:** pm-swot-risk-ui
**Project folder:** `docs/project/prj0000078/`

## Project Overview
Add two toolbar buttons — **SWOT Analysis** and **Risk Register** — to the `FilterBar`
in `web/apps/ProjectManager.tsx`. Each button opens `docs/project/kanban.md` in the
NebulaOS Editor app, scrolled to the matching `## SWOT Analysis` or `## Risk Register`
section. The sections were added by prj0000076 and currently have no UI access point.

## Goal & Scope
**Goal:** Give the Project Manager UI one-click access to the SWOT Analysis and Risk
Register sections of `kanban.md` without leaving NebulaOS.

**In scope:**
- `web/apps/ProjectManager.tsx` — two new buttons in `FilterBar`
- `web/App.tsx` — thread `openApp` (or a dedicated `openEditor`) callback into
  `ProjectManager` and extend the `editor` case to accept an optional `initialContent`
  / `scrollToSection` prop
- `web/apps/Editor.tsx` — add optional props for pre-loaded content and anchor target

**Out of scope:** modifying `kanban.md` content, any backend routes, new NebulaOS apps,
changes to other apps

## Branch Plan
**Expected branch:** `prj0000078-pm-swot-risk-ui`
**Scope boundary:** `docs/project/prj0000078/`, `web/apps/ProjectManager.tsx`,
`web/apps/Editor.tsx`, `web/App.tsx`, `web/types.ts` (if needed), plus
`docs/project/kanban.md` and `data/projects.json` for lifecycle updates.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch is `prj0000078-pm-swot-risk-ui` and the changed files stay inside the
scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Editor-opening mechanism (investigation findings for @4plan)
- `openApp(appId: AppId)` is defined in `web/App.tsx` — it creates a new window with a
  fresh component instance.
- `ProjectManager` is instantiated as `<ProjectManager />` with **zero** props; no
  `openApp` is passed down to it or to `FilterBar`.
- `Editor` (`web/apps/Editor.tsx`) accepts **no** props — it has a hardcoded default
  string and no way to receive a file path, content, or anchor target.
- The `AppId` type in `web/types.ts` is a simple string union — no params are supported.

**Design tasks for @4plan:**
1. Extend `Editor` to accept optional `initialContent?: string` and
   `scrollToSection?: string` props.
2. Thread an `openEditor(content: string, section: string) => void` callback through
   `App.tsx → ProjectManager → FilterBar`, or use a React context / custom event so
   `ProjectManager` doesn't need a new prop on its public interface.
3. Wire the two `FilterBar` buttons to call that callback with the full text of
   `kanban.md` (fetched via `/api/files/docs/project/kanban.md` or a static import) and
   the target heading string.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Project setup | @1project | DONE |
| M2 | Options skipped (S tier) | — | N/A |
| M3 | Plan finalized | @4plan | |
| M4 | Tests written | @5test | |
| M5 | Code implemented | @6code | |
| M6 | Integration validated | @7exec | |
| M7 | Security clean | @8ql | |
| M8 | Committed | @9git | |

## Acceptance Criteria
1. `docs/project/prj0000078/pm-swot-risk-ui.project.md` exists with branch plan recorded
2. Branch `prj0000078-pm-swot-risk-ui` exists (local, off `main`)
3. `kanban.md` shows `prj0000078` in Discovery lane (with branch column)
4. `data/projects.json` shows `"lane": "Discovery"` for `prj0000078`
5. All existing structure tests pass (`pytest tests/structure/ -x -q`)

## Key Files
- [`web/apps/ProjectManager.tsx`](../../../../web/apps/ProjectManager.tsx) — FilterBar and main component
- [`web/App.tsx`](../../../../web/App.tsx) — `openApp` definition and window management
- [`web/apps/Editor.tsx`](../../../../web/apps/Editor.tsx) — Editor component (no props today)
- [`web/types.ts`](../../../../web/types.ts) — `AppId` union type
- [`docs/project/kanban.md`](../../kanban.md) — source for SWOT / Risk Register content

## Status
_Last updated: 2026-03-26_
Project folder and all stub files created. kanban.md and data/projects.json updated.
Branch `prj0000078-pm-swot-risk-ui` created off `main`. Handing off to @4plan.
