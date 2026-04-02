# projectmanager-ideas-autosync - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Selected Option
Option A - Backend-authoritative ideas API consumed by frontend.

Rationale:
- Keeps implemented filtering logic centralized in backend instead of duplicating in UI.
- Matches existing Project Manager data flow (`/api/projects` from backend).
- Minimizes risk by adding one additive endpoint and non-breaking frontend consumption.

## Problem Statement And Goals
Project Manager currently loads only `/api/projects` and has no idea ingestion feed. Idea markdown files in `docs/project/ideas/` contain `Planned project mapping` data, but no API currently converts that into active unimplemented ideas.

Goals:
1. Provide a backend endpoint that returns idea records and excludes implemented ideas by default.
2. Define deterministic mapping from markdown idea files to project IDs in `data/projects.json`.
3. Integrate frontend Project Manager to display active unimplemented ideas alongside the Kanban board.
4. Lock behavior with backend and frontend tests.

## Architecture
### High-Level Flow
1. Backend reads `docs/project/ideas/*.md`.
2. Backend parses idea metadata:
	 - idea ID (from filename and/or H1),
	 - title,
	 - summary,
	 - `Planned project mapping` line.
3. Backend resolves mapped project IDs against `/api/projects` source (`data/projects.json`).
4. Backend computes implemented status using lane semantics and query mode.
5. Frontend `ProjectManager.tsx` loads `/api/projects` and `/api/ideas` and renders active unimplemented ideas panel/list.

### Implemented Semantics (Default)
Implemented by default when any mapped project is in one of:
- `Discovery`
- `Design`
- `In Sprint`
- `Review`
- `Released`

Not implemented by default when:
- no mappings (`Planned project mapping: None yet`),
- mapped projects are missing in projects registry,
- mapped projects are only in `Ideas` or `Archived`.

## Interfaces & Contracts
### IFC-01 Ideas List Endpoint Contract
Path:
- `GET /api/ideas`

Query parameters:
- `implemented`: `exclude` (default), `include`, `only`
- `implemented_mode`: `active_or_released` (default), `released_only`
- `q`: optional case-insensitive substring filter over idea id/title/summary
- `sort`: `priority` (default), `idea_id`, `updated`
- `order`: `asc` or `desc` (default `desc`)

Implemented behavior:
- `implemented=exclude`: return only unimplemented ideas.
- `implemented=include`: return both implemented and unimplemented ideas.
- `implemented=only`: return only implemented ideas.

`implemented_mode` behavior:
- `active_or_released`: implemented lanes are `Discovery|Design|In Sprint|Review|Released`.
- `released_only`: implemented lane is only `Released`.

Sorting behavior:
- Primary key by selected `sort`.
- Stable tie-breaker always `idea_id` ascending.
- If field missing for selected sort, fallback comparator value is empty/lowest and tie-breaker applies.

Response schema (list item):
- `idea_id: str` (example `idea000005`)
- `title: str`
- `summary: str`
- `priority: str | null` (parsed from summary text like `priority P2`, else null)
- `impact: str | null` (parsed from summary text, else null)
- `urgency: str | null` (parsed from summary text, else null)
- `source_path: str` (workspace-relative path)
- `mapped_project_ids: list[str]`
- `implemented_project_ids: list[str]`
- `implemented: bool`

Error behavior:
- Never fail entire list due to one malformed idea file.
- Malformed file is skipped with warning log entry and processing continues.

### IFC-02 Idea-to-Project Mapping Strategy
Input source:
- Idea markdown files under `docs/project/ideas/*.md`.

Mapping extraction:
1. Read line starting with `Planned project mapping:`.
2. If value is `None yet` (case-insensitive), mapping list is empty.
3. Otherwise, extract all tokens matching project ID regex `prj\d{7}`.
4. Preserve unique IDs in first-seen order.

Project resolution:
1. Lookup mapped IDs in validated `ProjectModel` list from `data/projects.json`.
2. Ignore unknown IDs for implemented calculation but keep them in `mapped_project_ids` for transparency.
3. Compute `implemented_project_ids` using chosen `implemented_mode` lane set.

Determinism rules:
- Matching is case-insensitive on lane labels after normalization.
- Duplicate IDs in mapping line collapse to one.
- Missing mapping line behaves like empty mapping list.

### IFC-03 Frontend Integration Contract (`ProjectManager.tsx`)
Data loading:
- Continue loading projects from `GET /api/projects`.
- Add second fetch to `GET /api/ideas?implemented=exclude&implemented_mode=active_or_released&sort=priority&order=desc`.

