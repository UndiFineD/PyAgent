# live-agent-execution-in-codebuilder — Project Overview

_Owner: @1project | Status: DONE_
_Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000062
**Short name:** live-agent-execution-in-codebuilder
**Project folder:** `docs/project/prj0000062/`
**Branch:** `prj0000062-live-agent-execution-in-codebuilder`
**Date:** 2026-03-25

## Goal

Wire the 10-agent pipeline to the CodeBuilder NebulaOS app. Add a "Run Pipeline"
button to CodeBuilder that POSTs task details to a new backend endpoint
`/api/pipeline/run`, then polls per-agent log output every 2 seconds from
`/api/pipeline/status/{pipeline_id}`. Show a per-agent progress list in the
CodeBuilder UI.

## In Scope

- `backend/app.py` — 2 new endpoints: POST `/api/pipeline/run`, GET `/api/pipeline/status/{pipeline_id}`
- `web/apps/CodeBuilder.tsx` — Run Pipeline button, pipeline status panel, 3 new state vars, polling logic
- `tests/test_pipeline_execution.py` — NEW: 5 pipeline endpoint tests
- `docs/project/prj0000062/` — 9 project artifacts
- `data/projects.json` — update prj0000062 entry
- `docs/project/kanban.md` — move prj0000062 lane

## Scope Boundary

- `docs/project/prj0000062/` — all project artifacts
- `backend/app.py` — pipeline run/status endpoints only
- `web/apps/CodeBuilder.tsx` — pipeline UI additions only (non-breaking)
- `tests/test_pipeline_execution.py` — new test file
- `data/projects.json` — prj0000062 lane/branch/pr update
- `docs/project/kanban.md` — lane row update

**Out of scope:** Real agent execution (in-memory demo store only), authentication
changes, WebSocket modifications, other NebulaOS apps.

## Handoff Rule

All 5 tests in `tests/test_pipeline_execution.py` pass. PR open → hand to reviewer.

## Failure Rule

Do not push if tests fail.

## Project Overview

Wire the 10-agent pipeline to the CodeBuilder NebulaOS app with streaming per-agent
log output and progress indicators. Exposes `/api/pipeline/run` and
`/api/pipeline/status/{pipeline_id}` backend endpoints.

## Goal & Scope

**Goal:** Enable live agent pipeline execution from the CodeBuilder UI with
real-time per-agent progress polling.

**In scope:**
- `backend/app.py` — pipeline run + status endpoints
- `web/apps/CodeBuilder.tsx` — Run Pipeline button and status panel
- `tests/test_pipeline_execution.py` — 5 pipeline tests

**Out of scope:** real agent execution, authentication changes, WebSocket changes.

## Branch Plan

**Expected branch:** `prj0000062-live-agent-execution-in-codebuilder`
**Scope boundary:** `docs/project/prj0000062/`, `backend/app.py`, `web/apps/CodeBuilder.tsx`, `tests/test_pipeline_execution.py`
**Handoff rule:** All 5 tests pass; merge after PR review.
**Failure rule:** Return to @6code if tests fail.
