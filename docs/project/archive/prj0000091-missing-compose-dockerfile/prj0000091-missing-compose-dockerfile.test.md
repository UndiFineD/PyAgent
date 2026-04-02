# missing-compose-dockerfile - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-28_

## Test Plan
Scope: RED-phase tests for compose Dockerfile path contract in `deploy/compose.yaml`.

Approach:
- Add deterministic pytest checks in `tests/deploy/test_compose_dockerfile_paths.py`.
- Validate expected contract target path for `services.pyagent.build.dockerfile`.
- Validate referenced Dockerfile resolves and exists on disk.
- Execute targeted pytest command only for this contract.

Command plan:
- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1`
- `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py --tb=short`

Executed commands:
- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/deploy/test_compose_dockerfile_paths.py --tb=short`
- `.venv/Scripts/ruff.exe check tests/deploy/test_compose_dockerfile_paths.py`
- `.venv/Scripts/ruff.exe check --select D tests/deploy/test_compose_dockerfile_paths.py`

Observed test run summary:
- `2 failed in 3.19s`
- Failure type: AssertionError (behavior-level contract failures)
- No import/collection blockers observed

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-AC002 | `services.pyagent.build.dockerfile` equals `deploy/Dockerfile.pyagent` | tests/deploy/test_compose_dockerfile_paths.py | RED_EXPECTED |
| TC-AC003 | Referenced Dockerfile path resolves and exists | tests/deploy/test_compose_dockerfile_paths.py | RED_EXPECTED |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case ID(s) |
|---|---|---|
| AC-002 | Compose pyagent service uses deploy-local Dockerfile path strategy | TC-AC002 |
| AC-003 | Target Dockerfile file exists in configured path | TC-AC003 |

## Weak-Test Detection Gate
- Gate W1 (placeholder resilience): PASS
	- Tests assert exact `dockerfile` value and resolved filesystem existence; they fail on stub/no-op implementations.
- Gate W2 (assertion strength): PASS
	- No `assert True`, no import-only assertions, no existence-only class checks.
- Gate W3 (red failure quality): PASS
	- Both failures are assertion-level contract violations, not `ImportError` or `AttributeError`.

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-AC002 | FAIL (RED_EXPECTED) | `AssertionError`: expected `deploy/Dockerfile.pyagent`, got `src/infrastructure/docker/Dockerfile` |
| TC-AC003 | FAIL (RED_EXPECTED) | `AssertionError`: resolved path `C:\Dev\PyAgent\src\infrastructure\docker\Dockerfile` does not exist |

## Unresolved Failures
- `tests/deploy/test_compose_dockerfile_paths.py::test_compose_reference_contract_uses_expected_pyagent_dockerfile_path`
	- Required fix for @6code: set `services.pyagent.build.dockerfile` in `deploy/compose.yaml` to `deploy/Dockerfile.pyagent`.
- `tests/deploy/test_compose_dockerfile_paths.py::test_compose_referenced_dockerfile_path_exists_in_repository`
	- Required fix for @6code: ensure the compose-referenced Dockerfile path exists (planned `deploy/Dockerfile.pyagent`).
