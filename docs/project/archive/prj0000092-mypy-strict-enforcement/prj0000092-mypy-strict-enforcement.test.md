# mypy-strict-enforcement - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-28_

## Test Plan
Create failing-first (RED) contract tests for strict-lane mypy enforcement before implementation.
Scope for this phase is limited to:
1) strict-lane config contract checks,
2) CI strict-lane blocking-step contract checks,
3) deterministic smoke test behavior using a known-bad fixture.

Execution approach:
- write tests that fail due missing strict-lane artifacts/wiring,
- run only targeted test files,
- capture failure output proving contract gaps.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-001 | Strict-lane config exists and enforces required strict options | tests/structure/test_mypy_strict_lane_config.py | RED |
| TC-002 | Strict-lane config locks exact phase-1 allowlist | tests/structure/test_mypy_strict_lane_config.py | RED |
| TC-003 | CI includes blocking strict-lane mypy command without soft-fail semantics | tests/structure/test_ci_yaml.py | RED |
| TC-004 | Smoke check runs mypy strict lane against known-bad fixture and expects non-zero type-check failure | tests/test_zzc_mypy_strict_lane_smoke.py | RED |

## AC-to-Test Matrix
| AC ID | Contract | Tests |
|---|---|---|
| AC-001 | strict config file + required strict options | TC-001 |
| AC-002 | strict config allowlist equals locked phase-1 files | TC-002 |
| AC-003 | CI has blocking strict-lane mypy step | TC-003 |
| AC-004 | structure tests detect contract drift | TC-001, TC-002, TC-003 |
| AC-005 | deterministic known-bad smoke returns non-zero | TC-004 |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-001 | FAIL (expected RED) | `AssertionError: Expected strict-lane config at mypy-strict-lane.ini...` |
| TC-002 | FAIL (expected RED) | `AssertionError: Expected strict-lane config at mypy-strict-lane.ini...` |
| TC-003 | FAIL (expected RED) | `AssertionError: CI must include a strict-lane mypy run command: python -m mypy --config-file mypy-strict-lane.ini` |
| TC-004 | FAIL (expected RED) | `AssertionError: Expected strict-lane config at mypy-strict-lane.ini before smoke validation can run.` |

## Unresolved Failures
- Missing strict-lane config file: `mypy-strict-lane.ini`
- Missing blocking CI strict-lane command in `.github/workflows/ci.yml`
- Smoke lane cannot execute until strict config exists

## RED Evidence
- Command:
	- `python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py --tb=short`
- Result:
	- `5 failed, 3 passed in 3.85s`
- Failure quality gate:
	- PASS: failures are assertion-style contract failures
	- PASS: no `ImportError`/`AttributeError` collection blockers

## Weak-Test Detection Gate
- Gate status: PASS (design-time)
- Checks applied:
	- no placeholder tests (`assert True`, TODO-only, or no assertions),
	- no import-only existence assertions,
	- assertions target concrete behavior: exact config keys, exact allowlist, explicit CI blocking command contract, and non-zero mypy execution result.
