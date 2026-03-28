# projectmanager-ideas-autosync - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
- There is no current backend endpoint that reads `docs/project/ideas/*.md`, so Project Manager cannot auto-ingest idea documents.
- Project Manager currently consumes only `/api/projects` and renders Kanban projects; it has no ideas feed or exclusion logic.
- Idea files already contain useful matching metadata (`Planned project mapping:`), but implemented overlap is not normalized into a deterministic API contract.
- "Implemented" is currently ambiguous: it could mean Released-only or any non-Ideas active/released project state.

## Constraint Mapping
- Must keep scope to project docs plus memory in this phase; no production code edits in @2think.
- Must respect one-project-one-branch governance (`prj0000093-projectmanager-ideas-autosync`).
- Must align with existing backend-first consumption pattern used by Project Manager (`/api/projects`).
- Must preserve lane governance in `docs/project/kanban.md` and `data/projects.json` semantics.
- Must remain minimal-risk for @3design: additive API contract, no lane policy rewrite.

## Research Evidence
| Task Type | Finding | Evidence |
|---|---|---|
| Literature review | Project goal explicitly requires ideas ingestion + exclusion of implemented ideas. | `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md` |
| Literature review | Kanban lane definitions make Discovery+ states active lifecycle, Released merged, Archived terminal. | `docs/project/kanban.md` |
| Alternative enumeration | Three viable implementation boundaries exist: frontend-only filtering, backend filtering with mode, backend materialized map. | `web/apps/ProjectManager.tsx`, `backend/app.py` |
| Prior-art search | Similar @2think structure with option matrix and risk-to-testability mapping already used successfully. | `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`, `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md` |
| Prior-art search | Idea files already encode overlap hints via `Planned project mapping` (many mapped to Released projects). | `docs/project/ideas/idea000050-inference-speculative-decoding-runtime.md`, `docs/project/ideas/idea000034-projects-json-schema-validation.md` |
| Constraint mapping | Backend already exposes `/api/projects` under auth router and frontend already consumes it. | `backend/app.py`, `web/apps/ProjectManager.tsx` |
| Stakeholder impact | Affects @3design/@4plan/@6code implementation path, PM users, and governance maintainers. | `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md`, `.github/agents/0master.agent.md` |
| Risk enumeration | Main risks are false exclusions, stale mapping drift, and UI/backend contract mismatch. | `docs/project/ideas/*.md`, `data/projects.json`, `web/apps/ProjectManager.tsx` |

## Options
### Option A - Backend authoritative exclusion API + frontend consumption (minimal-risk)
Approach:
- Add backend ideas endpoint that parses `docs/project/ideas/*.md`, computes candidate ideas, and excludes ideas mapped to project IDs in active/released lanes.
- Frontend Project Manager consumes the new endpoint (read-only list of unimplemented ideas) and renders alongside existing `/api/projects` board data.
- Implemented default rule: mapped project exists with lane in `{Discovery, Design, In Sprint, Review, Released}`.

Research coverage (6/6 task types):
- Literature review: `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md`
- Alternative enumeration: compare backend-authoritative vs frontend filtering in `backend/app.py` and `web/apps/ProjectManager.tsx`
- Prior-art search: `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`, `docs/project/prj0000052/project-management.think.md`
- Constraint mapping: `docs/project/kanban.md`, `data/projects.json`
- Stakeholder impact: PM users + agent workflow (`.github/agents/1project.agent.md`)
- Risk enumeration: mapped below

Pros:
- Aligns with existing backend-first data pattern in Project Manager.
- Single source of truth for exclusion semantics; reduces frontend duplication.
- Minimal blast radius and clear path for contract tests.

Cons:
- Requires lightweight markdown parsing contract in backend.
- Adds one new API surface to maintain.

Risk-to-testability mapping:
- Failure mode: false exclusion from over-broad lane rule (Likelihood M, Impact H).
	Validation signal: backend unit tests for lane matrix permutations + golden samples from idea files.
- Failure mode: parser misses `Planned project mapping` variants (Likelihood M, Impact M).
	Validation signal: parser fixture tests with representative ideas (`None yet`, single mapping, multi-mapping).
- Failure mode: frontend consumes wrong shape/version (Likelihood L, Impact M).
	Validation signal: API contract test + frontend integration test with mocked endpoint payload.

### Option B - Frontend-only exclusion using existing `/api/projects` + client-side markdown reads
Approach:
- Keep backend unchanged; Project Manager reads idea markdown payloads client-side and filters using `/api/projects` lane data.

