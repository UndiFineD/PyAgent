# openapi-spec-generation - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-03_

## Test Plan
Author a narrow red-phase contract for the backend-only OpenAPI drift lane. The test scope is intentionally limited to
`tests/docs/test_backend_openapi_drift.py`, where `backend.app` is the only allowed schema authority. The selector must
fail via assertion-level contract checks when the committed artifact is missing or stale, and it must prove the drift
path stays read-only instead of regenerating files during pytest runs.

## Branch and Scope Preconditions
- Expected branch: prj0000120-openapi-spec-generation
- Observed branch: prj0000120-openapi-spec-generation
- Project match: PASS
- Scope-bounded files reviewed:
	- `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.test.md`
	- `tests/docs/test_backend_openapi_drift.py`
	- `.github/agents/data/current.5test.memory.md`
	- `.github/agents/data/2026-04-03.5test.log.md`
- Required evidence:
	- `git branch --show-current`

## AC-to-Test Matrix
| AC ID | Requirement Summary | Test Case ID | Selector(s) |
|---|---|---|---|
| AC-OAS-001 | Explicit backend-only generator command exists. | TC-OAS-901 | `python scripts/generate_backend_openapi.py` (downstream @6code validation target) |
| AC-OAS-002 | Committed artifact path and deterministic serialization are fixed. | TC-OAS-902 | `python scripts/generate_backend_openapi.py` plus git diff review on `docs/api/openapi/backend_openapi.json` (downstream @6code validation target) |
| AC-OAS-003 | Drift detection is read-only and fails on semantic mismatch. | TC-OAS-001, TC-OAS-002 | `tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_committed_backend_artifact_exists_with_semantic_shape`, `tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_drift_check_is_read_only_and_semantic` |
| AC-OAS-004 | CI enforcement stays lightweight and generation-free. | TC-OAS-904 | `rg -n "test_backend_openapi_drift.py|pytest .*backend_openapi_drift|mkdocs build|generate_backend_openapi" .github/workflows/ci.yml` (downstream @6code validation target) |
| AC-OAS-005 | Docs publication remains consumer-only. | TC-OAS-905 | `rg -n "openapi/backend_openapi.json|OpenAPI|backend schema" docs/api/index.md` (downstream @6code validation target) |
| AC-OAS-006 | Phase-one scope remains backend-only. | TC-OAS-003 | `tests/docs/test_backend_openapi_drift.py::test_ac_oas_006_drift_lane_imports_backend_app_only` |

## Weak-Test Detection Gate
- Block handoff to @6code if any selector can pass against a placeholder/stub implementation or by asserting only file existence/importability.
- Reject tests that only assert `is not None`, `isinstance(...)`, or no-exception behavior without validating schema semantics.
- Reject tests that regenerate files as a side effect of the drift selector.
- Reject tests that use `assert True`, TODO placeholders, or import-only smoke coverage.
- Red-phase evidence is valid only when failures are assertion-level contract failures, not `ImportError` or `AttributeError`.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-OAS-001 | The committed backend OpenAPI artifact exists and contains real backend schema content. | tests/docs/test_backend_openapi_drift.py | RED_CONFIRMED |
| TC-OAS-002 | The drift check compares committed vs generated backend schema in read-only mode. | tests/docs/test_backend_openapi_drift.py | RED_CONFIRMED |
| TC-OAS-003 | The drift lane imports `backend.app` only and excludes secondary FastAPI apps. | tests/docs/test_backend_openapi_drift.py | PASS_SCOPE_GUARD |
| TC-OAS-901 | Explicit backend-only generator command contract. | scripts/generate_backend_openapi.py | PLANNED_DOWNSTREAM |
| TC-OAS-902 | Canonical committed artifact path and deterministic serialization contract. | docs/api/openapi/backend_openapi.json | PLANNED_DOWNSTREAM |
| TC-OAS-904 | Lightweight CI selector contract. | .github/workflows/ci.yml | PLANNED_DOWNSTREAM |
| TC-OAS-905 | Consumer-only docs publication contract. | docs/api/index.md | PLANNED_DOWNSTREAM |

## Red-Phase Selector Order
| Selector ID | Command | Purpose |
|---|---|---|
| S1 | `python -m pytest -q tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_committed_backend_artifact_exists_with_semantic_shape` | Missing-artifact and semantic-shape contract |
| S2 | `python -m pytest -q tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_drift_check_is_read_only_and_semantic` | Read-only semantic drift contract |
| S3 | `python -m pytest -q tests/docs/test_backend_openapi_drift.py::test_ac_oas_006_drift_lane_imports_backend_app_only` | Backend-only import-scope contract |
| S4 | `python -m pytest -q tests/docs/test_backend_openapi_drift.py` | Aggregate red-phase evidence for T-OAS-001 |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-OAS-001 | FAIL (RED_EXPECTED) | `AssertionError: Missing committed backend OpenAPI artifact at C:\Dev\PyAgent\docs\api\openapi\backend_openapi.json.` |
| TC-OAS-002 | FAIL (RED_EXPECTED) | `AssertionError: Missing committed backend OpenAPI artifact at C:\Dev\PyAgent\docs\api\openapi\backend_openapi.json.` |
| TC-OAS-003 | PASS | `backend.app.openapi()` loaded successfully and did not import `src.github_app` or `src.chat.api`. |

## Unresolved Failures
- Aggregate selector `python -m pytest -q tests/docs/test_backend_openapi_drift.py` returns `2 failed, 1 passed in 4.92s`.
- Failure mode is assertion-level only; no `ImportError` or `AttributeError` occurred during the red-phase run.
- `@6code` must add `scripts/generate_backend_openapi.py` and commit `docs/api/openapi/backend_openapi.json` from `backend.app.openapi()`.
- `@6code` must preserve the backend-only scope guard and keep the drift selector read-only.