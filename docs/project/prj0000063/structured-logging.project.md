# structured-logging — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000063
**Short name:** structured-logging
**Project folder:** `docs/project/prj0000063/`
**Branch:** `prj0000063-structured-logging`
**Date:** 2026-03-25

## Project Overview

Replace ad-hoc `print` statements and the default Python logging configuration in
the FastAPI backend with structured JSON logging via `python-json-logger`. Every
log entry carries a `correlation_id` (from the `X-Correlation-ID` request header
or an auto-generated UUID), the request `endpoint` path, `timestamp`, `level`,
and `message`. A `CorrelationIdMiddleware` ensures all responses echo the
correlation ID back to the caller.

## Goal & Scope

**Goal:** JSON structured logging with correlation IDs across all backend requests

**In scope:**
- `backend/logging_config.py` — NEW: JSON formatter + logger factory
- `backend/app.py` — MODIFY: add CorrelationIdMiddleware, structured health-check log
- `backend/requirements.txt` — add `python-json-logger>=2.0.0`
- `tests/test_structured_logging.py` — NEW: 5 tests
- `docs/project/prj0000063/` — 9 project artifacts
- `data/projects.json` — update prj0000063 lane to "Review"
- `docs/project/kanban.md` — move prj0000063 to Review table

**Out of scope:** Agent-side structured logging, log aggregation/shipping, log
rotation, OpenTelemetry integration (see prj0000070)

## Branch Plan

**Expected branch:** `prj0000063-structured-logging`
**Scope boundary:**
  - `docs/project/prj0000063/` — all project artifacts
  - `backend/logging_config.py` — new structured logging module
  - `backend/app.py` — CorrelationIdMiddleware + health log only
  - `backend/requirements.txt` — python-json-logger dependency
  - `tests/test_structured_logging.py` — new test file
  - `data/projects.json` — lane + pr update
  - `docs/project/kanban.md` — lane row update

**Handoff rule:** All 5 tests pass, PR open on GitHub
**Failure rule:** Do not push if tests fail


## Milestones
Legacy milestone details are not specified in this historical document.


## Status
Legacy status details are not specified in this historical document.

