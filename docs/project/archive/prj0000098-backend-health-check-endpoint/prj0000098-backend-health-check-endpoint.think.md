# prj0000098-backend-health-check-endpoint - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## Root Cause Analysis
- Idea drift: `GET /health` already exists in `backend/app.py`, but `GET /readyz` and `GET /livez` do not exist.
- Operational contract gap: current health signal is a single liveness-style check and does not separate process liveness from dependency readiness.
- Startup semantics are implicit: backend startup happens via import-time initialization in `backend/app.py` plus `uvicorn.run(...)` in `backend/__main__.py`; there is no explicit readiness gate tied to startup completion.

Policy gate check:
- `docs/project/code_of_conduct.md`: no policy conflict for this scope.
- `docs/project/naming_standards.md`: endpoint naming and test-file naming can remain snake_case-compatible.

Branch gate check:
- Expected branch from project overview: `prj0000098-backend-health-check-endpoint`.
- Observed branch: `prj0000098-backend-health-check-endpoint`.
- Result: PASS.

## Key Findings in backend/app.py
- `GET /health` already exists and is intentionally mounted on `app` (not auth router), matching load-balancer-friendly behavior.
- `RateLimitMiddleware` exempts `/health` (see `backend/rate_limiter.py`), so health probes are not throttled.
- Middleware currently adds correlation IDs and API version/deprecation headers; health path is unversioned and outside auth-protected routing.
- Runtime starts with import-time setup (`setup_logging()`, store/session initialization) and is served via `python -m backend` in `backend/__main__.py`.
- There is currently no `/readyz` or `/livez`, and no explicit startup/lifespan readiness state machine.

## Research Coverage
Task types covered across options:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

Core evidence references:
- `backend/app.py`
- `backend/__main__.py`
- `backend/rate_limiter.py`
- `tests/test_backend_worker.py`
- `tests/test_rate_limiting.py`
- `tests/test_structured_logging.py`
- `docs/project/prj0000054/backend-authentication.design.md`
- `docs/project/prj0000064/rate-limiting-middleware.design.md`
- `docs/project/prj0000020/github-import.plan.md`
- `docs/architecture/archive/9operations-observability.md`

## Options
### Option A - Additive Probe Endpoints in `backend/app.py` (minimal-first)
Approach:
- Keep current `GET /health` behavior unchanged for compatibility.
- Add `GET /livez` as process-liveness-only (fast local signal).
- Add `GET /readyz` as lightweight readiness signal (internal checks only in v1).
- Add focused tests in existing backend HTTP test modules.

Task-type evidence:
- Literature review: `backend/README.md` and current app routing show `/health` as existing contract.
- Prior art: `docs/project/prj0000054/backend-authentication.design.md` and `docs/project/prj0000064/rate-limiting-middleware.design.md` preserve unauthenticated and exempt health semantics.
- Constraint mapping: no production-wide refactor; endpoint additions only plus related tests.
- Stakeholder impact: backend runtime + CI tests + ops probes; low blast radius.

Pros:
- Lowest implementation risk and fastest testability.
- Preserves existing `/health` semantics relied on by tests and tooling.
- Clear migration path for richer readiness checks later.

Cons:
- Readiness remains intentionally shallow in v1.
- Potential short-term duplication among `/health`, `/livez`, `/readyz` payload semantics.

Risks and testability mapping:
- Risk: Probe contract confusion (M/M). Validation: API contract tests asserting status code and body per endpoint.
- Risk: Accidental auth/rate-limit regression on new endpoints (M/H). Validation: auth-free + no-throttle integration tests mirroring existing `/health` tests.
- Risk: Operational docs drift (M/M). Validation: README/endpoint doc assertion test (or structure check) in follow-up slice.

Rollback:
- Revert newly added `/readyz` and `/livez` handlers and their tests only; keep `/health` unchanged.

### Option B - Health Router + Probe Contract Refactor
Approach:
- Introduce a dedicated probe router (for `/health`, `/livez`, `/readyz`) and move health logic from mixed locations to one module.
- Normalize response schema and shared helper functions.

