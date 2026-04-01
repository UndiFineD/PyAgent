# idea000004-quality-workflow-branch-trigger - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-01_

## Test Plan
Execute T-QWB-001 in red phase by extending CI workflow contract tests for:
1. Explicit project-branch PR trigger pattern (reject ambiguous wildcard branch matching).
2. Stable required-check identity contract via deterministic workflow/job naming.

Scope limited to planned test/doc files plus required @5test memory/log records.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-QWB-001 | PR trigger uses explicit project branch glob and rejects ambiguous `prj*` | tests/ci/test_ci_workflow.py | RED |
| TC-QWB-002 | Required-check workflow identity matches stable governance contract | tests/ci/test_ci_workflow.py | RED |
| TC-QWB-003 | Branch/scope canonical enforcement regression remains green | tests/test_enforce_branch.py | GREEN |
| TC-QWB-004 | Docs governance policy suite remains green | tests/docs/test_agent_workflow_policy_docs.py | GREEN |

## AC-to-Test Matrix
| AC ID | Contract | Test Case IDs |
|---|---|---|
| AC-QWB-001 | Project-branch PR trigger contract | TC-QWB-001 |
| AC-QWB-004 | Required-check identity stability contract | TC-QWB-002 |

## Weak-Test Detection Gate
Gate status: PASS

Checks performed:
1. No placeholder tests (`assert True`, TODO-only, existence-only assertions) added.
2. Red-phase failure reason is assertion-level behavior mismatch, not ImportError/AttributeError.
3. Contracts require concrete YAML values from `.github/workflows/ci.yml`.

Evidence:
1. `tests/ci/test_ci_workflow.py::test_ci_workflow_pull_request_trigger_includes_project_branches` failed on branch pattern mismatch (`['main', 'prj*']` vs required explicit `prj[0-9]...-*`).
2. `tests/ci/test_ci_workflow.py::test_ci_workflow_required_check_identity_contract` failed on workflow name mismatch (`CI (minimal)` vs required `CI / Branch Governance`).

## Validation Results
| ID | Result | Output |
|---|---|---|
| LINT-QWB-001 | PASS | `.venv\Scripts\ruff.exe check tests/ci/test_ci_workflow.py` -> All checks passed |
| RUN-QWB-001 | RED (expected) | `python -m pytest -q tests/ci/test_ci_workflow.py tests/test_enforce_branch.py` -> 2 failed, 25 passed |
| RUN-QWB-002 | PASS | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> 17 passed |

## Unresolved Failures
1. Trigger pattern contract failure in `tests/ci/test_ci_workflow.py` requiring explicit project pattern.
2. Required-check identity contract failure in `tests/ci/test_ci_workflow.py` requiring stable workflow name.

## Handoff
Target agent: @6code
Handoff state: READY_FOR_IMPLEMENTATION
Requested implementation scope (per T-QWB-002 follow-up):
1. Update `.github/workflows/ci.yml` pull_request branch pattern to explicit project format expected by TC-QWB-001.
2. Update `.github/workflows/ci.yml` workflow identity to satisfy TC-QWB-002 while preserving governance job identity.