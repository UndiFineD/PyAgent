# prj0000099-stub-module-elimination - Implementation Plan

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-03-29_

## Overview
Validation-first closure for stub-module-elimination. This plan schedules only evidence
collection and closure artifacts: verify non-empty package APIs, run focused package tests,
record code/test/exec/ql evidence, then prepare @9git handoff.

## Task List
- [ ] T1 - Verify non-empty APIs for target packages
	- Objective: prove each target package exposes substantive API content and is not a stub-only surface.
	- Target files: `src/rl/__init__.py`, `src/speculation/__init__.py`, `src/cort/__init__.py`, `src/runtime_py/__init__.py`, `src/runtime/__init__.py`, `src/memory/__init__.py`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md`
	- Acceptance: AC-099-01 passes with explicit evidence rows captured in code artifact.
	- Validation command: `python -c "from pathlib import Path; fs=['src/rl/__init__.py','src/speculation/__init__.py','src/cort/__init__.py','src/runtime_py/__init__.py','src/runtime/__init__.py','src/memory/__init__.py']; bad=[f for f in fs if not any(l.strip() and not l.strip().startswith('#') for l in Path(f).read_text(encoding='utf-8').splitlines())]; print('PASS' if not bad else 'FAIL:' + ','.join(bad)); raise SystemExit(1 if bad else 0)"`
- [ ] T2 - Run focused package regression tests
	- Objective: confirm targeted package import and behavior surfaces remain green.
	- Target files: `tests/test_rl_package.py`, `tests/test_speculation_package.py`, `tests/test_cort.py`, `tests/test_memory_package.py`, `tests/test_runtime.py`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md`
	- Acceptance: AC-099-02 passes with all selected tests green.
	- Validation command: `python -m pytest -q tests/test_rl_package.py tests/test_speculation_package.py tests/test_cort.py tests/test_memory_package.py tests/test_runtime.py`
- [ ] T3 - Record code/test/exec/ql closure artifacts
	- Objective: capture deterministic evidence in project artifacts for audit-ready closure.
	- Target files: `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.exec.md`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.ql.md`
	- Acceptance: each artifact contains executed evidence and non-placeholder status content.
	- Validation command: `rg -n "_Status:|Validation Results|Run Log|Findings|Cleared" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.exec.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.ql.md`
- [ ] T4 - Update milestones and prepare @9git handoff packet
	- Objective: mark closure progress and stage final governance handoff metadata.
	- Target files: `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.plan.md`, `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.git.md`
	- Acceptance: milestone statuses reflect closure state and handoff target is @9git.
	- Validation command: `rg -n "Milestone|M8|@9git|_Status:" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.plan.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.git.md`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M3 | Plan finalized for validation-first closure | T1-T4 | IN_PROGRESS |
| M4 | Test evidence captured | T2-T3 | ACTIONABLE |
| M5 | Code artifact evidence captured | T1-T3 | ACTIONABLE |
| M6 | Execution evidence captured | T2-T3 | ACTIONABLE |
| M7 | Security/QL evidence captured | T3 | ACTIONABLE |
| M8 | Handoff packet ready for @9git | T4 | ACTIONABLE |

## Validation Commands
```powershell
python -c "from pathlib import Path; fs=['src/rl/__init__.py','src/speculation/__init__.py','src/cort/__init__.py','src/runtime_py/__init__.py','src/runtime/__init__.py','src/memory/__init__.py']; bad=[f for f in fs if not any(l.strip() and not l.strip().startswith('#') for l in Path(f).read_text(encoding='utf-8').splitlines())]; print('PASS' if not bad else 'FAIL:' + ','.join(bad)); raise SystemExit(1 if bad else 0)"
python -m pytest -q tests/test_rl_package.py tests/test_speculation_package.py tests/test_cort.py tests/test_memory_package.py tests/test_runtime.py
rg -n "_Status:|Validation Results|Run Log|Findings|Cleared" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.code.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.test.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.exec.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.ql.md
rg -n "Milestone|M8|@9git|_Status:" docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.plan.md docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.git.md
python -m pytest -q
```
