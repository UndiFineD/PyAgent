# agent-timeout-watchdog — Project Overview

**ID:** prj0000068  
**Name:** agent-timeout-watchdog  
**Branch:** prj0000068-agent-timeout-watchdog  
**Priority:** P3  
**Budget:** M  
**Tags:** agents, reliability, watchdog

## Goal
Provide a configurable per-agent execution timeout with graceful shutdown, a retry budget, and a dead-letter queue (DLQ) for tasks that exhaust their retry budget.

## Scope boundary
- **New file:** `backend/watchdog.py` — `AgentWatchdog` class
- **Modified:** `backend/app.py` — expose `GET /api/watchdog/status` endpoint
- **New file:** `tests/test_watchdog.py` — 6 tests

Out of scope: persistent DLQ storage, frontend UI, Rust acceleration.

## Branch Plan
`prj0000068-agent-timeout-watchdog`

## Handoff rule
Merge only after all 6 tests pass and PR is approved.

## Failure rule
If tests fail, return to @6code before creating PR.


## Legacy Project Overview Exception

This project overview predates the modern Project Identity / Goal and Scope / Branch Plan
template. It was authored with an earlier workflow format and has not been migrated.
The project was completed successfully; the deviation is a documentation formatting issue only.

Migration to the modern template is on record with @0master.
