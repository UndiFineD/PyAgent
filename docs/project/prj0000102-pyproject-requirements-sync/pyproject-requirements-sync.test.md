# pyproject-requirements-sync - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-30_

## Test Plan
This artifact defines the failing-first (red) contract for dependency-sync governance
and the expected pass criteria (green) for @6code validation.

### Strategy
- Unit: Validate canonical dependency-source parsing, deterministic rendering behavior,
	duplicate detection, malformed specifier rejection, and critical package policy checks.
- Integration: Validate generated-vs-committed parity and CI drift gate behavior using
	repository structure and policy checks.
- Regression: Preserve deterministic output and policy constraints across future dependency
	updates so drift or relaxed rules cannot silently re-enter.

### Scope
- In scope: project acceptance criteria AC-001 through AC-006 from
	`pyproject-requirements-sync.plan.md`.
- Out of scope: production implementation edits during @5test artifact completion.

### Weak-Test Detection Gate (Blocking)
- Reject tests that only assert existence/import/type checks or no-exception behavior.
- Reject placeholder tests (`assert True`, TODO-only tests, pass-only checks).
- Red-phase failures must be meaningful assertion/policy failures, not ImportError or
	AttributeError.
- Green-phase sign-off is blocked if any test still passes against placeholder/stub logic.

## AC-to-Test Matrix
| AC ID | Requirement | Test Case IDs | Primary Selector/Command |
|---|---|---|---|
| AC-001 | Canonical runtime authority is `pyproject.toml` `[project.dependencies]` | TC-001 | `python -m pytest -q tests -k "dependency and canonical and pyproject"` |
| AC-002 | `requirements.txt` is deterministic derived output | TC-002 | `python -m pytest -q tests -k "requirements and deterministic"` |
| AC-003 | Drift blocks CI | TC-003 | `python -m pytest -q tests/structure -k "dependency and drift and ci"` |
| AC-004 | Duplicate and malformed dependency protections | TC-004 | `python -m pytest -q tests -k "dependency and policy"` |
| AC-005 | Security-sensitive package spec policy enforcement | TC-004 | `python -m pytest -q tests -k "dependency and policy"` |
| AC-006 | Changes remain bounded to dependency-sync governance scope | TC-005 | `git diff --name-only` |

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-001 | Canonical source contract fails unless dependency authority is read from `[project.dependencies]` only. | tests (selector: `dependency and canonical and pyproject`) | PLANNED_RED |
| TC-002 | Deterministic output contract fails when repeated generation from identical input is not byte-equivalent. | tests (selector: `requirements and deterministic`) | PLANNED_RED |
| TC-003 | Drift/CI gate contract fails when generated requirements differ from committed artifact. | tests/structure (selector: `dependency and drift and ci`) | PLANNED_RED |
| TC-004 | Policy contract fails for duplicate lines, malformed specifiers, or critical package policy violations. | tests (selector: `dependency and policy`) | PLANNED_RED |
| TC-005 | Scope lock fails if changed files leave dependency-sync governance/project artifact boundary. | repository diff gate | PLANNED_RED |

## Deterministic Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests -k "dependency and canonical and pyproject"
python -m pytest -q tests -k "requirements and deterministic"
python -m pytest -q tests/structure -k "dependency and drift and ci"
python -m pytest -q tests -k "dependency and policy"
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
git diff --name-only
```

Expected command determinism contract:
- Re-running the same selector with unchanged inputs yields identical pass/fail status.
- Red phase before @6code: TC-001..TC-004 fail for assertion/policy reasons tied to missing
	behavior, not import/symbol absence.
- Green phase after @6code: TC-001..TC-004 pass; TC-005 pass confirms scope boundaries.

## Validation Results
| ID | Result | Output |
|---|---|---|
| DOCS-POLICY | PASS | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` (executed during this @5test artifact update) |
| TC-001 | NOT_RUN_IN_DOCS_ONLY_PHASE | Planned red/green validation owned by @5test/@6code execution phases per finalized plan. |
| TC-002 | NOT_RUN_IN_DOCS_ONLY_PHASE | Planned red/green validation owned by @5test/@6code execution phases per finalized plan. |
| TC-003 | NOT_RUN_IN_DOCS_ONLY_PHASE | Planned red/green validation owned by @5test/@6code execution phases per finalized plan. |
| TC-004 | NOT_RUN_IN_DOCS_ONLY_PHASE | Planned red/green validation owned by @5test/@6code execution phases per finalized plan. |
| TC-005 | NOT_RUN_IN_DOCS_ONLY_PHASE | Scope validation command is deterministic and required at @7exec/@9git gates. |

## Expected Red/Green Handoff Criteria For @6code
- READY_FOR_@6code (Red complete) when:
	- AC-to-test matrix is complete with no unmapped AC IDs.
	- Weak-test detection gate is documented and unresolved weak tests are zero.
	- Red expectations are explicit for TC-001..TC-004 and tied to meaningful failures.
	- Docs policy check passes for this artifact update.
- GREEN_ACCEPTANCE (post-implementation) requires:
	- TC-001..TC-004 pass on @6code changes.
	- No regressions on dependency policy/structure selectors.
	- Scope boundary remains compliant (AC-006).

## Unresolved Failures
None in this docs-only artifact completion step.
