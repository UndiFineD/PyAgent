# openapi-spec-generation - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-03_

## Overview
Deliver the phase-one backend-only OpenAPI contract lane defined by Option A and ADR-0007 without broadening scope beyond the committed schema pipeline. This plan keeps `backend/app.py` as the only schema authority, adds an explicit generator command, introduces a narrow drift test and CI selector, and preserves MkDocs as a consumer of the committed artifact rather than a generator.

In scope for implementation:
1. Explicit generation script for the backend schema.
2. Committed schema artifact at `docs/api/openapi/backend_openapi.json`.
3. Narrow read-only drift test for `backend.app.openapi()` parity.
4. Lightweight CI selector wiring for the drift check.
5. Consumer-only docs link to the committed JSON artifact.

Out of scope for implementation:
1. Schema generation for `src/github_app.py` or `src/chat/api.py`.
2. MkDocs build ownership of schema generation.
3. Broader FastAPI metadata refactors outside what is required to keep backend generation deterministic.
4. SDK generation, rendered OpenAPI pages, or multi-spec aggregation.

## Branch Gate
- Project ID: prj0000120
- Expected branch: prj0000120-openapi-spec-generation
- Observed branch: prj0000120-openapi-spec-generation
- Result: PASS

## Scope Guardrails
- Planning-scope files updated in this step: this plan file, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/2026-04-03.4plan.log.md`.
- Downstream implementation ownership is limited to: `scripts/generate_backend_openapi.py`, `docs/api/openapi/backend_openapi.json`, `tests/docs/test_backend_openapi_drift.py`, `.github/workflows/ci.yml`, `docs/api/index.md`, and project handoff artifacts under `docs/project/prj0000120-openapi-spec-generation/`.
- `backend/app.py` is a read-only schema authority in this slice. If downstream work requires behavior changes here to make generation deterministic, stop and return to `@0master` for scope review instead of expanding silently.
- Any import of `src/github_app.py` or `src/chat/api.py` in generator, test, or CI paths is BLOCKED.

## AC and Interface Traceability
| Task ID | AC Coverage | Interface Coverage |
|---|---|---|
| T-OAS-001 | AC-OAS-003, AC-OAS-007 | IFACE-OAS-004, IFACE-OAS-007 |
| T-OAS-002 | AC-OAS-001, AC-OAS-002, AC-OAS-006 | IFACE-OAS-001, IFACE-OAS-002, IFACE-OAS-003, IFACE-OAS-007 |
| T-OAS-003 | AC-OAS-005 | IFACE-OAS-006 |
| T-OAS-004 | AC-OAS-004 | IFACE-OAS-005 |
| T-OAS-005 | AC-OAS-001..AC-OAS-006 | IFACE-OAS-001..IFACE-OAS-007 |
| T-OAS-006 | AC-OAS-001..AC-OAS-006 | IFACE-OAS-001..IFACE-OAS-007 |
| T-OAS-007 | AC-OAS-001..AC-OAS-006 | IFACE-OAS-001..IFACE-OAS-007 |

## Chunking Strategy
- Chunk C1 (contract and implementation lane): T-OAS-001..T-OAS-004.
	- Estimated implementation files: 5 (`scripts/generate_backend_openapi.py`, `docs/api/openapi/backend_openapi.json`, `tests/docs/test_backend_openapi_drift.py`, `.github/workflows/ci.yml`, `docs/api/index.md`).
	- Estimated project handoff files: 1 to 2 (`openapi-spec-generation.test.md`, optional `openapi-spec-generation.code.md` evidence).
- Chunk C2 (execution, quality, and git closure): T-OAS-005..T-OAS-007.
	- Estimated execution files: 3 (`openapi-spec-generation.exec.md`, `openapi-spec-generation.ql.md`, `openapi-spec-generation.git.md`).

## Task List
| Task ID | Parallel Class | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|---|
| T-OAS-001 | sequential-only | @5test | Author the narrow backend-only drift test contract and failing-first selector set before generator implementation. | `tests/docs/test_backend_openapi_drift.py`, `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.test.md` | Drift test compares committed vs generated backend schema in read-only mode, names `backend.app` as the only import target, and records fail/pass expectations for AC-OAS-003 and AC-OAS-006. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_backend_openapi_drift.py` |
| T-OAS-002 | sequential-only | @6code | Implement the explicit backend generator and produce the committed canonical artifact without touching other FastAPI apps. | `scripts/generate_backend_openapi.py`, `docs/api/openapi/backend_openapi.json` | Generator exits `0`, writes only `docs/api/openapi/backend_openapi.json`, uses deterministic JSON formatting, and imports `backend.app` only (AC-OAS-001, AC-OAS-002, AC-OAS-006). | `c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/generate_backend_openapi.py` |
| T-OAS-003 | parallel-safe | @6code | Link narrative docs to the committed JSON artifact while preserving MkDocs as a static consumer only. | `docs/api/index.md` | Docs page links to `openapi/backend_openapi.json` and does not introduce generation logic or MkDocs build hooks (AC-OAS-005). | `rg -n "openapi/backend_openapi.json|OpenAPI|backend schema" docs/api/index.md` |
| T-OAS-004 | parallel-safe | @6code | Add the lightweight CI drift selector without adding generation or MkDocs build responsibilities. | `.github/workflows/ci.yml` | Quick CI path runs only `pytest tests/docs/test_backend_openapi_drift.py -q`, stays read-only, and adds no schema-generation step (AC-OAS-004). | `rg -n "test_backend_openapi_drift.py|pytest .*backend_openapi_drift|mkdocs build|generate_backend_openapi" .github/workflows/ci.yml` |
| T-OAS-005 | sequential-only (convergence) | @7exec | Execute the generator, drift selector, and docs policy gate as the convergence barrier for all phase-one deliverables. | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.exec.md` | Evidence pack captures generator output, drift-selector pass/fail state, docs-policy status, and confirms only approved files changed in Chunk C1. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_backend_openapi_drift.py` |
| T-OAS-006 | sequential-only | @8ql | Verify quality/security closure for backend-only scope, read-only drift behavior, and consumer-only docs publication. | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.ql.md` | Review proves no secondary-app imports, no file writes during drift checks, no MkDocs generation coupling, and ADR-0007 consequences remain honored. | `rg -n "backend\.app|github_app|chat/api|openapi\(|write_text|json.dump" scripts/generate_backend_openapi.py tests/docs/test_backend_openapi_drift.py` |
| T-OAS-007 | sequential-only | @9git | Complete scoped git handoff with branch validation, narrow staging proof, and artifact traceability. | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.git.md` | Handoff packet records branch match, approved file list, validation commands executed, and links back to this plan plus ADR-0007. | `git status --short` |