Research coverage (4/6 task types):
- Literature review: `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md`
- Alternative enumeration: frontend-only path in `web/apps/ProjectManager.tsx`
- Constraint mapping: existing backend auth/data flow in `backend/app.py`
- Stakeholder impact: frontend ownership + browser loading behavior

Pros:
- No backend API changes.
- Faster first visual prototype.

Cons:
- Higher policy/logic duplication risk in UI.
- Harder to keep exclusion semantics deterministic across consumers.
- Potential Vite/raw import coupling and larger client payload.

Risk-to-testability mapping:
- Failure mode: frontend parsing diverges from future backend expectations (Likelihood H, Impact M).
	Validation signal: component integration tests with snapshot fixtures.
- Failure mode: ideas not available in all runtime deployments (Likelihood M, Impact H).
	Validation signal: e2e load tests in prod-like build (not only dev).
- Failure mode: repeated logic in multiple UI surfaces (Likelihood M, Impact M).
	Validation signal: code review guard + centralized utility tests.

### Option C - Backend materialized registry (`data/ideas.json`) generated from markdown
Approach:
- Add generated artifact pipeline that converts markdown ideas into structured JSON; backend serves JSON and applies exclusion.

Research coverage (5/6 task types):
- Literature review: idea source corpus in `docs/project/ideas/*.md`
- Alternative enumeration: generated-registry path vs direct parse
- Prior-art search: project registry patterns in `data/projects.json` and `docs/project/kanban.md`
- Constraint mapping: governance around canonical files in `.github/agents/1project.agent.md`
- Risk enumeration: build drift and sync lag

Pros:
- Strong runtime performance and stable schema.
- Easier downstream analytics.

Cons:
- Highest process complexity (generation + synchronization + ownership).
- Risk of stale generated file and dual-source confusion.
- Over-scoped for minimal-risk implementation goal.

Risk-to-testability mapping:
- Failure mode: markdown and generated JSON drift (Likelihood M, Impact H).
	Validation signal: deterministic regeneration check in CI.
- Failure mode: merge conflicts in generated artifact (Likelihood M, Impact M).
	Validation signal: pre-commit/CI normalized generation test.
- Failure mode: ownership ambiguity over canonical source (Likelihood M, Impact M).
	Validation signal: documentation contract test + guardrail lint on source-of-truth note.

## Decision Matrix
| Criterion | Option A: backend authoritative API + frontend consume | Option B: frontend-only filtering | Option C: materialized ideas registry |
|---|---|---|---|
| Delivery risk | Low | Medium/High | Medium/High |
| Alignment with existing architecture | High | Medium | Medium |
| Blast radius | Low | Medium | Medium/High |
| Semantic consistency (implemented definition) | High | Medium/Low | High |
| Testability clarity | High | Medium | Medium |
| Time-to-value | High | Medium | Low/Medium |

## Implemented Definition Decision
Candidate definitions:
1. Any mapped project with lane != `Ideas`.
2. Released-only mapped projects.
3. Active-or-released mapped projects (Discovery/Design/In Sprint/Review/Released), exclude Archived.

Recommended default:
- **Definition 3 (Active-or-released, excluding Archived)**.

Rationale:
- Better matches "exclude implemented ideas" in practical PM workflow: once work is active, that idea should no longer appear as an unimplemented backlog candidate.
- Avoids duplicate planning of ideas already in flight.
- Prevents false exclusion for cancelled/stalled work in `Archived`.

Optional mode for future extension:
- Support query mode for stricter interpretation (`implemented_mode=released_only`) without changing default.

## Recommendation
**Choose Option A - Backend authoritative exclusion API + frontend consumption.**

Why this is the minimal-risk choice:
- Uses the established data flow where Project Manager consumes backend APIs (`/api/projects`) rather than deriving governance logic client-side.
- Keeps exclusion policy centralized and testable in one place.
- Delivers required behavior without introducing generated artifact workflows.

Historical prior-art citations (required):
- `docs/project/prj0000052/project-management.think.md`
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`
- `docs/project/kanban.md`
- `data/projects.json`

## Open Questions
- Should the backend expose exclusion details (`excluded_by_project_id`, `excluded_lane`) for UI transparency, or return only visible ideas?
- Should ideas with malformed mapping lines be treated as visible-by-default with warning telemetry?
- For @3design: confirm API shape as additive endpoint vs extending existing `/api/projects` response.

