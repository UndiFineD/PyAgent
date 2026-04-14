# ci-security-quality-workflow-consolidation - Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-04-02_

## Branch Gate
- Expected branch: prj0000115-ci-security-quality-workflow-consolidation
- Observed branch: prj0000115-ci-security-quality-workflow-consolidation
- Result: PASS

## Test Plan
- Scope: Wave A red-phase test authoring for T-SEC-001 and T-SEC-003.
- Strategy: Add deterministic pytest contracts for security workflow structure and CI pre-commit command parity.
- Red/green intent:
	- T-SEC-001 selectors should fail until .github/workflows/security-scheduled.yml is implemented.
	- T-SEC-003 parity selector should pass immediately against existing ci.yml behavior.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-SEC-001 | security-scheduled.yml file exists | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-002 | triggers are schedule + workflow_dispatch and exclude pull_request | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-003 | top-level permissions include contents: read and security-events: write | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-004 | dependency-audit job exists | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-005 | codeql-scan job exists | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-006 | CodeQL init languages is python only | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-007 | CodeQL init references python custom query pack path | tests/ci/test_security_workflow.py | RED_EXPECTED |
| TC-SEC-008 | quick CI job pre-commit step runs pre-commit run --all-files | tests/ci/test_ci_workflow.py | READY |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case IDs |
|---|---|---|
| AC-SEC-001 | security-scheduled workflow exists with schedule + dispatch only | TC-SEC-001, TC-SEC-002 |
| AC-SEC-002 | workflow permissions are least-privilege for contents/security events | TC-SEC-003 |
| AC-SEC-003 | dependency-audit + python-only codeql-scan with custom queries | TC-SEC-004, TC-SEC-005, TC-SEC-006, TC-SEC-007 |
| AC-SEC-004 | lightweight CI retains pre-commit run --all-files command | TC-SEC-008 |

## Weak-Test Detection Gate
- Gate WTG-1 (placeholder/stub pass): PASS (tests assert specific workflow keys, values, and command strings).
- Gate WTG-2 (existence-only assertions): PASS (only TC-SEC-001 is existence; all others assert concrete behavior contracts).
- Gate WTG-3 (import-only/no-op): PASS (no import-only or assert-True tests).

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-SEC-001..TC-SEC-007 | RED_EXPECTED | `python -m pytest -q tests/ci/test_security_workflow.py` -> 7 failed in 4.56s |
| TC-SEC-008 | PASS | `python -m pytest -q tests/ci/test_ci_workflow.py` -> 7 passed in 3.68s |

## Command Evidence
- `.venv\Scripts\ruff.exe check --fix tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py` -> Found 1 error (1 fixed, 0 remaining)
- `.venv\Scripts\ruff.exe check tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py` -> All checks passed
- `python -m pytest -q tests/ci/test_security_workflow.py` -> `FFFFFFF [100%]` with `7 failed in 4.56s`
- `python -m pytest -q tests/ci/test_ci_workflow.py` -> `....... [100%]` with `7 passed in 3.68s`

## Unresolved Failures
- Expected red-phase failures remain for T-SEC-001 until `.github/workflows/security-scheduled.yml` is implemented by @6code.
