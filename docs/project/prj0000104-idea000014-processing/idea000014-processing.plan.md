# idea000014-processing - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-30_

## Overview
Implement Option A from design: `pyproject.toml` is the single manually edited dependency source and `requirements.txt` is a deterministic generated artifact.

This plan is staged for downstream execution in strict TDD order:
1) @5test writes failing tests/checks (red)
2) @6code implements minimal code to pass tests (green)
3) @7exec validates runtime and workflow behavior
4) @8ql runs security/quality gates
5) @9git performs scoped handoff and PR preparation

Scope for @4plan remains planning artifacts + memory/log updates only.

## Scope Boundary (Expected Edit/Test Files)

Expected production-edit targets (planned for @6code):
- `pyproject.toml`
- `requirements.txt`
- `requirements-ci.txt` (only if include chain adjustments are required)
- `scripts/deps/generate_requirements.py` (new)
- `scripts/deps/check_dependency_parity.py` (new)
- `.pre-commit-config.yaml` (or equivalent local parity command wiring)
- `.github/workflows/ci.yml` (or dedicated parity workflow)
- `install.ps1` (compatibility-preserving adjustments only)
- `README.md` and/or `docs/setup.md` (authoring and local parity workflow)

Expected test-edit targets (planned for @5test):
- `tests/deps/test_generate_requirements_deterministic.py` (new)
- `tests/deps/test_dependency_parity_gate.py` (new)
- `tests/deps/test_manual_requirements_edit_detected.py` (new)
- `tests/deps/test_pyproject_parse_failure.py` (new)
- `tests/deps/test_install_compatibility_contract.py` (new)
- `tests/deps/fixtures/pyproject_valid.toml` (new)
- `tests/deps/fixtures/pyproject_malformed.toml` (new)
- `tests/deps/fixtures/requirements_expected.txt` (new)
- `tests/deps/fixtures/requirements_drifted.txt` (new)

## Task List

### Phase 0 - Planning and Gate Setup

- [ ] T001 - Canonical-source policy codification
	- Objective: Define and document that `pyproject.toml` is the only manual runtime dependency source and `requirements.txt` is derived.
	- Owner: @6code
	- Target files: `README.md`, `docs/setup.md`, `pyproject.toml`
	- Acceptance criteria: AC-001, AC-007
	- Validation command:
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

### Phase 1 - Red (Tests First by @5test)

- [ ] T002 - Deterministic generation red tests
	- Objective: Add failing tests that define byte-stable generation behavior.
	- Owner: @5test
	- Target files: `tests/deps/test_generate_requirements_deterministic.py`, `tests/deps/fixtures/pyproject_valid.toml`, `tests/deps/fixtures/requirements_expected.txt`
	- Acceptance criteria: AC-002, AC-006
	- Validation command:
		- `python -m pytest -q tests/deps/test_generate_requirements_deterministic.py`

- [ ] T003 - Parity mismatch red tests
	- Objective: Add failing tests for CI/local non-zero exit on parity mismatch plus remediation message.
	- Owner: @5test
	- Target files: `tests/deps/test_dependency_parity_gate.py`, `tests/deps/fixtures/requirements_drifted.txt`
	- Acceptance criteria: AC-003, AC-004, AC-006
	- Validation command:
		- `python -m pytest -q tests/deps/test_dependency_parity_gate.py`

- [ ] T004 - Malformed source and manual-edit red tests
	- Objective: Add failing tests for malformed `pyproject.toml` handling and manual edits to generated file.
	- Owner: @5test
	- Target files: `tests/deps/test_pyproject_parse_failure.py`, `tests/deps/test_manual_requirements_edit_detected.py`, `tests/deps/fixtures/pyproject_malformed.toml`
	- Acceptance criteria: AC-006
	- Validation command:
		- `python -m pytest -q tests/deps/test_pyproject_parse_failure.py tests/deps/test_manual_requirements_edit_detected.py`