## Parallelization and Sequencing
- Sequential hard constraints:
	1. T-OAS-001 must complete before T-OAS-002 so the drift contract exists before generator implementation.
	2. T-OAS-002 must complete before T-OAS-003 because the docs link must reference the committed artifact path produced by the generator lane.
	3. T-OAS-002 must complete before T-OAS-004 so CI points at the finalized selector and artifact contract.
	4. T-OAS-005 waits for T-OAS-003 and T-OAS-004 as the convergence barrier.
	5. T-OAS-006 waits for T-OAS-005 evidence.
	6. T-OAS-007 waits for T-OAS-006 closure.
- Parallel-safe boundary:
	1. T-OAS-003 and T-OAS-004 are parallel-safe after T-OAS-002.
	2. T-OAS-003 exclusively owns `docs/api/index.md`.
	3. T-OAS-004 exclusively owns `.github/workflows/ci.yml`.
- Convergence step:
	1. T-OAS-005 is the required sync barrier.
	2. `@7exec` owns the merge decision for Chunk C1 outputs and must reject the handoff if T-OAS-003/T-OAS-004 introduce extra file writes or broaden scope.

## File Ownership Map
| Work Package | Owner | Files |
|---|---|---|
| WP1 - Drift contract | @5test | `tests/docs/test_backend_openapi_drift.py`, `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.test.md` |
| WP2 - Generator and committed artifact | @6code | `scripts/generate_backend_openapi.py`, `docs/api/openapi/backend_openapi.json` |
| WP3 - Docs consumer link | @6code | `docs/api/index.md` |
| WP4 - CI drift enforcement | @6code | `.github/workflows/ci.yml` |
| WP5 - Execution evidence | @7exec | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.exec.md` |
| WP6 - Quality closure | @8ql | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.ql.md` |
| WP7 - Git handoff | @9git | `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.git.md` |

