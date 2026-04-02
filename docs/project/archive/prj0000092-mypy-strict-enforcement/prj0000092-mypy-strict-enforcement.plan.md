# prj0000092-mypy-strict-enforcement - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Deliver phase-1 mypy strict-lane enforcement with deterministic TDD sequencing and narrow scope:
1. add a dedicated strict-lane config for the locked 6-module allowlist,
2. wire one blocking CI strict-lane command,
3. add structure tests and deterministic smoke fixture guardrails.

Scope is intentionally limited to strict-lane governance artifacts and guardrails defined in the design.

## Branch Gate
- Expected branch: `prj0000092-mypy-strict-enforcement`
- Observed branch: `prj0000092-mypy-strict-enforcement`
- Result: PASS

## Policy Compliance
- Code of conduct: PASS (planning-only content)
- Naming standards: PASS (all planned new files use `snake_case` conventions)

## Locked Phase-1 Allowlist
The strict lane must target exactly:
1. `src/core/audit/AuditEvent.py`
2. `src/core/audit/exceptions.py`
3. `src/core/resilience/CircuitBreakerConfig.py`
4. `src/core/resilience/CircuitBreakerState.py`
5. `src/core/resilience/exceptions.py`
6. `src/core/universal/exceptions.py`

## Acceptance Criteria
- AC-001: `mypy-strict-lane.ini` exists and sets `strict=True`, `ignore_errors=False`, `show_error_codes=True`, `warn_unused_ignores=True`.
- AC-002: `mypy-strict-lane.ini` `files` equals the locked phase-1 allowlist exactly.
- AC-003: `.github/workflows/ci.yml` contains blocking `python -m mypy --config-file mypy-strict-lane.ini` wiring with no non-blocking softeners.
- AC-004: Structure tests fail if allowlist or CI command contract drifts.
- AC-005: Deterministic strict-lane smoke test uses known-bad fixture and expects non-zero mypy exit.
- AC-006: Existing permissive global lane remains unchanged in `mypy.ini` during phase-1.

## Task Chunking For TDD
Single chunk (`chunk-001`) to keep handoff focused:
- Code/config files planned: 3
- Test files planned: 4
- Deterministic order: tests first (@5test), then implementation wiring (@6code), then integrated verification (@7exec).

## Task Roadmap

1. T1 - Strict-lane config contract tests (failing-first)
- Objective: Add failing structure tests for strict-lane config existence, key-value strictness, and exact allowlist lock.
- Target files: `tests/structure/test_mypy_strict_lane_config.py`
- Acceptance criteria: AC-001, AC-002, AC-004
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure/test_mypy_strict_lane_config.py
	```
- Dependency/order: first

2. T2 - CI strict-lane wiring tests (failing-first)
- Objective: Add/extend CI structure tests to require one blocking strict-lane mypy command and disallow soft-fail semantics.
- Target files: `tests/structure/test_ci_yaml.py`
- Acceptance criteria: AC-003, AC-004
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure/test_ci_yaml.py -k "mypy and strict and lane"
	```
- Dependency/order: after T1

3. T3 - Strict-lane smoke fixture + smoke test (failing-first)
- Objective: Add deterministic known-bad fixture and smoke test asserting strict-lane mypy non-zero exit.
- Target files: `tests/fixtures/mypy_strict_lane/bad_case.py`, `tests/test_zzc_mypy_strict_lane_smoke.py`
- Acceptance criteria: AC-005
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/test_zzc_mypy_strict_lane_smoke.py
	```
- Dependency/order: after T2

4. T4 - Implement strict-lane config file
- Objective: Create strict-lane config with locked allowlist and strict enforcement values.
- Target files: `mypy-strict-lane.ini`
- Acceptance criteria: AC-001, AC-002
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure/test_mypy_strict_lane_config.py
	python -m mypy --config-file mypy-strict-lane.ini
	```
- Dependency/order: after T3

5. T5 - Implement CI strict-lane command wiring
- Objective: Wire a blocking strict-lane mypy command into CI, isolated from sharded test fan-out.
- Target files: `.github/workflows/ci.yml`
- Acceptance criteria: AC-003
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure/test_ci_yaml.py -k "mypy and strict and lane"
	```
- Dependency/order: after T4

6. T6 - Preserve global permissive behavior
- Objective: Confirm phase-1 does not flip global `mypy.ini` behavior and preserve non-lane baseline.
- Target files: `mypy.ini`, `tests/test_zzb_mypy_config.py`
- Acceptance criteria: AC-006
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/test_zzb_mypy_config.py
	```
- Dependency/order: after T5

7. T7 - Evidence and scope guard recording
- Objective: Record deterministic command outcomes and verify file changes stayed inside strict-lane project scope.
- Target files: `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.test.md`, `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.exec.md`
- Acceptance criteria: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py tests/test_zzb_mypy_config.py
	python -m mypy --config-file mypy-strict-lane.ini
	git diff --name-only
	```
- Dependency/order: final

## Acceptance Mapping
| Task | Acceptance Criteria |
|---|---|
| T1 | AC-001, AC-002, AC-004 |
| T2 | AC-003, AC-004 |
| T3 | AC-005 |
| T4 | AC-001, AC-002 |
| T5 | AC-003 |
| T6 | AC-006 |
| T7 | AC-001, AC-002, AC-003, AC-004, AC-005, AC-006 |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M3.1 | Failing-first guardrails authored | T1-T3 | READY_FOR_@5test |
| M3.2 | Strict-lane config + CI wiring implemented | T4-T5 | PENDING_@6code |
| M3.3 | Global behavior preservation + evidence capture | T6-T7 | PENDING_@6code_@7exec |

## Validation Commands
### @5test (author failing tests first)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/structure/test_mypy_strict_lane_config.py
python -m pytest -q tests/structure/test_ci_yaml.py -k "mypy and strict and lane"
python -m pytest -q tests/test_zzc_mypy_strict_lane_smoke.py
python -m pytest -q tests/test_zzb_mypy_config.py
```

### @6code (implement to green)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py tests/test_zzb_mypy_config.py
python -m mypy --config-file mypy-strict-lane.ini
```

### @7exec (integration verification)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py tests/test_zzb_mypy_config.py
python -m mypy --config-file mypy-strict-lane.ini
python -m pytest -q
```

## Handoff
- Target agent: `@5test`
- Handoff condition: satisfied (`_Status: DONE_`, branch gate PASS, project status set to `READY_FOR_5TEST`).
