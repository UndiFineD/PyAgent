# prj0000098-backend-health-check-endpoint - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-29_

## Implementation Summary
Implemented minimal backend probe support in scope:
- Added no-auth probe routes in backend app: GET /livez -> {"status":"alive"}, GET /readyz -> {"status":"ready"}
- Kept existing GET /health contract unchanged: 200 + {"status":"ok"}
- Expanded rate-limit bypass set to include /livez and /readyz with /health
- Updated probe-focused tests for contract, auth bypass, and rate-limit exemption behavior

## Acceptance Criteria Evidence
| AC ID | Changed module/file | Validating tests | Status |
|---|---|---|---|
| AC-001 | backend/app.py | tests/test_api_versioning.py::test_v1_health_unversioned_still_works; tests/test_backend_auth.py::test_health_no_auth_always_200 | PASS |
| AC-002 | backend/app.py | tests/test_api_versioning.py::test_livez_unversioned_still_works | PASS |
| AC-003 | backend/app.py | tests/test_api_versioning.py::test_readyz_unversioned_still_works | PASS |
| AC-004 | backend/app.py; tests/test_backend_auth.py | tests/test_backend_auth.py::test_health_no_auth_always_200; tests/test_backend_auth.py::test_livez_no_auth_always_200; tests/test_backend_auth.py::test_readyz_no_auth_always_200 | PASS |
| AC-005 | backend/rate_limiter.py; tests/test_rate_limiting.py | tests/test_rate_limiting.py::test_probe_paths_exempt_from_rate_limit | PASS |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| backend/app.py | Add /livez and /readyz probe handlers | +14/-0 |
| backend/rate_limiter.py | Expand probe exemption list to include /livez and /readyz | +4/-3 |
| tests/test_api_versioning.py | Add /livez and /readyz contract assertions | +14/-0 |
| tests/test_backend_auth.py | Add probe no-auth assertions for /livez and /readyz | +28/-1 |
| tests/test_rate_limiting.py | Consolidate probe path limiter bypass checks | +28/-15 |

## Test Run Results
```
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py
33 passed in 3.90s

c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_github_app.py tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py
52 passed in 4.62s

c:/Dev/PyAgent/.venv/Scripts/python.exe -m ruff check backend/rate_limiter.py tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py
PASS (no lint violations)

c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q
FAIL (1 unrelated baseline doc-policy failure):
tests/docs/test_agent_workflow_policy_docs.py::test_git_summaries_use_modern_branch_plan_format_or_carry_legacy_exception
Reason: docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md is missing required "## Branch Plan" section.

rg --type py "raise NotImplementedError|raise NotImplemented\b|#\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" backend/app.py backend/rate_limiter.py tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py
rg --type py "^\s*\.\.\.\s*$" backend/app.py backend/rate_limiter.py
PASS (no matches)
```

## Deferred Items
- Repository-wide full pytest remains red due to pre-existing docs workflow policy in prj0000098 .git artifact.
- This @6code pass intentionally kept scope to backend probe implementation and directly-related tests/helpers.

## Blocker Remediation Follow-up (2026-03-29)

### Implementation Summary
- Added deterministic degraded readiness path for `/v1/readyz` and legacy `/readyz` via `PYAGENT_READYZ_FORCE_DEGRADED=1` (and optional `app.state.readyz_degraded_reason` override), returning HTTP 503 with explicit reason.
- Preserved existing ready behavior when not degraded: HTTP 200 with `{"status": "ready"}`.
- Added coverage in `tests/test_api_versioning.py` for degraded behavior on both canonical and legacy paths.
- Updated prj0000098 project/design/plan/git scope text to include canonical `/v1/...` alignment work and added required modern `## Branch Plan` section in git artifact.

### Acceptance Criteria Evidence (Follow-up)
| AC ID | Changed module/file | Validating tests | Status |
|---|---|---|---|
| AC-003 | backend/app.py | tests/test_api_versioning.py::test_v1_readyz_routable | PASS |
| AC-004 | backend/app.py; tests/test_api_versioning.py | tests/test_api_versioning.py::test_readyz_degraded_when_forced[/v1/readyz]; tests/test_api_versioning.py::test_readyz_degraded_when_forced[/readyz] | PASS |
| AC-007 | docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.project.md; docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.design.md; docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.plan.md; docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md | tests/docs/test_agent_workflow_policy_docs.py (targeted rerun by @7exec/@8ql) | READY |

### Requested Regression Command Result
```powershell
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -v tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py tests/test_backend_worker.py tests/test_structured_logging.py tests/test_github_app.py tests/test_providers_flm.py tests/structure/test_readme.py::test_backend_endpoints
85 passed in 6.12s
```