Task-type evidence:
- Literature review: current route layering (`app` + auth router) in `backend/app.py`.
- Alternative enumeration: modular route ownership for maintainability.
- Constraint mapping: larger structural change than required for first slice.
- Stakeholder impact: broader impact to middleware ordering expectations and import paths.

Pros:
- Better long-term structure and ownership.
- Easier to extend with additional dependency checks.

Cons:
- Unnecessary refactor risk for initial delivery.
- Higher chance of regressions on current `/health` behavior.

Risks and testability mapping:
- Risk: Route registration order errors (M/H). Validation: routing table/integration tests for endpoint availability.
- Risk: Middleware/auth behavior drift (M/H). Validation: explicit auth/rate-limit regression tests for all probe endpoints.
- Risk: Refactor churn delays delivery (H/M). Validation: scope gates in plan + focused change-set review.

Rollback:
- Revert router extraction commit(s) and restore existing in-file route declarations.

### Option C - Dependency-Aware Readiness with Startup State
Approach:
- Add explicit startup lifecycle state and perform dependency checks (store, optional downstream services) in `/readyz`.
- Keep `/livez` simple and process-only.

Task-type evidence:
- Literature review: startup/import behavior in `backend/app.py` and `backend/__main__.py`.
- Prior art: observability expectations in `docs/architecture/archive/9operations-observability.md`.
- Constraint mapping: dependency probing can introduce transient failures and slow probes.
- Risk enumeration: readiness false negatives become an availability hazard.

Pros:
- Stronger operational signal for orchestrators.
- Aligns with mature readiness/liveness split.

Cons:
- Highest complexity for first slice.
- Requires careful non-flaky dependency checks and timeouts.

Risks and testability mapping:
- Risk: Flaky readiness due to transient dependency states (H/H). Validation: deterministic unit tests with mocked dependency failures/timeouts.
- Risk: Probe latency spikes (M/M). Validation: response-time threshold test for `/readyz`.
- Risk: Circular startup/readiness coupling (M/H). Validation: startup smoke test asserting readiness transition behavior.

Rollback:
- Disable deep dependency checks behind a feature flag or revert readiness internals to static-pass behavior.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivery speed | High | Medium | Low |
| Blast radius | Low | Medium | High |
| Testability (first slice) | High | Medium | Medium |
| Operational fidelity (day 1) | Medium | Medium | High |
| Regression risk | Low | Medium | High |
| Fit for minimal scope | High | Low | Low |

## Recommendation
**Selected: Option A - Additive Probe Endpoints in `backend/app.py` (minimal-first).**

Why this option:
- It is the smallest safe slice that closes the specific gap (`/readyz`, `/livez`) without destabilizing existing `/health` behavior.
- It is easiest to validate with deterministic tests, using existing health/auth/rate-limit test patterns.
- It preserves backward compatibility for current consumers and creates a clean step-up path toward Option C later.

Minimal, testable first slice for @3design:
1. Keep `GET /health` response unchanged.
2. Add `GET /livez` with static process-liveness response.
3. Add `GET /readyz` with lightweight readiness response (no external network probes in v1).
4. Add/extend tests for status/body/auth/rate-limit behavior of all three endpoints.

Risk/rollback summary:
- Primary risk: endpoint semantics confusion.
- Mitigation: explicit contract tests and short endpoint docs update.
- Rollback: revert only `/readyz` and `/livez` additions and associated tests, retaining existing `/health` path unchanged.

Prior-art references supporting recommendation:
- `docs/project/prj0000054/backend-authentication.design.md`
- `docs/project/prj0000064/rate-limiting-middleware.design.md`
- `tests/test_backend_worker.py`
- `tests/test_rate_limiting.py`

## Open Questions for @3design
- Should `/readyz` return `503` for any local initialization failure, or remain `200` with detail fields in v1?
- Should `/livez` and `/readyz` be added to rate-limit exemption list, or keep only `/health` exempt initially?
- Do we want a shared JSON schema for probe responses now, or defer schema normalization to a follow-up refactor?
- Should API version headers be intentionally excluded from probe endpoints to keep probe contracts minimal?
