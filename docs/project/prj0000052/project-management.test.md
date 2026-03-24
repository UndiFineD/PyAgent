# project-management — Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-24_

## Test Plan

**Scope**: Structural validation of prj0000052 deliverables T1 and T2.
**Framework**: pytest 9.0.2, Python 3.13.12
**File**: `tests/structure/test_kanban.py`
**Pattern**: Module-level file loading with `_FILE_MISSING` sentinels (same as `test_readme.py`).
Content-dependent tests skip until files exist with the correct marker.
Only the two existence tests (`test_projects_json_exists`, `test_kanban_exists`) are hard-fail red gates.

**Validation command**:
```
python -m pytest tests/structure/test_kanban.py -v --tb=short
```

Expected baseline (pre-@6code): 2 FAILED, 18 SKIPPED, 0 PASSED (20 items collected)
Expected after @6code: 20 PASSED, 0 FAILED, 0 SKIPPED

## Test Cases

| ID  | Description                                            | File                              | Status |
|-----|--------------------------------------------------------|-----------------------------------|--------|
| TC1 | `test_projects_json_exists` — file exists at expected path | tests/structure/test_kanban.py | RED    |
| TC2 | `test_projects_json_valid` — parses as valid JSON array | tests/structure/test_kanban.py   | SKIP   |
| TC3 | `test_projects_json_entry_count` — exactly 62 entries  | tests/structure/test_kanban.py    | SKIP   |
| TC4 | `test_projects_json_required_fields` — all 11 required keys on every entry | tests/structure/test_kanban.py | SKIP |
| TC5 | `test_projects_json_lane_values` — all lane values in VALID_LANES | tests/structure/test_kanban.py | SKIP |
| TC6 | `test_projects_json_priority_values` — all priority values in {P1–P4} | tests/structure/test_kanban.py | SKIP |
| TC7 | `test_projects_json_budget_tier_values` — all budget_tier in {XS,S,M,L,XL,unknown} | tests/structure/test_kanban.py | SKIP |
| TC8 | `test_projects_json_prj0000052_present` — entry with id=="prj0000052" present | tests/structure/test_kanban.py | SKIP |
| TC9 | `test_kanban_exists` — file exists, first line is `# PyAgent Project Kanban Board` | tests/structure/test_kanban.py | RED |
| TC10 | `test_kanban_required_h2s[## Ideas]` — H2 present | tests/structure/test_kanban.py   | SKIP   |
| TC11 | `test_kanban_required_h2s[## Discovery]` — H2 present | tests/structure/test_kanban.py  | SKIP   |
| TC12 | `test_kanban_required_h2s[## Design]` — H2 present | tests/structure/test_kanban.py    | SKIP   |
| TC13 | `test_kanban_required_h2s[## In Sprint]` — H2 present | tests/structure/test_kanban.py  | SKIP   |
| TC14 | `test_kanban_required_h2s[## Review]` — H2 present | tests/structure/test_kanban.py    | SKIP   |
| TC15 | `test_kanban_required_h2s[## Released]` — H2 present | tests/structure/test_kanban.py   | SKIP   |
| TC16 | `test_kanban_required_h2s[## Archived]` — H2 present | tests/structure/test_kanban.py   | SKIP   |
| TC17 | `test_kanban_required_h2s[## Summary Metrics]` — H2 present | tests/structure/test_kanban.py | SKIP |
| TC18 | `test_kanban_total_rows` — exactly 62 rows matching `^\|\s*prj\d{7}` | tests/structure/test_kanban.py | SKIP |
| TC19 | `test_kanban_prj0000052_present` — "prj0000052" in file content | tests/structure/test_kanban.py | SKIP |
| TC20 | `test_kanban_no_todo_fixme` — no TODO/FIXME/TBD in file | tests/structure/test_kanban.py | SKIP |

## Validation Results (Baseline — pre-@6code)

| ID   | Result  | Output                                                                         |
|------|---------|--------------------------------------------------------------------------------|
| TC1  | FAILED  | `AssertionError: data/projects.json not found at …/data/projects.json`        |
| TC2  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC3  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC4  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC5  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC6  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC7  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC8  | SKIPPED | `data/projects.json not yet created (awaiting @6code)`                         |
| TC9  | FAILED  | `AssertionError: docs/project/kanban.md not found at …/kanban.md`             |
| TC10–TC17 | SKIPPED | `docs/project/kanban.md not yet created (awaiting @6code)`              |
| TC18 | SKIPPED | `docs/project/kanban.md not yet created (awaiting @6code)`                     |
| TC19 | SKIPPED | `docs/project/kanban.md not yet created (awaiting @6code)`                     |
| TC20 | SKIPPED | `docs/project/kanban.md not yet created (awaiting @6code)`                     |

**Baseline run result**: `2 failed, 18 skipped in 2.79s`

## Unresolved Failures

TC1 and TC9 are the intended TDD red gates. Both fail because the target files do not exist yet.
Failure reason is an `AssertionError` (file not found), **not** `ImportError` or `AttributeError`.
This confirms correct red-phase behavior. Hand off to @6code to implement T1 and T2.
