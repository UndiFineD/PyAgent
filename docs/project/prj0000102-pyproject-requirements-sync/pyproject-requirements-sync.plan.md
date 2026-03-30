# pyproject-requirements-sync - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-30_

## Overview
Deliver deterministic dependency-sync governance from the finalized design by implementing one canonical runtime authority,
one derived requirements artifact, and one blocking parity/policy CI gate.

Planned implementation is sequenced for downstream agents as:
1. @5test authors failing-first tests for generator, drift checks, and policy enforcement.
2. @6code implements minimal tooling/config changes to satisfy those tests.
3. @7exec runs full validation evidence.

## Branch Gate
- Expected branch: `prj0000102-pyproject-requirements-sync`
- Observed branch: `prj0000102-pyproject-requirements-sync`
- Result: PASS

## Policy Compliance
- Code of conduct: PASS (planning artifact only)
- Naming standards: PASS (all planned new file names are `snake_case`)

## Scope Boundaries
Implementation scope for this project is restricted to dependency-sync governance paths:
- `pyproject.toml`
- `requirements.txt`
- optional dependency sync script/config artifacts directly supporting deterministic derivation
- CI/policy checks that enforce parity and dependency rules
- project artifacts in `docs/project/prj0000102-pyproject-requirements-sync/`

Out of scope:
- runtime feature behavior changes
- unrelated module refactors
- broad packaging ecosystem migrations outside dependency-sync contracts

## Acceptance Criteria (From Design)
- AC-001: Canonical runtime dependency authority is `pyproject.toml` `[project.dependencies]`.
- AC-002: `requirements.txt` is deterministic derived output, not manually authoritative.
- AC-003: Drift between generated and committed requirements blocks CI.
- AC-004: Duplicate and malformed dependency protections are enforced.
- AC-005: Security-sensitive package spec policy is defined and enforced.
- AC-006: Changes remain bounded to dependency-sync governance scope.

## Phased Task Plan With Ownership

### Phase P1 - Failing-first contract tests (@5test)

1. T1 - Canonical source contract tests
- Objective: Add tests that fail unless dependency source is read from `[project.dependencies]` only.
- Owner: @5test
- Target files: `tests/`, `tests/structure/` selectors covering dependency source authority
- Acceptance criteria: AC-001
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests -k "dependency and canonical and pyproject"
	```
- Dependency/order: first

2. T2 - Derived requirements determinism tests
- Objective: Add failing tests asserting deterministic byte-equivalent `requirements.txt` output from identical inputs.
- Owner: @5test
- Target files: `tests/`, `tests/structure/` selectors covering deterministic emission
- Acceptance criteria: AC-002
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests -k "requirements and deterministic"
	```
- Dependency/order: after T1

3. T3 - Drift and CI blocking tests
- Objective: Add tests asserting CI/parity checks fail on generated-vs-committed mismatch.
- Owner: @5test
- Target files: `tests/structure/` and CI structure checks
- Acceptance criteria: AC-003
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure -k "dependency and drift and ci"
	```
- Dependency/order: after T2

4. T4 - Policy validator tests
- Objective: Add tests for duplicate lines, malformed specifiers, and critical package spec constraints.
- Owner: @5test
- Target files: `tests/`, `tests/structure/` selectors covering dependency policy checks
- Acceptance criteria: AC-004, AC-005
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests -k "dependency and policy"
	```
- Dependency/order: after T3

### Phase P2 - Minimal implementation to green (@6code)

5. T5 - Canonical reader + deterministic emitter implementation
- Objective: Implement/update dependency sync mechanism so output is deterministic and pyproject-driven.
- Owner: @6code
- Target files: `pyproject.toml`, `requirements.txt`, dependency-sync script/config artifacts (project-scoped)
- Acceptance criteria: AC-001, AC-002
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests -k "dependency and canonical and pyproject"
	python -m pytest -q tests -k "requirements and deterministic"
	```
- Dependency/order: after T4

6. T6 - Drift gate + policy enforcement wiring
- Objective: Wire blocking parity and dependency policy commands in CI and local verification surfaces.
- Owner: @6code
- Target files: CI workflow files and policy check integration files within project scope
- Acceptance criteria: AC-003, AC-004, AC-005
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/structure -k "dependency and drift and ci"
	python -m pytest -q tests -k "dependency and policy"
	```
- Dependency/order: after T5

### Phase P3 - Integration evidence and scope lock (@7exec)

7. T7 - End-to-end validation and scope verification
- Objective: Run deterministic evidence commands and confirm only dependency-sync governance files changed.
- Owner: @7exec
- Target files: `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.exec.md` and project-scoped touched files
- Acceptance criteria: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006
- Validation command:
	```powershell
	& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
	python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
	python -m pytest -q
	git diff --name-only
	```
- Dependency/order: final

## Acceptance-Criteria To Task Mapping
| Acceptance Criterion | Tasks |
|---|---|
| AC-001 | T1, T5, T7 |
| AC-002 | T2, T5, T7 |
| AC-003 | T3, T6, T7 |
| AC-004 | T4, T6, T7 |
| AC-005 | T4, T6, T7 |
| AC-006 | T7 |

## Milestones
| # | Milestone | Tasks | Owner | Status |
|---|---|---|---|---|
| M3.1 | Failing-first dependency contracts authored | T1-T4 | @5test | READY_FOR_@5test |
| M3.2 | Deterministic sync implementation and policy wiring complete | T5-T6 | @6code | PENDING_@6code |
| M3.3 | Integrated evidence and scope-lock verification complete | T7 | @7exec | PENDING_@7exec |

## Validation Commands

### @5test
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests -k "dependency and canonical and pyproject"
python -m pytest -q tests -k "requirements and deterministic"
python -m pytest -q tests/structure -k "dependency and drift and ci"
python -m pytest -q tests -k "dependency and policy"
```

### @6code
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests -k "dependency and canonical and pyproject"
python -m pytest -q tests -k "requirements and deterministic"
python -m pytest -q tests/structure -k "dependency and drift and ci"
python -m pytest -q tests -k "dependency and policy"
```

### @7exec
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python -m pytest -q
git diff --name-only
```

## Handoff Readiness Criteria For @5test
Handoff is READY when all of the following are true:
1. This plan remains `_Status: DONE_` with complete objective/file/acceptance/validation entries per task.
2. Branch gate remains PASS on `prj0000102-pyproject-requirements-sync`.
3. Required docs policy validation command passes:
	 - `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
4. Scope remains bounded to dependency-sync governance and project artifact files.
5. @5test starts from T1 and executes tasks sequentially through T4 before @6code work begins.

## Handoff
- Target agent: `@5test`
- Handoff condition: satisfied (plan finalized, branch gate PASS, docs-policy validation required and executed in this @4plan step)