- [ ] T005 - Install compatibility red tests
	- Objective: Add failing contract tests proving requirements-based installs remain valid.
	- Owner: @5test
	- Target files: `tests/deps/test_install_compatibility_contract.py`, `requirements-ci.txt`
	- Acceptance criteria: AC-005
	- Validation command:
		- `python -m pytest -q tests/deps/test_install_compatibility_contract.py`

### Phase 2 - Green (Implementation by @6code)

- [ ] T006 - Implement deterministic generator wrapper
	- Objective: Implement generator command wrapper that normalizes output ordering/newlines and supports deterministic repeated runs.
	- Owner: @6code
	- Target files: `scripts/deps/generate_requirements.py`, `requirements.txt`
	- Acceptance criteria: AC-002
	- Validation command:
		- `python scripts/deps/generate_requirements.py --output requirements.txt`

- [ ] T007 - Implement parity checker command
	- Objective: Implement check-only parity command with non-zero exit and actionable remediation output on mismatch.
	- Owner: @6code
	- Target files: `scripts/deps/check_dependency_parity.py`
	- Acceptance criteria: AC-003, AC-004
	- Validation command:
		- `python scripts/deps/check_dependency_parity.py --check`

- [ ] T008 - Wire local fast feedback
	- Objective: Wire parity check into local contributor workflow for rapid drift detection.
	- Owner: @6code
	- Target files: `.pre-commit-config.yaml` (or equivalent), `README.md`
	- Acceptance criteria: AC-004
	- Validation command:
		- `pre-commit run --all-files`

- [ ] T009 - Wire CI authoritative parity gate
	- Objective: Add CI parity check job that fails on mismatch and emits remediation command.
	- Owner: @6code
	- Target files: `.github/workflows/ci.yml` (or dedicated workflow)
	- Acceptance criteria: AC-003
	- Validation command:
		- `python scripts/deps/check_dependency_parity.py --check`

- [ ] T010 - Preserve install compatibility contract
	- Objective: Ensure existing requirements-based install paths continue to function.
	- Owner: @6code
	- Target files: `install.ps1`, `requirements-ci.txt`, `README.md`
	- Acceptance criteria: AC-005
	- Validation command:
		- `pip install -r requirements.txt`

### Phase 3 - Runtime Validation by @7exec

- [ ] T011 - End-to-end parity workflow execution
	- Objective: Execute generation then parity checks under clean conditions and verify byte-identical no-op run.
	- Owner: @7exec
	- Target files: No new files; validate implemented workflow.
	- Acceptance criteria: AC-002, AC-003, AC-006
	- Validation command:
		- `python scripts/deps/generate_requirements.py --output requirements.txt`
		- `python scripts/deps/check_dependency_parity.py --check`
		- `git diff --exit-code -- requirements.txt`

### Phase 4 - Security/Quality Closure by @8ql

- [ ] T012 - Quality/security gate confirmation
	- Objective: Confirm lint/test/security signals remain passing after dependency workflow changes.
	- Owner: @8ql
	- Target files: No new files; run gates and report.
	- Acceptance criteria: AC-006
	- Validation command:
		- `python -m pytest -q tests/deps`
		- `python -m pip_audit`

### Phase 5 - Handoff by @9git

- [ ] T013 - Scoped staging and PR handoff
	- Objective: Stage only branch-scope files, attach gate evidence, and prepare PR.
	- Owner: @9git
	- Target files: Branch-scope files only.
	- Acceptance criteria: AC-001..AC-007 closure evidence attached to PR.
	- Validation command:
		- `git branch --show-current`
		- `git status --short`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Red tests complete | T002-T005 | NOT_STARTED |
| M2 | Green implementation complete | T006-T010 | NOT_STARTED |
| M3 | Runtime validation complete | T011 | NOT_STARTED |
| M4 | Security/quality closure complete | T012 | NOT_STARTED |
| M5 | Git handoff complete | T013 | NOT_STARTED |

