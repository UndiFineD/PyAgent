# flm-token-throughput-dashboard — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000060
**Short name:** flm-token-throughput-dashboard
**Project folder:** `docs/project/prj0000060/`
**Branch:** `prj0000060-flm-token-throughput-dashboard`
**Date:** 2026-03-25

## Project Overview

A NebulaOS panel app showing real-time FLM (Federated Language Model) token
throughput data. The backend exposes a `/api/metrics/flm` endpoint with simulated
tokens-per-second telemetry; the frontend charts it with a pure SVG bar chart
(no external chart library) and auto-refreshes every 2 seconds.

## Goal & Scope

**Goal:** Real-time FLM token throughput dashboard in NebulaOS with SVG charts

**In scope:**
- `backend/app.py` — add GET `/api/metrics/flm` (public, no auth)
- `web/apps/FLMDashboard.tsx` — NEW: React panel polling the endpoint, SVG bar chart
- `web/App.tsx` — add `flm-dashboard` case, import, menu entry
- `web/types.ts` — add `'flm-dashboard'` to `AppId`
- `tests/test_flm_dashboard.py` — NEW: 5 endpoint tests
- `docs/project/prj0000060/` — 9 project artifacts
- `data/projects.json` — update prj0000060 lane + branch
- `docs/project/kanban.md` — move prj0000060 to Review

**Out of scope:** Real FLM server integration, historical persistence, WebSocket streaming

## Branch Plan

**Expected branch:** `prj0000060-flm-token-throughput-dashboard`
**Scope boundary:**
  - `docs/project/prj0000060/` — all project artifacts
  - `backend/app.py` — add `/api/metrics/flm` endpoint only
  - `web/apps/FLMDashboard.tsx` — new panel component
  - `web/App.tsx` — add flm-dashboard case + menu entry
  - `web/types.ts` — add 'flm-dashboard' to AppId
  - `tests/test_flm_dashboard.py` — new test file
  - `data/projects.json` — lane + branch update
  - `docs/project/kanban.md` — lane row update
**Handoff rule:** All 5 tests pass, PR open → hand to reviewer
**Failure rule:** If tests fail, stop and report. Do not push broken code.
