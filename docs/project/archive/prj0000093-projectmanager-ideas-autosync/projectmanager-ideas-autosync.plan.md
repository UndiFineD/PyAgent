# projectmanager-ideas-autosync - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-28_

## Overview
Implement backend-authoritative idea ingestion for Project Manager with deterministic mapping from `docs/project/ideas/*.md`, expose `GET /api/ideas` with implemented/filter/sort semantics, integrate an Active Ideas panel in frontend Project Manager, and lock behavior with TDD-first backend/frontend tests.

## Chunking
- Chunk 001 (single chunk): 3-5 code files and 3-5 test files; one runnable increment covering API contract, parsing/mapping behavior, and frontend rendering/failure isolation.

## Task List
- [ ] T1 - Create backend idea parsing helpers for deterministic extraction.
	Objective: add pure helper functions to parse planned mapping IDs, summary fields (priority/impact/urgency), and stable idea metadata from markdown files.
	Files: `backend/app.py` (or extracted helper module under `backend/` if @6code splits logic), `docs/project/ideas/*.md` fixtures consumed by tests.
	Acceptance: `None yet`, duplicate project IDs, missing mapping line, and malformed mapping lines are handled per IFC-02 without raising endpoint-fatal exceptions.
	Validation command: `python -m pytest -q tests/test_api_ideas.py`

- [ ] T2 - Add implemented resolution logic against project lanes and mode semantics.
	Objective: compute `implemented` and `implemented_project_ids` from mapped IDs and `data/projects.json` lane values for `active_or_released` and `released_only` modes.
	Files: `backend/app.py`, `data/projects.json` (read-only fixture input in tests).
	Acceptance: implemented lane set is exact for each mode; unknown mapped IDs remain visible in `mapped_project_ids` but do not crash or produce false positives.
	Validation command: `python -m pytest -q tests/test_api_ideas.py -k "implemented_mode or lane"`

- [ ] T3 - Implement `GET /api/ideas` endpoint contract with filtering and sorting.
	Objective: expose `/api/ideas` on authenticated router with query params `implemented`, `implemented_mode`, `q`, `sort`, `order`; apply stable tie-break by `idea_id`.
	Files: `backend/app.py`, `tests/test_api_versioning.py` (versioned routing assertion extension).
	Acceptance: response schema matches IFC-01; malformed idea file skips with warning; `/api/v1/ideas` routes correctly via shared router prefix behavior.
	Validation command: `python -m pytest -q tests/test_api_ideas.py tests/test_api_versioning.py -k "ideas"`

- [ ] T4 - Add backend TDD coverage for parser, mapping, endpoint matrix, and sort determinism.
	Objective: add focused tests that fail before implementation and pass after implementation for endpoint behavior matrix and deterministic ordering.
	Files: `tests/test_api_ideas.py` (new), optional shared fixture file under `tests/fixtures/` if needed.
	Acceptance: tests cover parser edge cases, `implemented` (`exclude/include/only`), `implemented_mode`, `q` filtering, sort/order combinations, and malformed-file resilience.
	Validation command: `python -m pytest -q tests/test_api_ideas.py`

- [ ] T5 - Integrate Active Ideas panel in Project Manager frontend with non-blocking failure behavior.
	Objective: fetch `/api/ideas?implemented=exclude&implemented_mode=active_or_released&sort=priority&order=desc` and render ideas list, empty state, and safe fallback on ideas fetch error.
	Files: `web/apps/ProjectManager.tsx`.
	Acceptance: project board remains usable when ideas fetch fails; ideas panel renders expected fields (`idea_id`, title, summary snippet, mapped project chips).
	Validation command: `npm --prefix web test -- apps/ProjectManager.test.tsx`

- [ ] T6 - Add frontend integration tests for ideas rendering, filtering, empty, and failure isolation.
	Objective: extend Project Manager tests to mock dual API fetch flow and verify UI contracts for ideas panel behavior.
	Files: `web/apps/ProjectManager.test.tsx`.
	Acceptance: tests assert (1) ideas render from payload, (2) empty-state text appears when zero ideas, (3) ideas API failure does not block project rendering, (4) any local quick-filter narrows visible ideas.
	Validation command: `npm --prefix web test -- apps/ProjectManager.test.tsx`

- [ ] T7 - Update project docs and milestone state after implementation/test contract alignment.
	Objective: reflect @4plan completion and @5test handoff readiness in canonical project artifacts.
	Files: `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md`, `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.plan.md`, `.github/agents/data/4plan.memory.md`.
	Acceptance: M3 is DONE, project status indicates READY_FOR_5TEST, and plan contains actionable tasks with explicit validation commands.
	Validation command: `python -m pytest -q tests/test_enforce_branch.py`

## Dependency Order
1. T1 -> T2 -> T3 (backend contract path)
2. T4 starts first as TDD gate; @6code implementation for T1-T3 must satisfy failing tests from T4.
3. T5 -> T6 (frontend integration after endpoint contract is fixed/mocked)
4. T7 finalizes artifacts and handoff metadata.

## TDD Handoff Contract For @5test
- Write failing tests for T4 before implementation starts in @6code.
- Write failing tests for T6 before frontend integration implementation starts in @6code.
- Maintain deterministic fixtures for idea markdown corpus and lane matrix assertions.
- Keep backend contract assertions aligned with AC-01 through AC-07 from design doc.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M3.1 | Backend parser + mapping planned | T1-T2 | DONE |
| M3.2 | Backend endpoint contract planned | T3-T4 | DONE |
| M3.3 | Frontend panel + tests planned | T5-T6 | DONE |
| M3.4 | Docs/handoff updated | T7 | DONE |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/test_api_ideas.py
python -m pytest -q tests/test_api_ideas.py tests/test_api_versioning.py
python -m pytest -q tests/test_enforce_branch.py
npm --prefix web test -- apps/ProjectManager.test.tsx
```

## Handoff
Next agent: `@5test`
Handoff readiness: `READY_FOR_5TEST`
