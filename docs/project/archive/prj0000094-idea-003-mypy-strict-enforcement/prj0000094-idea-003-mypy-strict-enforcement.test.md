# prj0000094-idea-003-mypy-strict-enforcement - Test Artifacts

_Status: IN_PROGRESS_
_Tester: @5test | Updated: 2026-03-28_

## Test Plan
Scope: execute T1-T2 only for Wave 1 red-phase gate.

Branch and policy gates:
1. Expected branch from project artifact: `prj0000094-idea-003-mypy-strict-enforcement`.
2. Observed branch: `prj0000094-idea-003-mypy-strict-enforcement`.
3. Result: PASS.
4. Policy references loaded before test edits: `docs/project/code_of_conduct.md`, `docs/project/naming_standards.md`.

Approach:
1. Run baseline strict-lane contract test bundle from plan unchanged (T1).
2. Tighten Wave 1 allowlist expectation in structure test only (T2), without changing implementation config.
3. Re-run same bundle to confirm assertion-level red failure due to missing Wave 1 implementation delta.
4. Validate modified test file with ruff lint and docstring checks.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-T1-BASELINE | Baseline strict-lane contract bundle passes before Wave 1 test deltas | tests/structure/test_mypy_strict_lane_config.py, tests/structure/test_ci_yaml.py, tests/zzz/test_zzc_mypy_strict_lane_smoke.py | PASS |
| TC-T2-WAVE1-ALLOWLIST | Wave 1 allowlist lock enforces 10-file expectation (should fail pre-implementation) | tests/structure/test_mypy_strict_lane_config.py | RED |
| TC-T2-CI-BLOCKING | CI strict-lane command remains present and blocking semantics unchanged | tests/structure/test_ci_yaml.py | PASS |
| TC-T2-SMOKE-DETERMINISM | Strict-lane behavioral smoke remains deterministic for known-bad fixture | tests/zzz/test_zzc_mypy_strict_lane_smoke.py | PASS |

## AC-to-Test Matrix
| AC ID | Requirement Summary | Test Case IDs |
|---|---|---|
| AC-01 | Wave-based expansion encoded through explicit gate expectations | TC-T2-WAVE1-ALLOWLIST |
| AC-02 | Strict-lane deterministic config contract remains explicit | TC-T1-BASELINE, TC-T2-WAVE1-ALLOWLIST |
| AC-03 | CI strict-lane command remains present and blocking | TC-T1-BASELINE, TC-T2-CI-BLOCKING |
| AC-04 | Strict-lane behavioral failure remains deterministic | TC-T1-BASELINE, TC-T2-SMOKE-DETERMINISM |
| AC-07 | Interface-to-task traceability via contract tests | TC-T2-WAVE1-ALLOWLIST, TC-T2-CI-BLOCKING, TC-T2-SMOKE-DETERMINISM |

## Weak-Test Detection Gate
Gate checks:
1. Reject tests that assert only import/existence/`assert True`: PASS.
2. Confirm red failure is assertion-level behavior mismatch, not import/attribute error: PASS.
3. Confirm target failing test can pass only after implementation delta in `mypy-strict-lane.ini`: PASS.
4. Confirm no placeholder test bodies (`TODO`, no-op): PASS.

## Validation Results
| ID | Result | Output |
|---|---|---|
| VR-T1-01 | PASS | `& c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py` -> `8 passed in 3.89s` |
| VR-T2-01 | RED (expected) | `& c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py --tb=short` -> `1 failed, 7 passed in 5.68s`; failing test: `tests/structure/test_mypy_strict_lane_config.py::test_mypy_strict_lane_allowlist_locked`; assertion message: `Strict-lane allowlist drift detected... locked Wave 1 10-file list.` |
| VR-T2-02 | PASS | `& c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --fix tests/structure/test_mypy_strict_lane_config.py` -> `All checks passed!` |
| VR-T2-03 | PASS | `& c:/Dev/PyAgent/.venv/Scripts/ruff.exe check tests/structure/test_mypy_strict_lane_config.py` -> `All checks passed!` |
| VR-T2-04 | PASS | `& c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --select D tests/structure/test_mypy_strict_lane_config.py` -> `All checks passed!` |

## Unresolved Failures
1. `tests/structure/test_mypy_strict_lane_config.py::test_mypy_strict_lane_allowlist_locked`
	- Failure type: assertion mismatch (expected red).
	- Why unresolved: Wave 1 implementation (T3) has not yet expanded `[mypy] files` in `mypy-strict-lane.ini`.
	- Expected implementing agent action: add the 4 Wave 1 files to strict-lane allowlist in config.