## Agent Validation Contracts and Evidence Expectations
### @5test Contract
- Deliverables:
	1. `tests/docs/test_backend_openapi_drift.py` with deterministic canonicalization and read-only comparison behavior.
	2. `openapi-spec-generation.test.md` mapping selectors to AC-OAS-001..AC-OAS-006.
- Required evidence:
	1. Pre-implementation selector output showing the red state or missing-artifact state.
	2. Explicit assertion that no test path regenerates the artifact automatically.

### @6code Contract
- Deliverables:
	1. Explicit generator script and committed JSON artifact.
	2. Docs link and CI selector updates with no other workflow expansion.
- Required evidence:
	1. Generator command transcript with exit code `0`.
	2. Diff proof that only the committed artifact path is written by the generator.
	3. `rg` proof that only `backend.app` appears in generator and drift-test imports.

### @7exec Contract
- Deliverables:
	1. `openapi-spec-generation.exec.md` evidence log.
- Required evidence:
	1. Generator command transcript.
	2. Drift selector transcript.
	3. Docs policy selector transcript.
	4. Changed-file list limited to approved scope.

### @8ql Contract
- Deliverables:
	1. `openapi-spec-generation.ql.md` closure review.
- Required evidence:
	1. Scope audit showing no `src/github_app.py` or `src/chat/api.py` imports.
	2. CI audit showing no generation step and no `mkdocs build` addition.
	3. Claim-to-ADR traceability against `docs/architecture/adr/0007-script-first-backend-openapi-artifact-governance.md`.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Red contract established | T-OAS-001 | PLANNED |
| M2 | Generator and artifact committed | T-OAS-002 | PLANNED |
| M3 | Parallel docs and CI touch points complete | T-OAS-003, T-OAS-004 | PLANNED |
| M4 | Execution convergence complete | T-OAS-005 | PLANNED |
| M5 | Quality and git closure ready | T-OAS-006, T-OAS-007 | PLANNED |

## Validation Commands by Milestone
### M1
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_backend_openapi_drift.py
```

### M2
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/generate_backend_openapi.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_backend_openapi_drift.py
```

### M3
```powershell
rg -n "openapi/backend_openapi.json|OpenAPI|backend schema" docs/api/index.md
rg -n "test_backend_openapi_drift.py|pytest .*backend_openapi_drift|mkdocs build|generate_backend_openapi" .github/workflows/ci.yml
```

### M4
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/generate_backend_openapi.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_backend_openapi_drift.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
git diff --name-only
```

### M5
```powershell
rg -n "backend\.app|github_app|chat/api|openapi\(|write_text|json.dump" scripts/generate_backend_openapi.py tests/docs/test_backend_openapi_drift.py
git branch --show-current
git status --short
```

## Handoff Package to @5test
1. Start with T-OAS-001 only.
2. Keep the first red selector limited to `tests/docs/test_backend_openapi_drift.py`; do not broaden into docs builds or multi-app schema coverage.
3. Treat the committed artifact path as fixed: `docs/api/openapi/backend_openapi.json`.
4. If the red test indicates `backend/app.py` must change to stabilize schema generation, stop and escalate instead of mutating runtime behavior inside this project.

## Validation Evidence (Planning Update)
- Executed: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
- Result: `17 passed in 6.16s`
- Disposition: plan artifact, current memory update, and daily log update are governance-compliant and ready for downstream handoff.