State additions:
- `ideas: IdeaCard[]`
- `ideasLoading: boolean`
- `ideasError: string | null`
- optional local `ideasQuery` for client-side quick filter on visible ideas.

UI behavior:
- Add "Active Ideas" panel in Project Manager shell (above lanes or right-side rail, desktop; stacked on mobile width).
- Each row shows `idea_id`, title, summary snippet, and mapped project chips.
- Empty state when no active ideas: "No active unimplemented ideas".
- Failure of ideas fetch must not block Kanban project rendering.

Interaction behavior:
- Clicking source badge opens corresponding markdown file URL in repository path.
- No edit operations for ideas in this phase (read-only view).

### IFC-04 Test Contracts
Backend tests:
- parser and mapping unit tests for:
	- `None yet`,
	- single mapping,
	- multi mapping,
	- duplicate IDs,
	- malformed mapping line.
- endpoint tests for `implemented` and `implemented_mode` matrix.
- sorting tests for `priority`, `idea_id`, and deterministic tie-break.
- resiliency test: malformed idea file does not break whole response.

Frontend tests:
- ProjectManager integration test verifies:
	- projects still render when ideas API fails,
	- active ideas list renders unimplemented ideas from mocked payload,
	- empty state renders on zero ideas,
	- query/filter text narrows visible ideas if implemented.

## Acceptance Criteria
| AC ID | Requirement | Verification | Owner Phase |
|---|---|---|---|
| AC-01 | `GET /api/ideas` exists with documented query params and schema | Backend route + response model tests | @5test/@6code |
| AC-02 | Default implemented semantics exclude ideas mapped to active/released projects | Endpoint matrix tests against lane fixtures | @5test |
| AC-03 | `implemented_mode=released_only` returns different set from default where applicable | Endpoint mode comparison test | @5test |
| AC-04 | Idea mapping extraction is deterministic for `None yet`, duplicates, malformed lines | Parser unit tests | @5test |
| AC-05 | Project Manager displays unimplemented ideas from backend in read-only panel | Frontend integration test with mocked API | @5test/@6code |
| AC-06 | Ideas API failure does not block projects board render | Frontend integration test for partial failure | @5test |
| AC-07 | Sort behavior is deterministic with stable tie-break by `idea_id` | Backend sorting tests | @5test |
| AC-08 | Interface-to-task traceability is complete for all contracts | Design review before @4plan handoff | @3design/@4plan |

## Interface-To-Task Traceability (For @4plan Seeding)
| Interface/Contract | Task Seed ID | Planned Task Description |
|---|---|---|
| IFC-01 Ideas List Endpoint Contract | TSK-01 | Add backend `GET /api/ideas` route, query validation, response model |
| IFC-02 Idea-to-Project Mapping Strategy | TSK-02 | Implement markdown mapping parser + implemented resolver against project lanes |
| IFC-01 sorting/filter semantics | TSK-03 | Implement endpoint filtering (`implemented`, `implemented_mode`, `q`) and sorting (`sort`, `order`) |
| IFC-03 Frontend Integration Contract | TSK-04 | Add ideas fetch/state/UI panel to `ProjectManager.tsx` with non-blocking failure handling |
| IFC-04 Backend test contract | TSK-05 | Add backend parser/endpoint tests for mode matrix, sorting, malformed input behavior |
| IFC-04 Frontend test contract | TSK-06 | Add frontend integration tests for ideas render, empty state, and ideas API failure isolation |

## Non-Functional Requirements
- Performance: parse-and-filter should complete under 250ms for current idea corpus; route remains read-only and cacheable in-process per request cycle.
- Security: route remains behind existing `require_auth` auth router; no filesystem paths accepted from user input; only fixed `docs/project/ideas` directory scanned.
- Testability: parser pure-function boundaries and endpoint query matrix are deterministic and unit-testable.

## ADR Recording
No new cross-cutting architecture decision requiring a new ADR in `docs/architecture/adr/`.
This design is an additive endpoint and UI integration within established backend-authoritative API pattern.

## Open Questions
1. Should backend include optional debug metadata (`excluded_by_lane`, `excluded_by_project`) in v1 response, or keep lean payload and add later?
2. Should priority parsing be strict enum (`P1..P4`) or permissive nullable string in first iteration?

## Handoff
Design is actionable and ready for @4plan.
Target implementation scope is approximately 8-12 code file touches and 8-12 test file touches.
