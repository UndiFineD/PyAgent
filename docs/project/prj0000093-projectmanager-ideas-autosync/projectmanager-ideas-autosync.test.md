# projectmanager-ideas-autosync - Test Artifacts

_Status: DONE (READY_FOR_6CODE)_
_Tester: @5test | Updated: 2026-03-28_

## Test Plan
Scope: backend RED tests for `/api/ideas` only (minimum viable scope for M4).

Approach:
- Write behavior-first endpoint tests that exercise real repository corpus under `docs/project/ideas`.
- Derive expected filtering sets from `data/projects.json` lanes and idea mappings.
- Validate deterministic sort contract (`rank` then `idea_id`).
- Validate malformed idea file resilience by injecting an unreadable markdown file and asserting endpoint continuity.

Frameworks/Tools:
- `pytest`
- `fastapi.testclient`
- `ruff` lint/docstring gates

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-001 | `/api/ideas` returns ideas loaded from `docs/project/ideas` with `implemented=include` | `tests/test_api_ideas.py` | RED |
| TC-002 | `implemented=exclude&implemented_mode=active_or_released` excludes ideas mapped to active/released lanes | `tests/test_api_ideas.py` | RED |
| TC-003 | `implemented_mode=released_only` excludes only `Released` lane mappings | `tests/test_api_ideas.py` | RED |
| TC-004 | Stable ordering contract: sort by rank then tie-break by `idea_id` | `tests/test_api_ideas.py` | RED |
| TC-005 | Malformed idea markdown file does not crash endpoint | `tests/test_api_ideas.py` | RED |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case ID(s) |
|---|---|---|
| AC-01 | `GET /api/ideas` exists and returns list contract | TC-001 |
| AC-02 | Default implemented semantics exclude active/released-mapped ideas | TC-002 |
| AC-03 | `implemented_mode=released_only` behavior differs appropriately | TC-003 |
| AC-07 | Deterministic sorting with stable tie-break by idea ID | TC-004 |
| AC-01 (error behavior) | Malformed idea file does not fail entire endpoint | TC-005 |

## Validation Results
| ID | Result | Output |
|---|---|---|
| LINT-001 | PASS | `ruff check --fix tests/test_api_ideas.py` -> 6 fixed, 0 remaining |
| LINT-002 | PASS | `ruff check tests/test_api_ideas.py` |
| LINT-003 | PASS | `ruff check --select D tests/test_api_ideas.py` |
| TC-001..TC-005 | RED (expected) | `python -m pytest -q tests/test_api_ideas.py --tb=short` -> 5 failed, all on `assert response.status_code == 200` with actual `404 Not Found` |

## Weak-Test Detection Gate
- Placeholder/stub checks: PASS (tests assert concrete response status and behavior-specific payload contracts; no `assert True`, no existence-only assertions).
- Import/collection failure gate: PASS (suite collected and executed all 5 tests; failures are assertion-level, not import/attribute errors).
- Behavior specificity gate: PASS (each test maps to a distinct endpoint behavior contract).

## Unresolved Failures
- `/api/ideas` endpoint is not implemented yet in `backend/app.py`, producing HTTP 404 for all five RED tests.

## Handoff
- Next agent: `@6code`
- Handoff status: `READY_FOR_6CODE`
- Required implementation scope:
	- Add `GET /api/ideas` on authenticated router.
	- Implement corpus ingestion from `docs/project/ideas`.
	- Implement `implemented` + `implemented_mode` filtering semantics.
	- Implement stable `rank` sort with `idea_id` tie-break.
	- Skip malformed idea files without crashing endpoint.
