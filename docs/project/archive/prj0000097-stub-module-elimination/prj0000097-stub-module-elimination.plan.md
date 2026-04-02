# prj0000097-stub-module-elimination - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-29_

## Overview
Slice 1 delivers deterministic behavior for `rl` and `speculation` while keeping temporary
deprecated `validate()` shims. Sequence is strict TDD: @5test writes failing tests first,
then @6code implements in-scope module logic and finalizes test inventory closure.

## Scope And Guardrails
- In scope: `src/rl/__init__.py`, `src/speculation/__init__.py`, and related tests/guards.
- Out of scope: all `runtime*`, `memory*`, and `cort*` implementation files.
- Branch gate: expected and observed branch is `prj0000097-stub-module-elimination`.
- Delivery rule: no skeleton or placeholder-only deliverables.

## Acceptance Mapping
- AC-001: RL discounted return correctness, including empty input.
	Verify: `tests/rl/test_discounted_return.py`
- AC-002: RL rejects invalid `gamma` and non-finite rewards.
	Verify: `tests/rl/test_discounted_return.py`
- AC-003: Speculation threshold and top candidate selection are correct.
	Verify: `tests/speculation/test_select_candidate.py`
- AC-004: Speculation tie-break is deterministic and lexicographic.
	Verify: `tests/speculation/test_select_candidate.py`
- AC-005: Legacy `validate()` shims emit warnings and remain callable.
	Verify: `tests/rl/test_rl_deprecation.py`, `tests/speculation/test_speculation_deprecation.py`
- AC-006: Import guard blocks unauthorized new imports of `rl` and `speculation`.
	Verify: `tests/guards/test_rl_speculation_import_scope.py`
- AC-007: Import-smoke focus is replaced by behavior and deprecation coverage.
	Verify: inventory in `tests/rl/` and `tests/speculation/`
- AC-008: No out-of-scope implementation edits in runtime/memory/cort lanes.
	Verify: scoped git diff review

## Slice 1 Task List (TDD Sequence)
- [ ] T1 - RL behavior tests
	Owner: @5test
	Objective: Add deterministic return tests for formula correctness and empty input.
	Target files: `tests/rl/test_discounted_return.py`
	Acceptance: AC-001
	Validation command: `python -m pytest -q tests/rl/test_discounted_return.py`
	Pass criteria: tests fail before code, then pass after code without flaky assertions.

- [ ] T2 - RL invalid-input tests
	Owner: @5test
	Objective: Assert `ValueError` for invalid `gamma` and non-finite rewards.
	Target files: `tests/rl/test_discounted_return.py`
	Acceptance: AC-002
	Validation command: `python -m pytest -q tests/rl/test_discounted_return.py`
	Pass criteria: all invalid paths are covered and deterministic.

- [ ] T3 - Speculation behavior tests
	Owner: @5test
	Objective: Cover threshold filter, highest-score pick, tie-break, and empty input.
	Target files: `tests/speculation/test_select_candidate.py`
	Acceptance: AC-003, AC-004
	Validation command: `python -m pytest -q tests/speculation/test_select_candidate.py`
	Pass criteria: tie behavior is lexicographic and stable across runs.

- [ ] T4 - Deprecation tests for legacy shims
	Owner: @5test
	Objective: Assert warnings and call compatibility for both `validate()` shims.
	Target files: `tests/rl/test_rl_deprecation.py`, `tests/speculation/test_speculation_deprecation.py`
	Acceptance: AC-005
	Validation command: `python -m pytest -q tests/rl/test_rl_deprecation.py`
	Validation command: `python -m pytest -q tests/speculation/test_speculation_deprecation.py`
	Pass criteria: warning type/message and return compatibility are asserted.

- [ ] T5 - Import-scope guard test
	Owner: @5test
	Objective: Block unauthorized new imports of `rl` and `speculation`.
	Target files: `tests/guards/test_rl_speculation_import_scope.py`
	Acceptance: AC-006
	Validation command: `python -m pytest -q tests/guards/test_rl_speculation_import_scope.py`
	Pass criteria: unauthorized imports fail; approved locations pass.

- [ ] T6 - RL implementation
	Owner: @6code
	Objective: Implement `discounted_return()` and deprecating `validate()` shim.
	Target files: `src/rl/__init__.py`
	Acceptance: AC-001, AC-002, AC-005
	Validation command: `python -m pytest -q tests/rl/test_discounted_return.py tests/rl/test_rl_deprecation.py`
	Pass criteria: RL suite green with no runtime/memory/cort implementation edits.

- [ ] T7 - Speculation implementation
	Owner: @6code
	Objective: Implement `select_candidate()` and deprecating `validate()` shim.
	Target files: `src/speculation/__init__.py`
	Acceptance: AC-003, AC-004, AC-005
	Validation command: `python -m pytest -q tests/speculation/test_select_candidate.py`
	Validation command: `python -m pytest -q tests/speculation/test_speculation_deprecation.py`
	Pass criteria: speculation suite green with deterministic tie-break behavior.

- [ ] T8 - Inventory and guardrail closure
	Owner: @6code
	Objective: Replace import-smoke focus and finalize guard coverage without scope drift.
	Target files: `tests/test_rl_package.py`, `tests/test_speculation_package.py`, `tests/rl/`
	Target files: `tests/speculation/`, `tests/guards/test_rl_speculation_import_scope.py`
	Acceptance: AC-006, AC-007, AC-008
	Validation command: `python -m pytest -q tests/rl tests/speculation tests/guards/test_rl_speculation_import_scope.py`
	Pass criteria: behavior/deprecation coverage is primary; scope gate remains clean.

## Dependency Order
1. T1 -> T2 -> T3 -> T4 -> T5 (all @5test, tests must exist and fail first).
2. T6 depends on T1-T2 and must make RL tests green.
3. T7 depends on T3-T4 and must make speculation tests green.
4. T8 depends on T5-T7 and closes inventory/scope criteria.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Test contracts authored (red) | T1-T5 | PLANNED FOR @5test |
| M2 | RL implementation green | T6 | PLANNED FOR @6code |
| M3 | Speculation implementation green | T7 | PLANNED FOR @6code |
| M4 | Guardrails and inventory closure | T8 | PLANNED FOR @6code |

## Validation Commands
Targeted (run first):
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/rl/test_discounted_return.py
python -m pytest -q tests/speculation/test_select_candidate.py
python -m pytest -q tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py
python -m pytest -q tests/guards/test_rl_speculation_import_scope.py
```

Broader (run after targeted commands are green):
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/rl tests/speculation tests/guards/test_rl_speculation_import_scope.py
python -m pytest -q
```

Pass criteria:
- All targeted commands exit with status 0.
- Broader slice suite exits with status 0.
- Full `python -m pytest -q` has no new failures attributable to Slice 1.
- Diff contains no edits to out-of-scope implementation areas (`runtime*`, `memory*`, `cort*`).