## AC To Task Traceability
| AC ID | Mapped Tasks | Primary validation commands |
|---|---|---|
| AC-001 | T001 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| AC-002 | T002, T006, T011 | `python -m pytest -q tests/deps/test_generate_requirements_deterministic.py`; `python scripts/deps/generate_requirements.py --output requirements.txt`; `git diff --exit-code -- requirements.txt` |
| AC-003 | T003, T007, T009, T011 | `python -m pytest -q tests/deps/test_dependency_parity_gate.py`; `python scripts/deps/check_dependency_parity.py --check` |
| AC-004 | T003, T007, T008 | `python -m pytest -q tests/deps/test_dependency_parity_gate.py`; `pre-commit run --all-files` |
| AC-005 | T005, T010 | `python -m pytest -q tests/deps/test_install_compatibility_contract.py`; `pip install -r requirements.txt` |
| AC-006 | T002, T003, T004, T011, T012 | `python -m pytest -q tests/deps`; `python scripts/deps/check_dependency_parity.py --check` |
| AC-007 | T001, T013 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`; PR checklist evidence |

## Downstream TDD Sequence And Gates
1. @5test (Red Gate)
	 - Entry criteria: T001 planning/policy context complete.
	 - Exit criteria: T002-T005 tests fail for expected reasons only.
	 - Gate command: `python -m pytest -q tests/deps`
2. @6code (Green Gate)
	 - Entry criteria: red tests merged in branch and reproducible.
	 - Exit criteria: T006-T010 implemented with zero placeholder files.
	 - Gate command: `python -m pytest -q tests/deps`
3. @7exec (Runtime Gate)
	 - Entry criteria: green tests pass.
	 - Exit criteria: end-to-end command sequence succeeds and no-op regeneration is byte-stable.
	 - Gate command: `python scripts/deps/generate_requirements.py --output requirements.txt` + `python scripts/deps/check_dependency_parity.py --check`
4. @8ql (Security/Quality Gate)
	 - Entry criteria: runtime gate passed.
	 - Exit criteria: quality/security checks pass with no unresolved blocker.
	 - Gate command: `python -m pytest -q tests/deps` and `python -m pip_audit`
5. @9git (Release Gate)
	 - Entry criteria: all prior gates green with evidence.
	 - Exit criteria: scoped staging, commit, and PR ready.
	 - Gate command: `git branch --show-current` and `git status --short`

## Rollback And Contingency
| Trigger | Contingency action | Rollback command path | Pass/fail gate |
|---|---|---|---|
| Nondeterministic generated output | Freeze merge; capture environment/tool versions; rerun deterministic test locally and CI | Revert generator/parity commits in reverse order | Pass only when two consecutive generation runs are byte-identical |
| CI parity fails but local passes | Align toolchain versions with documented baseline and rerun parity | Revert CI/workflow changes if mismatch persists | Pass only when local and CI parity both return exit 0 |
| Install compatibility regression | Restore previous install command path while keeping source-of-truth docs | Revert install script changes first; keep tests | Pass only when install contract tests pass |
| Malformed pyproject handling regresses | Tighten parse/validation branch and error contract | Revert parser changes breaking structured error behavior | Pass only when parse-failure tests pass |

## Risks And Blockers
- Risk: Toolchain drift between local and CI can cause false parity diffs.
	- Mitigation: pin generator/checker tool versions and record in docs.
- Risk: Manual edits to derived artifact can reappear.
	- Mitigation: keep local and CI parity checks both active.

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Policy docs gate required for project artifact updates
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# Planned downstream command matrix
python -m pytest -q tests/deps
python scripts/deps/generate_requirements.py --output requirements.txt
python scripts/deps/check_dependency_parity.py --check
pre-commit run --all-files
pip install -r requirements.txt
python -m pip_audit
git diff --exit-code -- requirements.txt
git branch --show-current
git status --short
```

## Handoff Readiness To @5test
- Current readiness: READY
- Preconditions satisfied:
	- Branch gate validated (`prj0000104-idea000014-processing`).
	- AC-to-task traceability complete for AC-001..AC-007.
	- File-level red-test scope explicitly defined.
	- Red gate command and expected failing stage defined.
