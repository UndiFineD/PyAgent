# taskbar-config — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-23_

## Project Identity
**Project ID:** prj0000048
**Short name:** taskbar-config
**Project folder:** `docs/project/prj0000048/`

## Project Overview
Add a configurable taskbar/header visibility option to NebulaOS (`web/App.tsx`). Currently the top bar auto-hides after 2 seconds; this project adds a settings toggle that lets the user choose between auto-hide and permanently visible, alongside the existing theme toggle in the dropdown menu.

## Goal & Scope
**Goal:** Introduce a persistent `taskbarAlwaysVisible` config option in the NebulaOS dropdown settings panel so the user can disable the auto-hide behaviour.

**In scope:**
- `web/App.tsx` — add config state, settings toggle UI, and conditional auto-hide logic

**Out of scope:**
- Backend changes
- Tests outside `web/`
- New React component files (separate files)
- Authentication changes

## Branch Plan
**Expected branch:** `prj0000048-taskbar-config`
**Scope boundary:** `docs/project/prj0000048/` and `web/App.tsx` only
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch is `prj0000048-taskbar-config` and the changed files stay inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to `@0master` before downstream handoff.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | |
| M2 | Design confirmed | @3design | |
| M3 | Plan finalized | @4plan | |
| M4 | Tests written | @5test | |
| M5 | Code implemented | @6code | |
| M6 | Integration validated | @7exec | |
| M7 | Security clean | @8ql | |
| M8 | Committed | @9git | |

## Artifacts
| File | Purpose |
|---|---|
| [taskbar-config.project.md](taskbar-config.project.md) | This overview |
| [taskbar-config.think.md](taskbar-config.think.md) | Options exploration |
| [taskbar-config.design.md](taskbar-config.design.md) | Selected design |
| [taskbar-config.plan.md](taskbar-config.plan.md) | Implementation plan |
| [taskbar-config.test.md](taskbar-config.test.md) | Test artifacts |
| [taskbar-config.code.md](taskbar-config.code.md) | Code artifacts |
| [taskbar-config.exec.md](taskbar-config.exec.md) | Execution log |
| [taskbar-config.ql.md](taskbar-config.ql.md) | Security scan results |
| [taskbar-config.git.md](taskbar-config.git.md) | Git summary |

## Status
_Last updated: 2026-03-23_
Branch `prj0000048-taskbar-config` created from `main`. Project folder and all 9 artifact stubs created. Awaiting handoff to `@2think` for options exploration.
