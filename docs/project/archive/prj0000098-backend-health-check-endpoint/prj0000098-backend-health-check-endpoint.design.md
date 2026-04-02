# prj0000098-backend-health-check-endpoint - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-29_

## Selected Option
Option A - Additive probe endpoints in backend/app.py (minimal-first).

Rationale:
- Preserves existing GET /health behavior and compatibility.
- Adds only two new endpoints (GET /livez and GET /readyz) without backend-wide refactor.
- Keeps implementation bounded to backend/app.py, targeted health-check tests, and
	canonical `/v1/...` documentation-path updates tied to this endpoint slice.

## Architecture
### High-level architecture
- Keep probes mounted directly on FastAPI app object in backend/app.py.
- Keep protected API routes on authenticated router unchanged.
- Treat all three probe endpoints as unauthenticated operational probes.
- Keep probe behavior local and fast (no external network calls in first slice).

### Request flow
1. Probe request reaches middleware stack.
2. Endpoint handler executes constant-time local logic.
3. JSON response is returned with endpoint-specific contract.
4. For readiness failure mode, /readyz returns 503 with explicit non-ready payload.

### Component responsibilities
- backend/app.py:
	- Owns route declarations for /health, /livez, /readyz.
	- Owns probe response payload construction.
- backend/rate_limiter.py:
	- Exempts all probe endpoints from rate limiting.
- tests/*health-related files:
	- Verify contract, auth bypass, and rate-limit bypass behavior.

## Interfaces & Contracts
### Endpoint contracts

| Interface ID | Endpoint | Method | Success Status | Failure Status | Response Shape | Auth | Rate Limit |
|---|---|---|---|---|---|---|---|
| IFC-HC-001 | /health | GET | 200 | N/A | {"status": "ok"} | Not required | Exempt |
| IFC-HC-002 | /livez | GET | 200 | N/A | {"status": "ok"} | Not required | Exempt |
| IFC-HC-003 | /readyz | GET | 200 | 503 | 200: {"status": "ok", "ready": true}; 503: {"status": "degraded", "ready": false, "reason": "<machine_readable_reason>"} | Not required | Exempt |

### Contract notes
- /health remains backward-compatible with existing payload exactly: {"status": "ok"}.
- /livez is process liveness only and intentionally mirrors minimal payload.
- /readyz represents readiness semantics:
	- 200 when local startup/ready conditions are met.
	- 503 when local ready condition is not met.
- None of these endpoints are versioned /api routes, and no auth token/API key is required.

## Non-Functional Requirements
- Performance:
	- Probe handlers should be constant-time local checks (target p95 < 20ms in local test environment).
	- No blocking I/O or outbound network calls in first slice.
- Security:
	- Endpoints return non-sensitive operational status only.
	- Endpoints must remain unauthenticated and safe for orchestrator/load-balancer probing.
- Reliability:
	- /health and /livez should be stable 200 unless process is unavailable.
	- /readyz must use deterministic local readiness rule to avoid flaky probe behavior.
- Testability:
	- Each endpoint must have explicit contract assertions for status code + payload shape.
	- Auth and rate-limit bypass behavior must be regression-tested.

## Acceptance Criteria

| AC ID | Requirement | Verification Target |
|---|---|---|
| AC-001 | Existing GET /health behavior remains unchanged (HTTP 200, payload {"status":"ok"}). | tests/test_backend_worker.py and/or tests/test_api_versioning.py |
| AC-002 | GET /livez exists and returns HTTP 200 with payload {"status":"ok"}. | health endpoint tests under tests/ |
| AC-003 | GET /readyz exists and returns HTTP 200 with payload containing status="ok" and ready=true when ready. | health endpoint tests under tests/ |
| AC-004 | GET /readyz returns HTTP 503 with payload containing status="degraded", ready=false, and machine-readable reason when not ready. | readiness negative-path test with controlled condition |
| AC-005 | /health, /livez, and /readyz require no credentials even when auth enforcement is active. | tests/test_backend_auth.py |
| AC-006 | /health, /livez, and /readyz are exempt from rate limiting and never return 429 under burst probe traffic. | tests/test_rate_limiting.py |
| AC-007 | Scope includes backend probe handling plus repo canonical `/v1/...` documentation alignment for affected health-endpoint references. | code review against changed file set |

## Test Targets for Downstream Agents
### @4plan task seeds
- P-001: Add /livez handler in backend/app.py.
- P-002: Add /readyz handler in backend/app.py with explicit 200/503 contract path.
- P-003: Extend probe rate-limit exemption list to include /livez and /readyz.
- P-004: Add/extend health endpoint tests for contract coverage.
- P-005: Add/extend auth bypass tests for /livez and /readyz.
- P-006: Add/extend rate-limit bypass tests for all probe endpoints.

### @5test target files
- tests/test_backend_auth.py
- tests/test_rate_limiting.py
- tests/test_backend_worker.py
- tests/test_api_versioning.py

### @6code target file
- backend/app.py

## Interface-to-Task Traceability

| Interface ID | Contract Summary | Planned Tasks | Test Targets | Owner Phase |
|---|---|---|---|---|
| IFC-HC-001 | Preserve /health contract | P-004 (regression assertions) | tests/test_backend_worker.py, tests/test_api_versioning.py | @5test/@6code |
| IFC-HC-002 | Add /livez 200 + minimal payload + non-auth/non-rate-limit | P-001, P-003, P-004, P-005, P-006 | tests/test_backend_auth.py, tests/test_rate_limiting.py, health endpoint tests | @4plan/@5test/@6code |
| IFC-HC-003 | Add /readyz 200/503 readiness contract + non-auth/non-rate-limit | P-002, P-003, P-004, P-005, P-006 | tests/test_backend_auth.py, tests/test_rate_limiting.py, readiness contract tests | @4plan/@5test/@6code |

## Open Questions
- OQ-001 (non-blocking): Should first-slice /readyz failure reason taxonomy be constrained to a fixed enum now, or allow a single placeholder reason and tighten later?
