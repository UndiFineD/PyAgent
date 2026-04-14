# coverage-minimum-enforcement - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-05_

## Test Plan
- Scope: RED wave contracts for `T-COV-001..003` only.
- Branch gate: expected `prj0000128-coverage-minimum-enforcement`; observed `prj0000128-coverage-minimum-enforcement`; result `PASS`.
- RED target: workflow-shape and command-contract tests fail until `jobs.coverage` is implemented in `.github/workflows/ci.yml`.
- Non-goal in RED: no GREEN edits to `.github/workflows/ci.yml`.

## AC-to-Test Matrix
| AC ID | Contract | Test Case IDs |
|---|---|---|
| T-COV-001 | Exactly one `coverage` job, preserve `quick`, and enforce `coverage.needs: quick` | TC-COV-001, TC-COV-002 |
| T-COV-002 | Canonical pytest-cov command flags present; reject `--cov-fail-under`, `continue-on-error`, `\|\| true`, `set +e` in coverage path | TC-COV-003, TC-COV-004 |
| T-COV-003 | RED convergence handoff records failing selectors and ownership boundaries; config authority anchored in `tests/test_coverage_config.py` | TC-COV-005 |

## Weak-Test Detection Gate
- Gate rule: reject tests that pass on placeholders/stubs or only assert symbol existence/import.
- Gate result: `PASS`.
- Evidence:
	- Coverage tests parse workflow structure and command content (behavioral contract), not import/existence only.
	- RED failure reason must be assertion-level behavior mismatch (missing `jobs.coverage` / command contract), not `ImportError` or `AttributeError`.

## Ownership Boundaries
- `@5test` RED files:
	- `tests/structure/test_ci_yaml.py`
	- `docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.test.md`
	- `.github/agents/data/current.5test.memory.md`
	- `.github/agents/data/2026-04-05.5test.log.md`
- `@6code` GREEN files (future wave):
	- `.github/workflows/ci.yml`

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-COV-001 | Require exactly one `jobs.coverage` entry | `tests/structure/test_ci_yaml.py` | RED-ADDED |
| TC-COV-002 | Require `jobs.quick` preserved and `jobs.coverage.needs` includes `quick`; reject job-level soft-fail | `tests/structure/test_ci_yaml.py` | RED-ADDED |
| TC-COV-003 | Require canonical pytest-cov markers on coverage command path | `tests/structure/test_ci_yaml.py` | RED-ADDED |
| TC-COV-004 | Reject `--cov-fail-under`, `continue-on-error`, `\|\| true`, and `set +e` in coverage path | `tests/structure/test_ci_yaml.py` | RED-ADDED |
| TC-COV-005 | Keep config-authority checks anchored to `pyproject.toml` with fail_under minimum in test authority file | `tests/test_coverage_config.py` | BASELINE |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-COV-001 | RED (expected fail) | `python -m pytest -q tests/structure/test_ci_yaml.py -k "coverage or quick"` -> `test_ci_has_coverage_gate_step` failed: expected exactly one `jobs.coverage`, found zero |
| TC-COV-002 | RED (expected fail) | same selector -> `test_ci_coverage_gate_path_is_blocking` failed: missing `jobs.coverage` and therefore missing `needs: quick` path |
| TC-COV-003 | RED (expected fail) | same selector -> `test_ci_coverage_job_uses_canonical_pytest_cov_flags` failed because coverage command path is absent |
| TC-COV-004 | RED-N/A in selector window | forbidden-marker assertions are added and will activate on GREEN workflow edit when `jobs.coverage` exists |
| TC-COV-005 | PASS | `python -m pytest -q tests/test_coverage_config.py` -> `7 passed` |

## Unresolved Failures
- RED convergence outcome: expected failing-first contracts are confirmed and attributable to missing behavior in `.github/workflows/ci.yml`.
- Failing selectors (for @6code GREEN target):
	- `tests/structure/test_ci_yaml.py::test_ci_has_coverage_gate_step`
	- `tests/structure/test_ci_yaml.py::test_ci_coverage_gate_path_is_blocking`
	- `tests/structure/test_ci_yaml.py::test_ci_coverage_job_uses_canonical_pytest_cov_flags`
- Non-qualifying failure types absent: `ImportError`, `AttributeError`, `SyntaxError`.
- Handoff target: `@6code`.

