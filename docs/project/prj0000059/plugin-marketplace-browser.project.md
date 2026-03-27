# plugin-marketplace-browser — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000059
**Short name:** plugin-marketplace-browser
**Project folder:** `docs/project/prj0000059/`
**Branch:** `prj0000059-plugin-marketplace-browser`
**Date:** 2026-03-25

## Project Overview

A NebulaOS panel app that displays a marketplace of available agent plugins.
The backend serves a static plugin registry (JSON); the frontend renders plugin
cards with name, description, author, version, tags, and an install/uninstall
toggle. No real install logic — just the UI + backend endpoint.

## Goal & Scope

**Goal:** Plugin marketplace panel in NebulaOS with backend registry endpoint.

**In scope:**
- `backend/app.py` — MODIFY: add `GET /api/plugins` public endpoint
- `web/apps/PluginMarketplace.tsx` — NEW: React panel app
- `web/App.tsx` — MODIFY: add 'plugins' to openApp switch + menu entry
- `web/types.ts` — MODIFY: add 'plugins' to AppId union
- `tests/test_plugin_marketplace.py` — NEW: 5 tests for the backend endpoint
- `docs/project/prj0000059/` — 9 project artifacts
- `data/projects.json` — update prj0000059 lane to "Review"
- `docs/project/kanban.md` — move prj0000059 to Review table

**Out of scope:** Real install logic, plugin sandboxing, plugin version management

## Branch Plan

**Expected branch:** `prj0000059-plugin-marketplace-browser`
**Scope boundary:**
  - `docs/project/prj0000059/` — all project artifacts
  - `backend/app.py` — public plugin registry endpoint only
  - `web/apps/PluginMarketplace.tsx` — new marketplace panel
  - `web/App.tsx` — add 'plugins' case + menu button
  - `web/types.ts` — AppId union extension
  - `tests/test_plugin_marketplace.py` — new test file
  - `data/projects.json` — lane + pr update
  - `docs/project/kanban.md` — lane row update
**Handoff rule:** All tests pass, PR open → hand to reviewer
**Failure rule:** If tests fail, stop and report. Do not push broken code.


## Milestones
Legacy milestone details are not specified in this historical document.


## Status
Legacy status details are not specified in this historical document.

