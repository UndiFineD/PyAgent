# project-management — Project Overview

_Status: HANDED_OFF_
_Owner: @1project | Updated: 2026-03-24_

## Project Identity

**Project ID:** prj0000052
**Short name:** project-management
**Project folder:** `docs/project/prj0000052/`
**Branch:** `prj0000052-project-management`
**Date:** 2026-03-24

## Project Overview

This project delivers a comprehensive project lifecycle management system for PyAgent.
It introduces a Kanban board (`docs/project/kanban.md`) as the single source of truth for all
51 existing projects plus future ideas, a fully functional React app (`web/apps/ProjectManager.tsx`)
in the NebulaOS desktop, a `GET /api/projects` FastAPI endpoint, a `data/projects.json` static
data file, and updated agent definition files so that `@0master` and `@1project` reference the
Kanban board as the primary coordination artifact going forward.

## Goal & Scope

**Goal:** Replace ad-hoc project tracking with a structured, agile-friendly Kanban lifecycle
board visible inside NebulaOS and maintained in source control, so that every PyAgent project
(past, present, and future) has an authoritative status visible to all agents and contributors.

**In scope:**
- `docs/project/kanban.md` — canonical Kanban board (all 51 projects + 10 ideas)
- `web/apps/ProjectManager.tsx` — React Kanban UI in NebulaOS
- `backend/app.py` — new `GET /api/projects` endpoint
- `data/projects.json` — static JSON with all 51 projects + 10 ideas
- `.github/agents/1project.agent.md` — reference kanban.md as lifecycle board
- `.github/agents/0master.agent.md` — reference kanban.md as coordination artifact
- `docs/project/prj0000052/` — all 9 workflow artifacts for this project

**Out of scope:**
- Changes to `src/`, `rust_core/`, or `tests/` (except structure tests for new files)
- Database changes — projects.json is the data source (no DB)
- Authentication or access control for the `/api/projects` endpoint
- Drag-and-drop lane movement (read-only Kanban in v1; advancement via git)
- Changes to any other project folder

## Branch Plan

**Expected branch:** `prj0000052-project-management`
**Scope boundary:**
  - `docs/project/prj0000052/` — all project artifacts
  - `docs/project/kanban.md` — new Kanban board
  - `web/apps/ProjectManager.tsx` — new React component
  - `backend/app.py` — add `/api/projects` endpoint only
  - `data/projects.json` — new static data file
  - `.github/agents/0master.agent.md` — reference update only
  - `.github/agents/1project.agent.md` — reference update only
  - `tests/structure/test_project_manager.py` — structural tests for new files
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active
branch is `prj0000052-project-management` and changed files stay inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or
ambiguous, return the task to `@0master` before downstream handoff.

## Deliverables & Acceptance Criteria

### D1 — `docs/project/kanban.md`
- Shows all 51 existing projects (prj0000001–prj0000051) sorted into lifecycle lanes
- Includes "Project Ideas" lane with 10 future roadmap items (prj0000053–prj0000062 as placeholders)
- Lifecycle lanes: **Ideas | Discovery | Design | In Sprint | Review | Released | Archived**
- A table per lane: columns `prj ID | Name | Summary | Priority | Budget Tier | Branch | PR`
- Instructions section at the top explaining lanes, advancement rules, and governance
- Agile-friendly (sprint-based), PRINCE2-safe (stage gates, risk notes, budget column)

### D2 — `web/apps/ProjectManager.tsx`
- React component exported as `ProjectManager` (named export)
- Multiple swim lanes matching the kanban.md structure (7 lanes)
- Project cards: prj ID, name, stage badge, summary (truncated), priority badge, budget tier
- Filter by lane (dropdown), search by name or prj ID (text input)
- Matches NebulaOS dark theme (consistent with `Conky.tsx`, `AgentChat.tsx` styling)
- Fetches from `GET /api/projects` on mount; handles loading spinner and error state
- No drag-and-drop in v1 (read-only Kanban; lane changes go via git)

### D3 — `backend/app.py` endpoint
- New route: `GET /api/projects`
- Reads `data/projects.json` at startup and returns the full array as JSON
- Project schema: `{ id, name, lane, summary, branch, pr, priority, budget_tier }`
- Returns HTTP 200 with `application/json` response; HTTP 500 with message on read error
- Consistent with existing FastAPI patterns (router, CORS already configured)

### D4 — `data/projects.json`
- Valid JSON array of project objects
- All 51 released/active projects + 10 idea-lane entries (total ≥ 61 entries)
- Each entry: `{ "id": "prj0000001", "name": "...", "lane": "Released", "summary": "...",
  "branch": "...", "pr": "#NNN or null", "priority": "P1|P2|P3", "budget_tier": "S|M|L|XL" }`
- `lane` must be one of: `Ideas | Discovery | Design | In Sprint | Review | Released | Archived`

### D5 — `.github/agents/1project.agent.md` update
- Add guidance that `docs/project/kanban.md` is the project lifecycle board
- Document which lane new projects start in (Discovery) and how they advance
- No other behavioural changes to the agent spec

### D6 — `.github/agents/0master.agent.md` update
- Reference `docs/project/kanban.md` as the primary project coordination artifact
- Instruct master to update the kanban lane when assigning a new project ID
- No other behavioural changes to the agent spec

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
| M8 | Committed & PR merged | @9git | |

## Existing Project Context

All 51 existing projects are tracked:
- **Released (MERGED):** prj0000001–prj0000042, prj0000045, prj0000047–prj0000051
- **In Progress / Check:** prj0000043 (p2p-security-deps, PR open), prj0000044 (transaction-managers, PR #136 open)
- **Stalled:** prj0000046 (flm-tps-benchmark, FLM server offline)
- **Missing local dirs:** prj0000043 and prj0000044

The 10 future roadmap ideas (placeholder IDs prj0000053–prj0000062):
1. prj0000053 — HMAC webhook auth
2. prj0000054 — Backend JWT auth layer
3. prj0000055 — WebSocket E2E encryption
4. prj0000056 — Copilot review integration
5. prj0000057 — NebulaOS notification system
6. prj0000058 — Agent swarm dashboard (extends this project)
7. prj0000059 — Project status webhook broadcasts
8. prj0000060 — Multi-repository agent support
9. prj0000061 — Automated changelog generation
10. prj0000062 — Performance regression CI gate

## Codebase Patterns Reference

- **React apps:** `web/apps/*.tsx` — named exports, dark NebulaOS theme
- **Backend:** FastAPI `backend/app.py` — existing endpoints: `/health`, `/api/metrics/system`,
  `/api/agent-log/{id}`, `/api/agent-doc/{id}`, `WS /ws`
- **Shell:** PowerShell only; `rg` available for regex search
- **Testing:** `pytest src/`; structure tests in `tests/structure/`

## Canonical Artifact Links

| Artifact | File |
|---|---|
| Options | `docs/project/prj0000052/project-management.think.md` |
| Design | `docs/project/prj0000052/project-management.design.md` |
| Plan | `docs/project/prj0000052/project-management.plan.md` |
| Tests | `docs/project/prj0000052/project-management.test.md` |
| Code | `docs/project/prj0000052/project-management.code.md` |
| Execution | `docs/project/prj0000052/project-management.exec.md` |
| Security | `docs/project/prj0000052/project-management.ql.md` |
| Git | `docs/project/prj0000052/project-management.git.md` |

## Status

_Last updated: 2026-03-24_
Project folder and all 9 stub artifacts created and committed (2903ff990 on `prj0000052-project-management`).
Handed off to @2think for options exploration.
