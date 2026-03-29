# coverage-minimum-enforcement - Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-28_

## Test Plan
Scope is limited to first-slice staged ratchet enforcement (stage 1):
1. Coverage threshold guard in `pyproject.toml` must enforce stage-1 minimum (`fail_under >= 40`).
2. Existing CI workflow must include a blocking coverage gate path (no soft-fail behavior).
3. Existing workflow-count constraints remain unchanged and continue to guard workflow sprawl.

Approach:
1. Add deterministic structure/config assertions in existing test modules only.
2. Validate red behavior against current repository state.
3. Capture explicit assertion-failure evidence (no ImportError/AttributeError-only failures).

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC1 | `pyproject.toml` coverage config defines `fail_under` | tests/test_coverage_config.py | PASS |
| TC2 | Stage-1 coverage minimum enforces `fail_under >= 40` | tests/test_coverage_config.py | RED_EXPECTED |
| TC3 | CI test job contains an explicit coverage gate path | tests/structure/test_ci_yaml.py | RED_EXPECTED |
| TC4 | Coverage gate path is fail-closed (no `continue-on-error`, `|| true`, `set +e`) | tests/structure/test_ci_yaml.py | RED_EXPECTED |
| TC5 | Workflow-count guard remains exactly two workflow files | tests/ci/test_workflow_count.py | PASS |

## AC-to-Test Matrix
| AC ID | Acceptance Criterion | Test Case IDs |
|---|---|---|
| AC1 | Stage-1 `fail_under` in pyproject is >= 40 | TC2 |
| AC2 | CI includes a blocking coverage gate path | TC3, TC4 |
| AC3 | CI/workflow-count constraints remain consistent | TC5 |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC1 | PASS | `tests/test_coverage_config.py::test_coverage_report_fail_under_is_present` passed |
| TC2 | FAIL (RED expected) | `assert 30 >= 40` from `test_coverage_report_fail_under_stage1_minimum` |
| TC3 | FAIL (RED expected) | `assert []` from `test_ci_has_coverage_gate_step` (no gate markers found) |
| TC4 | FAIL (RED expected) | `assert []` from `test_ci_coverage_gate_path_is_blocking` (coverage gate step missing) |
| TC5 | PASS | `tests/ci/test_workflow_count.py` assertions passed in targeted run |

Command evidence:
1. `.venv\Scripts\ruff.exe check --fix tests/test_coverage_config.py tests/structure/test_ci_yaml.py` -> PASS (1 auto-fix)
2. `.venv\Scripts\ruff.exe check tests/test_coverage_config.py tests/structure/test_ci_yaml.py` -> PASS
3. `.venv\Scripts\ruff.exe check --select D tests/test_coverage_config.py tests/structure/test_ci_yaml.py` -> PASS
4. `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_coverage_config.py tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py --tb=short` -> `3 failed, 17 passed in 2.64s`

## Weak-Test Detection Gate
1. Rejected existence-only assertions for coverage gate; tests assert concrete command semantics and fail-closed operators.
2. Rejected placeholder/pass-through checks; tests validate specific config values and blocking behavior.
3. Red-phase validation requires assertion failures tied to missing/incorrect behavior, not import/attribute collection errors.

## Unresolved Failures
1. `tests/test_coverage_config.py::test_coverage_report_fail_under_stage1_minimum`
	- Expected stage-1 minimum (`>= 40`) not satisfied because current value is 30.
2. `tests/structure/test_ci_yaml.py::test_ci_has_coverage_gate_step`
	- No coverage gate command currently present in `jobs.test`.
3. `tests/structure/test_ci_yaml.py::test_ci_coverage_gate_path_is_blocking`
	- Blocking semantics cannot be validated until coverage gate path exists.

## Handoff Notes (@6code)
1. Update `pyproject.toml` `[tool.coverage.report].fail_under` to stage-1 minimum (40 or higher).
2. Add a coverage gate command in `.github/workflows/ci.yml` `jobs.test.steps` using `--cov-fail-under` or `coverage report`.
3. Keep gate fail-closed: no `continue-on-error`, `|| true`, `||true`, or `set +e` in coverage gate path.
4. Preserve workflow inventory so `tests/ci/test_workflow_count.py` remains green.

## Post-Implementation Revalidation (@6code)
1. `pyproject.toml` updated to `fail_under = 40` for stage-1 enforcement.
2. `.github/workflows/ci.yml` now contains explicit coverage gate path in `jobs.test.steps` with `--cov-fail-under=40`.
3. Coverage gate path remains fail-closed (no `continue-on-error`, `|| true`, `||true`, `set +e`).
4. Targeted validation command:
	`c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_coverage_config.py tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py --tb=short`
5. Result: `20 passed in 4.01s`.
