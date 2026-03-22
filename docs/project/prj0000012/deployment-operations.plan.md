# deployment-operations — Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22_

## Implementation Tasks

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Write `scripts/setup_deployment.py` | @6code | DONE |
| 2 | Write `tests/structure/test_deployment_dirs.py` | @5test | DONE |
| 3 | Write `.github/workflows/ci.yml` | @6code | DONE |
| 4 | Write `tests/ci/` workflow validation tests | @5test | DONE |
| 5 | Wire smoke CI to run setup and structure tests | @7exec | DONE |

## Acceptance Criteria
- `python scripts/setup_deployment.py` exits 0.
- `pytest tests/structure/test_deployment_dirs.py` passes.
- `pytest tests/ci/` passes.
- CI workflow YAML is valid and GitHub Actions triggers correctly.
- Re-running setup script is idempotent (exits 0 on existing structure).

## Validation Commands
```powershell
python scripts/setup_deployment.py
pytest tests/structure/test_deployment_dirs.py -v
pytest tests/ci/ -v
```
