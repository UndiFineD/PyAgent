# prj0000098-backend-health-check-endpoint - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-29_

## Overview
Slice 1 delivers a narrow, test-first health probe expansion with canonicalization
alignment: keep existing `/health` behavior stable, add `/livez` and `/readyz`,
support deterministic degraded readiness for `/readyz`, and align affected docs to
canonical `/v1/...` paths.

Branch gate:
- Expected branch: `prj0000098-backend-health-check-endpoint`
- Observed branch: `prj0000098-backend-health-check-endpoint`
- Result: PASS

Policy gate:
- `docs/project/code_of_conduct.md`: PASS (no conduct/policy conflict in scope).
- `docs/project/naming_standards.md`: PASS (no new non-snake_case file or symbol names planned).

## Scope Boundaries
In scope:
- `GET /health` compatibility protection
- `GET /livez` and `GET /readyz` endpoint delivery
- Related backend tests for endpoint contract, auth bypass, and rate-limit behavior
- Canonical `/v1/...` path alignment in touched docs and provider guidance associated
	with this endpoint work (README/docs/api/providers/github_app)

Out of scope:
- Any non-health route work
- Startup state machines and deep dependency probing
- Frontend runtime feature changes

## Slice 1 Task List (TDD)

### @5test Red Phase Tasks

- [ ] T1 - Add contract red tests for `/livez` and `/readyz` and lock `/health` compatibility  
	Objective: Define failing endpoint-contract expectations before implementation.  
	Files: `tests/test_github_app.py`, `tests/test_api_versioning.py`  
	Acceptance:
	- AC-001: `/health` remains HTTP 200 with `{"status": "ok"}`.
	- AC-002: `/livez` expected HTTP 200 with body `{"status": "alive"}` (fails before green).
	- AC-003: `/readyz` expected HTTP 200 with body `{"status": "ready"}` (fails before green).
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py`
	Pass criteria:
	- Red phase: at least one failing assertion for `/livez` and one for `/readyz` due to missing route.

- [ ] T2 - Add auth-bypass red tests for new probe endpoints  
	Objective: Ensure probes remain accessible without credentials under enforced auth.  
	Files: `tests/test_backend_auth.py`  
	Acceptance:
	- AC-004: `/health`, `/livez`, `/readyz` all return 200 without auth token.
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_auth.py`
	Pass criteria:
	- Red phase: `/livez` and `/readyz` checks fail until endpoints are implemented.

- [ ] T3 - Add rate-limit red tests for new probe endpoints  
	Objective: Lock probe behavior under low rate-limit configuration.
	Files: `tests/test_rate_limiting.py`  
	Acceptance:
	- AC-005: Health probes are not blocked by limiter policy in test harness (`/health`, `/livez`, `/readyz` all 200).
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_rate_limiting.py`
	Pass criteria:
	- Red phase: tests for `/livez` and `/readyz` fail pre-implementation.

### @6code Green Phase Tasks

- [ ] T4 - Implement `/livez` and `/readyz` handlers in backend app  
	Objective: Make red contract/auth tests pass with minimal, deterministic responses.
	Files: `backend/app.py`  
	Acceptance:
	- AC-002 and AC-003 satisfied with exact response payloads.
	- AC-001 remains unchanged for `/health`.
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py tests/test_backend_auth.py`
	Pass criteria:
	- Command exits 0 and all selected tests pass.

- [ ] T5 - Align rate-limit exemption logic for new probe endpoints  
	Objective: Keep probe endpoints consistently probe-safe in limiter behavior.
	Files: `backend/rate_limiter.py`, `tests/test_rate_limiting.py`  
	Acceptance:
	- AC-005 satisfied for all three probe endpoints.
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_rate_limiting.py`
	Pass criteria:
	- Command exits 0 and probe-related rate-limit tests pass.

- [ ] T6 - Run slice-1 narrow regression gate  
	Objective: Verify full scoped behavior before @7exec handoff.
	Files: `backend/app.py`, `backend/rate_limiter.py`, `tests/test_github_app.py`, `tests/test_api_versioning.py`, `tests/test_backend_auth.py`, `tests/test_rate_limiting.py`  
	Acceptance:
	- AC-001 through AC-005 all pass in one run.
	Validation command:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py`
	Pass criteria:
	- Command exits 0 with no failures, errors, or xfails in scoped suites.

## Dependency Order
1. T1 -> T2 -> T3 (all red tests first by @5test)
2. T4 depends on T1-T3
3. T5 depends on T3 and may be completed with T4
4. T6 depends on T4-T5

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Red tests authored and failing as expected | T1-T3 | PLANNED |
| M2 | Green implementation completed | T4-T5 | NOT_STARTED |
| M3 | Slice-1 scoped regression gate passed | T6 | NOT_STARTED |

## Validation Commands
```powershell
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_auth.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_rate_limiting.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py
```

## Handoff Target
- Next agent: `@5test`
- Handoff package for @5test: T1-T3 only (red phase); do not implement production endpoint code.
