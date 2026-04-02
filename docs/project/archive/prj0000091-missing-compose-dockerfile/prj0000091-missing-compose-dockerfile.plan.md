# prj0000091-missing-compose-dockerfile - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Deliver a minimal, deterministic fix for missing compose Dockerfile references by:
1. correcting `deploy/compose.yaml` to use `deploy/Dockerfile.pyagent`,
2. adding `deploy/Dockerfile.pyagent`,
3. adding regression guard tests that fail if compose Dockerfile paths do not exist.

Scope remains limited to compose reference correction, Dockerfile addition, and regression guard coverage.

## Requirements and Constraints
- REQ-001: `deploy/compose.yaml` must not reference a missing Dockerfile path.
- REQ-002: `pyagent` compose service must use deploy-local Dockerfile strategy (`deploy/Dockerfile.pyagent`).
- REQ-003: Regression guard must deterministically fail on missing compose Dockerfile references.
- CON-001: No broad deploy stack redesign or unrelated service changes.
- CON-002: Branch must remain `prj0000091-missing-compose-dockerfile` through @5test handoff.
- GUD-001: All tasks must include objective, target files, acceptance criteria, and validation command.

## Chunk Plan
Single chunk (`chunk-001`) sized for focused handoff:
- Code files: `deploy/compose.yaml`, `deploy/Dockerfile.pyagent`
- Test files: `tests/deploy/test_compose_dockerfile_paths.py`

## Task List
- [ ] T1 - Compose reference correction
	- Objective: Update compose contract so `pyagent` points to existing deploy-local Dockerfile path.
	- Target files: `deploy/compose.yaml`
	- Acceptance: AC-001, AC-002
	- Validation command:
		```powershell
		& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
		python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py -k compose_reference_contract
		```
	- Dependency order: first

- [ ] T2 - Add deploy Dockerfile
	- Objective: Create `deploy/Dockerfile.pyagent` with viable build instructions for compose `pyagent` service.
	- Target files: `deploy/Dockerfile.pyagent`
	- Acceptance: AC-003
	- Validation command:
		```powershell
		& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
		python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py -k dockerfile_exists_contract
		```
	- Dependency order: after T1

- [ ] T3 - Add regression guard tests
	- Objective: Add deterministic tests that parse compose build entries and fail with actionable output for missing Dockerfile paths.
	- Target files: `tests/deploy/test_compose_dockerfile_paths.py`
	- Acceptance: AC-004
	- Validation command:
		```powershell
		& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
		python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
		```
	- Dependency order: after T2

- [ ] T4 - Capture execution evidence
	- Objective: Record reproducible validation command outcomes in project execution artifact.
	- Target files: `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.exec.md`
	- Acceptance: AC-005
	- Validation command:
		```powershell
		& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
		python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
		docker compose -f deploy/compose.yaml config
		```
	- Dependency order: after T3

- [ ] T5 - Scope guard verification
	- Objective: Confirm only in-scope files changed for this project and non-goals remain untouched.
	- Target files: `deploy/compose.yaml`, `deploy/Dockerfile.pyagent`, `tests/deploy/test_compose_dockerfile_paths.py`, `docs/project/prj0000091-missing-compose-dockerfile/*`
	- Acceptance: AC-006
	- Validation command:
		```powershell
		git diff --name-only
		```
	- Dependency order: final

## Acceptance Mapping
| Task | Acceptance Criteria |
|---|---|
| T1 | AC-001, AC-002 |
| T2 | AC-003 |
| T3 | AC-004 |
| T4 | AC-005 |
| T5 | AC-006 |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M3.1 | Compose contract fixed | T1 | PLANNED |
| M3.2 | Dockerfile in place | T2 | PLANNED |
| M3.3 | Regression guard active | T3 | PLANNED |
| M3.4 | Execution evidence + scope guard | T4-T5 | PLANNED |

## Validation Commands
### @5test (author failing-first tests)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
```

### @6code (implement to green)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
docker compose -f deploy/compose.yaml config
```

### @7exec (integration verification)
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
docker compose -f deploy/compose.yaml config
docker compose -f deploy/compose.yaml build pyagent
```

## Handoff
- Target agent: `@5test`
- Handoff condition: satisfied (`_Status: DONE_`, project status `READY_FOR_5TEST`, branch gate PASS).
