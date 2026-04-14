- [x] T-SEC-002 - Implement scheduled security workflow to make T-SEC-001 green (TDD green phase)
# ci-security-quality-workflow-consolidation - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-02_

## Overview
Implement Option C from design using a TDD-first sequence: define failing workflow-contract tests, implement a new scheduled security workflow to satisfy those tests, add CI pre-commit parity assertions, and close with execution/quality/git handoff evidence. Scope is intentionally minimal and constrained to workflow/test artifacts.

## Scope Boundaries
- In scope:
	- `.github/workflows/security-scheduled.yml` (new)
	- `tests/ci/test_security_workflow.py` (new)
	- `tests/ci/test_ci_workflow.py` (additive parity assertions only)
	- Read-only regression validation of `.github/workflows/ci.yml`
- Out of scope:
	- `.pre-commit-config.yaml`
	- Any non-parity changes to `.github/workflows/ci.yml`
	- Source/runtime files under `src/**`, `backend/**`, `rust_core/**`

## Task List
- [ ] T-SEC-001 - Create failing workflow-structure tests for scheduled security workflow (TDD red phase)
	- [x] T-SEC-001 - Create failing workflow-structure tests for scheduled security workflow (TDD red phase)
	- Objective: Add deterministic assertions for workflow existence, triggers, permissions, and job contracts before implementation.
	- Classification: `parallel-safe`
	- Target files: `tests/ci/test_security_workflow.py`
	- Acceptance criteria: AC-SEC-001, AC-SEC-002, AC-SEC-003
	- Validation command: `python -m pytest -q tests/ci/test_security_workflow.py`

- [x] T-SEC-002 - Implement scheduled security workflow to make T-SEC-001 green (TDD green phase)
	- Objective: Create `.github/workflows/security-scheduled.yml` with daily schedule + `workflow_dispatch`, minimal permissions, dependency audit job, and Python-only CodeQL job referencing custom query pack.
	- Classification: `sequential-only` (depends on T-SEC-001 red tests)
	- Target files: `.github/workflows/security-scheduled.yml`
	- Acceptance criteria: AC-SEC-001, AC-SEC-002, AC-SEC-003
	- Validation command: `python -m pytest -q tests/ci/test_security_workflow.py`

- [ ] T-SEC-003 - Add pre-commit parity assertions in CI workflow tests
	- [x] T-SEC-003 - Add pre-commit parity assertions in CI workflow tests
	- Objective: Ensure lightweight CI retains `pre-commit run --all-files` command-level parity.
	- Classification: `parallel-safe`
	- Target files: `tests/ci/test_ci_workflow.py`
	- Acceptance criteria: AC-SEC-004
	- Validation command: `python -m pytest -q tests/ci/test_ci_workflow.py`

- [ ] T-SEC-004 - Regression guard validation for unchanged lightweight CI workflow behavior
	- [x] T-SEC-004 - Regression guard validation for unchanged lightweight CI workflow behavior
	- Objective: Validate `ci.yml` remains pre-commit-first and is not modified beyond parity-coverage intent.
	- Classification: `sequential-only` (convergence check after T-SEC-002 and T-SEC-003)
	- Target files: `.github/workflows/ci.yml` (read-only), `tests/ci/test_ci_workflow.py`
	- Acceptance criteria: AC-SEC-004
	- Validation command: `python -m pytest -q tests/ci/test_ci_workflow.py`

- [ ] T-SEC-005 - Exec/QL/Git closure handoff package
	- Objective: Produce downstream-ready closure evidence for @7exec/@8ql/@9git with policy-doc selector results and branch/scope compliance.
	- Classification: `sequential-only`
	- Target files: `docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.plan.md`, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/<YYYY-MM-DD>.4plan.log.md`
	- Acceptance criteria: AC-SEC-001, AC-SEC-002, AC-SEC-003, AC-SEC-004
	- Validation command: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

## File Ownership Map
| Task | Ownership type | Files |
|---|---|---|
| T-SEC-001 | Write/create | `tests/ci/test_security_workflow.py` |
| T-SEC-002 | Write/create | `.github/workflows/security-scheduled.yml` |
| T-SEC-003 | Modify (additive assertions) | `tests/ci/test_ci_workflow.py` |
| T-SEC-004 | Read-only validation | `.github/workflows/ci.yml` |
| T-SEC-005 | Planning + handoff docs | `docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.plan.md`, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/<YYYY-MM-DD>.4plan.log.md` |

## Acceptance Criteria Linkage
| AC ID | Description | Covered by tasks |
|---|---|---|
| AC-SEC-001 | Workflow exists with schedule + workflow_dispatch and no PR trigger | T-SEC-001, T-SEC-002 |
| AC-SEC-002 | Minimal permissions include `contents: read` and `security-events: write` | T-SEC-001, T-SEC-002 |
| AC-SEC-003 | `dependency-audit` and `codeql-scan` jobs with required config | T-SEC-001, T-SEC-002 |
| AC-SEC-004 | Lightweight CI remains `pre-commit run --all-files` | T-SEC-003, T-SEC-004 |

## Parallel Execution Plan
1. Wave A (parallel-safe)
	 - T-SEC-001 (owner: @5test)
	 - T-SEC-003 (owner: @5test)
	 - File ownership disjointness: `tests/ci/test_security_workflow.py` and `tests/ci/test_ci_workflow.py` are distinct.
2. Wave B (sequential-only)
	 - T-SEC-002 follows T-SEC-001 failing contract completion.
3. Convergence step (merge authority: @0master)
	 - Run `python -m pytest -q tests/ci/test_security_workflow.py` and `python -m pytest -q tests/ci/test_ci_workflow.py` on a single branch state.
	 - Confirm no parallel file ownership collision before handing off to @6code/@7exec.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Test contracts authored (red) | T-SEC-001, T-SEC-003 | PLANNED |
| M1 | Test contracts authored (red) | T-SEC-001, T-SEC-003 | DONE |
| M2 | Workflow implementation (green) | T-SEC-002 | PLANNED |
| M2 | Workflow implementation (green) | T-SEC-002 | DONE |
| M3 | Regression and closure evidence | T-SEC-004, T-SEC-005 | DONE |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/ci/test_security_workflow.py
python -m pytest -q tests/ci/test_ci_workflow.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```
