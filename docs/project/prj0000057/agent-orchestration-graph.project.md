# agent-orchestration-graph — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000057
**Short name:** agent-orchestration-graph
**Project folder:** `docs/project/prj0000057/`
**Branch:** `prj0000057-agent-orchestration-graph`
**Date:** 2026-03-25

## Project Overview

Add a NebulaOS panel app that visualises the full 10-stage agent workflow
(`0master → 1project → 2think → 3design → 4plan → 5test → 6code → 7exec →
8ql → 9git`) as a horizontal pipeline graph. Each stage box is colour-coded
by status (idle/active/done/error) derived from live log polling. A progress
bar shows the fraction of stages completed and the current project ID (if
any) is displayed in the panel header.

## Goal & Scope

**Goal:** Visual 10-stage agent pipeline graph in NebulaOS reading from
`/api/agent-log/{agent_id}` for each stage, with real-time polling every
3 seconds.

**In scope:**
- `web/apps/OrchestrationGraph.tsx` — NEW: React polling component
- `web/App.tsx` — MODIFY: import + register OrchestrationGraph app
- `web/types.ts` — MODIFY: add `'orchestration'` to AppId union
- `tests/test_orchestration_graph.py` — NEW: 5 backend endpoint tests
- `docs/project/prj0000057/` — 9 project artifacts
- `data/projects.json` — update prj0000057 lane to "Review"
- `docs/project/kanban.md` — move prj0000057 to Review table

**Out of scope:** WebSocket streaming, agent execution, frontend-side routing

## Branch Plan

**Expected branch:** `prj0000057-agent-orchestration-graph`
**Scope boundary:**
  - `docs/project/prj0000057/` — all project artifacts
  - `web/apps/OrchestrationGraph.tsx` — new panel component
  - `web/App.tsx` — register new app (switch case + menu entry)
  - `web/types.ts` — add `'orchestration'` to AppId
  - `tests/test_orchestration_graph.py` — new test file
  - `data/projects.json` — lane + branch update
  - `docs/project/kanban.md` — lane row update
**Handoff rule:** All tests pass, PR open → hand to reviewer
**Failure rule:** If tests fail, stop and report. Do not push broken code.
