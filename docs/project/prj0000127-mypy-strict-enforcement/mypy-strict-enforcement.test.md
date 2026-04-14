# mypy-strict-enforcement - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-04_
## Test Plan
Execute RED phase for T-MYPY-001..003 only.
Scope is limited to docs-policy test coverage and project test artifact convergence.
No GREEN workflow/config implementation edits are allowed in this phase.

## Branch and Scope Preconditions
- Expected branch: prj0000127-mypy-strict-enforcement
- Observed branch: prj0000127-mypy-strict-enforcement
- Project match: PASS
- Scope-bounded files touched in this RED slice:
	- tests/docs/test_agent_workflow_policy_docs.py
	- docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md
	- .github/agents/data/current.5test.memory.md
	- .github/agents/data/2026-04-04.5test.log.md

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-MYPY-001 | Assert strict-lane CI contract must include explicit `--config-file pyproject.toml` and full phase-1 allowlist targets. | tests/docs/test_agent_workflow_policy_docs.py | RED_CONFIRMED |
| TC-MYPY-002 | Assert warn->required promotion contract includes explicit `N=5` threshold and promotion evidence markers in execution artifact. | tests/docs/test_agent_workflow_policy_docs.py | RED_CONFIRMED |
| TC-MYPY-003 | Converge RED handoff artifact with failing selectors, AC mapping, and ownership boundaries. | docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md | DONE |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case ID |
|---|---|---|
| AC-MYPY-001 | Strict-lane command contract must be explicit and deterministic in CI (config authority + allowlist coverage). | TC-MYPY-001 |
| AC-MYPY-002 | Warn->required promotion contract must include explicit threshold `N=5`. | TC-MYPY-002 |
| AC-MYPY-003 | RED convergence artifact must define failing selectors and ownership boundaries before @6code handoff. | TC-MYPY-003 |

## Weak-Test Detection Gate
Reject and block handoff to @6code if any of the following are true:
- Tests pass on placeholders/stubs or assert only existence/import.
- Assertions are non-behavioral (for example, unconditional `assert True`).
- RED evidence is only `ImportError`/`AttributeError` rather than contract assertion failure.
- AC-to-test matrix is missing or incomplete.

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-MYPY-001 | FAIL (expected RED) | `AssertionError: assert 'python -m mypy --config-file pyproject.toml' in ci.yml` |
| TC-MYPY-002 | FAIL (expected RED) | `AssertionError: assert 'n=5' in mypy-strict-enforcement.exec.md` |
| TC-MYPY-003 | PASS | Convergence artifact finalized with selectors and ownership boundaries. |

## RED-Phase Selector Order
| Selector ID | Command | Expected | Observed |
|---|---|---|---|
| S1 | `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or mypy or promotion"` | At least one failing assertion proving missing strict-lane/promotion implementation contracts | `2 failed, 17 deselected` |

## Ownership Boundaries (RED -> GREEN)
- @5test ownership (this slice):
	- tests/docs/test_agent_workflow_policy_docs.py (RED assertions only)
	- docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md
- @6code ownership (next GREEN slice):
	- .github/workflows/ci.yml strict-lane command implementation
	- docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.exec.md promotion evidence contract (`N=5`)
- Overlap policy: @5test does not implement workflow/config GREEN fixes.

## Unresolved Failures
- `test_prj0000127_mypy_strict_lane_ci_contract_requires_explicit_config_and_phase1_allowlist`
	- Missing strict-lane mypy command contract in `.github/workflows/ci.yml`.
- `test_prj0000127_mypy_promotion_contract_requires_n5_warn_to_required_artifacts`
	- Missing explicit `N=5` promotion evidence markers in `mypy-strict-enforcement.exec.md`.

