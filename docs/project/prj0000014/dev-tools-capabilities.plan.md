# dev-tools-capabilities — Implementation Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22_

## Task Breakdown

| # | Task | Owner | File(s) |
|---|------|-------|---------|
| 1 | Fix `shell=True` in `remote.py` | @6code | `src/tools/remote.py` |
| 2 | Add `check_expiry()` to `ssl_utils.py` | @6code | `src/tools/ssl_utils.py` |
| 3 | Add `create_feature_branch()` etc. to `git_utils.py` | @6code | `src/tools/git_utils.py` |
| 4 | Write tests for all new APIs | @5test | `tests/tools/test_capabilities_modules.py` |
| 5 | Write 9 doc artifacts | @0master | `docs/project/prj0000014/*.md` |

## Acceptance Criteria
- [x] `remote.py` uses no `shell=True` — `subprocess.run` arg is always a `list`
- [x] `ssl_utils.check_expiry("google.com")` returns a dict with `days_remaining`
- [x] `git_utils.create_feature_branch("my-feat")` creates a branch or returns `False` if checked out
- [x] `pytest tests/tools/test_capabilities_modules.py` passes
- [x] All 9 doc artifacts present in `docs/project/prj0000014/`

## Validation Commands
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/tools/test_capabilities_modules.py -v
```
