# dev-tools-autonomy — Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22_

## Implementation Tasks

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Write `src/tools/dependency_audit.py` | @6code | DONE |
| 2 | Write `src/tools/metrics.py` | @6code | DONE |
| 3 | Write `src/tools/self_heal.py` | @6code | DONE |
| 4 | Write `src/tools/plugin_loader.py` | @6code | DONE |
| 5 | Write `tests/tools/test_dependency_audit.py` | @5test | DONE |
| 6 | Write `tests/tools/test_metrics.py` | @5test | DONE |
| 7 | Write `tests/tools/test_self_heal.py` | @5test | DONE |
| 8 | Extend `scripts/setup_structure.py` for new dirs | @6code | DONE |

## Acceptance Criteria
- `pytest tests/tools/` passes with no failures.
- All four modules importable without network access.
- `plugin_loader.load_plugin` raises `ValueError` for unlisted plugin names.
- Metrics analysis returns correct counts for a known fixture file.

## Validation Commands
```powershell
pytest tests/tools/ -v
```
