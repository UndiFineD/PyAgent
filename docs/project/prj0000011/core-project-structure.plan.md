# core-project-structure — Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22_

## Implementation Tasks

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Write `scripts/setup_structure.py` | @6code | DONE |
| 2 | Write `tests/structure/test_project_structure.py` | @5test | DONE |
| 3 | Add `conftest.py` root fixture ensuring sys.path coverage | @6code | DONE |
| 4 | Document directory layout in `docs/architecture/` | @6code | DONE |
| 5 | Wire smoke-test CI workflow to run structure tests | @7exec | DONE |

## Acceptance Criteria
- `python scripts/setup_structure.py` exits 0 on a fresh checkout.
- `pytest tests/structure/` passes with 0 failures.
- Re-running `setup_structure.py` on an existing layout exits 0 (idempotent).
- CI smoke workflow includes structure test stage.

## Validation Commands
```powershell
python scripts/setup_structure.py
pytest tests/structure/ -v
```
