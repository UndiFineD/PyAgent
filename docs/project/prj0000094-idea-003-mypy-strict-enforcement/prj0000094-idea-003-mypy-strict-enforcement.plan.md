# prj0000094-idea-003-mypy-strict-enforcement - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Deliver deterministic, wave-based expansion of mypy strict-lane enforcement (Option A) while preserving blocking CI semantics, exact config contracts, and rollback safety.

Branch gate validation:
1. Expected branch (`project.md`): `prj0000094-idea-003-mypy-strict-enforcement`
2. Observed branch: `prj0000094-idea-003-mypy-strict-enforcement`
3. Result: PASS

Scope boundary for this planning cycle:
1. Plan artifact update in this project folder (this file).
2. Downstream implementation/testing tasks target typed-enforcement files outside this folder as listed below.

## Wave Plan
### Wave 0 (Baseline - already active)
1. Keep current 6-file allowlist and strict-lane blocking behavior unchanged.

### Wave 1 (Concrete scope candidates)
Candidate files to add to `mypy-strict-lane.ini` `[mypy] files` allowlist:
1. `src/core/fuzzing/exceptions.py`
2. `src/core/n8nbridge/exceptions.py`
3. `src/core/replay/exceptions.py`
4. `src/core/sandbox/SandboxViolationError.py`

Wave 1 cap:
1. 4 files in this wave (within design max <= 10).

### Wave 2 (Planned, gated)
Candidate files (only after Wave 1 gates pass):
1. `src/core/fuzzing/FuzzResult.py`
2. `src/core/fuzzing/FuzzCase.py`
3. `src/core/replay/ReplayEnvelope.py`

### Wave 3 (Planned, gated)
Candidate files (only after Wave 2 gates pass):
1. `src/core/n8nbridge/N8nBridgeConfig.py`
2. `src/core/resilience/CircuitBreakerRegistry.py`
3. `src/core/replay/ReplayStore.py`

## Task List
- [ ] T1 - Baseline strict-lane contract freeze and Wave 1 branch-safe prep.
	- Objective: confirm baseline contract, keep strict lane deterministic before introducing Wave 1 test deltas.
	- Target files: `mypy-strict-lane.ini`, `tests/structure/test_mypy_strict_lane_config.py`, `tests/structure/test_ci_yaml.py`, `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`
	- Acceptance criteria: AC-02, AC-03, AC-04
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

- [ ] T2 - TDD gate: author/adjust Wave 1 guard tests first (expected to fail pre-implementation).
	- Objective: encode Wave 1 allowlist and governance expectations before changing strict-lane config.
	- Target files: `tests/structure/test_mypy_strict_lane_config.py`, `tests/structure/test_ci_yaml.py`, `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`, `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.test.md`
	- Acceptance criteria: AC-01, AC-02, AC-03, AC-04, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

- [ ] T3 - Implement Wave 1 strict-lane allowlist expansion.
	- Objective: expand strict lane to the concrete Wave 1 candidate files while preserving strict flags.
	- Target files: `mypy-strict-lane.ini`, `tests/structure/test_mypy_strict_lane_config.py`
	- Acceptance criteria: AC-01, AC-02, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m mypy --config-file mypy-strict-lane.ini`

- [ ] T4 - Preserve CI blocking semantics and explicit strict-lane command contract.
	- Objective: ensure CI still runs strict lane as blocking with no soft-fail patterns.
	- Target files: `.github/workflows/ci.yml`, `tests/structure/test_ci_yaml.py`
	- Acceptance criteria: AC-03, AC-06, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_ci_yaml.py`

- [ ] T5 - Preserve deterministic behavioral smoke contract for strict lane.
	- Objective: keep known-bad fixture behavior deterministic after allowlist expansion.
	- Target files: `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`, `tests/fixtures/mypy_strict_lane/bad_case.py`
	- Acceptance criteria: AC-04, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

- [ ] T6 - Wave governance documentation sync and rollback trigger codification.
	- Objective: record Wave 1 gate results, promotion criteria, and rollback path in project artifacts.
	- Target files: `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.plan.md`, `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.test.md`, `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.exec.md`
	- Acceptance criteria: AC-01, AC-05, AC-06, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

- [ ] T7 - Promotion-gate execution for Wave 1.
	- Objective: enforce gate sequence before declaring Wave 1 complete.
	- Target files: `mypy-strict-lane.ini`, `tests/structure/test_mypy_strict_lane_config.py`, `tests/structure/test_ci_yaml.py`, `tests/zzz/test_zzc_mypy_strict_lane_smoke.py`, `.github/workflows/ci.yml`
	- Acceptance criteria: AC-01, AC-02, AC-03, AC-04, AC-06, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py; python -m mypy --config-file mypy-strict-lane.ini`

- [ ] T8 - Wave 2/Wave 3 readiness checkpoints (no implementation until gate pass).
	- Objective: stage next-wave candidate sets and dependency order without changing config scope early.
	- Target files: `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.plan.md`, `docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.test.md`
	- Acceptance criteria: AC-01, AC-05, AC-06, AC-07
	- Validation command:
		- `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py`

## Dependency Order
1. T1 -> T2 -> T3
2. T4 and T5 start after T3 and may run in parallel.
3. T6 starts after T4 and T5 pass.
4. T7 runs after T6.
5. T8 starts only after T7 gate completion.

## TDD Sequencing (Test-First Policy)
1. @5test implements T2 tests first and verifies failing state against pre-Wave-1 baseline.
2. @6code executes T3/T4/T5 implementation only after T2 failure evidence is recorded.
3. @7exec runs T7 gate commands and confirms promotion criteria.
4. No Wave 2 scope changes until T7 is green and logged.

## Rollback Checkpoints
### RC-1 (Pre-Wave-1)
1. Trigger: T2 tests fail for reasons unrelated to planned allowlist delta.
2. Action: revert T2 test deltas only; keep baseline config untouched.
3. Validation:
	 - `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

### RC-2 (Post-T3, Pre-promotion)
1. Trigger: strict-lane config expansion causes unstable CI or non-contract failures.
2. Action: remove latest Wave 1 entries from `mypy-strict-lane.ini` and restore expected allowlist test lock.
3. Validation:
	 - `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m mypy --config-file mypy-strict-lane.ini; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py`

### RC-3 (Post-promotion)
1. Trigger: repeated strict-lane failures during observation window (default 5 green CI runs not achieved).
2. Action: rollback latest wave entries, record cause in project artifacts, reduce next candidate set.
3. Validation:
	 - `& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`

## Acceptance Traceability
| Task | AC Coverage |
|---|---|
| T1 | AC-02, AC-03, AC-04 |
| T2 | AC-01, AC-02, AC-03, AC-04, AC-07 |
| T3 | AC-01, AC-02, AC-07 |
| T4 | AC-03, AC-06, AC-07 |
| T5 | AC-04, AC-07 |
| T6 | AC-01, AC-05, AC-06, AC-07 |
| T7 | AC-01, AC-02, AC-03, AC-04, AC-06, AC-07 |
| T8 | AC-01, AC-05, AC-06, AC-07 |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Wave 1 TDD gate authored | T1-T2 | PLANNED |
| M2 | Wave 1 implementation merged | T3-T5 | PLANNED |
| M3 | Governance and promotion evidence recorded | T6-T7 | PLANNED |
| M4 | Next-wave readiness staged | T8 | PLANNED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/structure/test_mypy_strict_lane_config.py
python -m pytest -q tests/structure/test_ci_yaml.py
python -m pytest -q tests/zzz/test_zzc_mypy_strict_lane_smoke.py
python -m mypy --config-file mypy-strict-lane.ini
```
