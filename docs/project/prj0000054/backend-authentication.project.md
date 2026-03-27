# backend-authentication — Project Overview

_Status: IN_SPRINT_
_Owner: @1project | Updated: 2026-03-24_

## Project Identity

**Project ID:** prj0000054
**Short name:** backend-authentication
**Project folder:** `docs/project/prj0000054/`
**Branch:** `prj0000054-backend-authentication`
**Date:** 2026-03-24

## Project Overview

Add API-key and JWT authentication to every REST and WebSocket endpoint in
`backend/app.py`. Currently all endpoints are unauthenticated. This project
implements:

1. **API-key authentication** — `X-API-Key` header, timing-safe comparison via
   `hmac.compare_digest`. Suitable for intra-service calls, CI, and CLI tools.
2. **JWT authentication** — `Authorization: Bearer <token>`, validated with
   PyJWT using HS256. Suitable for user sessions and role-based access.
3. **Combined dependency** — clients may present either credential; both are
   accepted.
4. **WebSocket authentication** — query-param based (`?api_key=` or `?token=`)
   since HTTP headers are unavailable after the WS handshake.
5. **Opt-out /health** — the health-check endpoint remains unauthenticated for
   load-balancer compatibility.

Secrets are read from environment variables (`PYAGENT_API_KEY`, `PYAGENT_JWT_SECRET`).
When neither is configured the system logs a warning and falls into dev-mode pass-through
(backward compatible).

## Goal & Scope

**Goal:** Secure every REST and WebSocket endpoint in `backend/app.py` by adding
API-key and JWT authentication — both credential types accepted — with full backward
compatibility in dev mode (no secrets configured).

**In scope:**
- `backend/app.py` — auth dependencies + guard all endpoints except `/health`
- `backend/auth.py` — NEW: standalone auth module with all helpers
- `tests/test_backend_auth.py` — NEW: auth-specific test suite
- `backend/requirements.txt` — add PyJWT dependency
- `data/projects.json` + `docs/project/kanban.md` — lifecycle updates

**Out of scope:**
- User management / registration
- Token refresh flows
- Frontend login UI changes
- Rate limiting

## Branch Plan

**Expected branch:** `prj0000054-backend-authentication`
**Scope boundary:**
  - `docs/project/prj0000054/` — all project artifacts
  - `backend/app.py` — auth router wiring + WS auth call only
  - `backend/auth.py` — new file
  - `backend/requirements.txt` — add PyJWT only
  - `tests/test_backend_auth.py` — new file
  - `data/projects.json` — prj0000054 lane + branch update only
  - `docs/project/kanban.md` — move prj0000054 lane entry only
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active
branch is `prj0000054-backend-authentication` and changed files stay inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or
ambiguous, return the task to `@0master` before downstream handoff.

## Acceptance Criteria

1. `verify_api_key(expected, provided)` returns True only for exact match (timing-safe).
2. `verify_jwt(token)` returns payload dict on valid token, None on invalid/expired.
3. `require_auth` FastAPI dependency supports API key OR JWT, raises 401 otherwise.
4. All REST endpoints except `/health` and `/ws` require authentication.
5. WebSocket `/ws` authenticates via `?api_key=` or `?token=` query param; closes with code 4401 on failure.
6. Dev-mode (no secrets configured): all requests pass through with logged warning.
7. All existing tests continue to pass.
8. ≥ 10 new auth test cases covering both credential types, WebSocket, and dev-mode.


## Milestones
Legacy milestone details are not specified in this historical document.


## Status
Legacy status details are not specified in this historical document.

