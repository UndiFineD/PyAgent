# dev-tools-implementation — Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22_

## Tasks

| # | Task | File | Done |
|---|------|------|------|
| 1 | Add Apache copyright header | `src/tools/common.py` | ✅ |
| 2 | Add TOML detection + `load_config` TOML branch | `src/tools/common.py` | ✅ |
| 3 | Add `ensure_dir(path)` | `src/tools/common.py` | ✅ |
| 4 | Add `retry(fn, *, max_attempts, delay, exceptions)` | `src/tools/common.py` | ✅ |
| 5 | Add `format_table(rows, headers)` | `src/tools/common.py` | ✅ |
| 6 | Write test suite | `tests/tools/test_implementation_helpers.py` | ✅ |
| 7 | Write 9 doc artifacts | `docs/project/prj0000015/` | ✅ |

## Acceptance Criteria
- [x] `load_config("x.toml")` returns parsed dict on Python 3.11+; raises `RuntimeError` on older
- [x] `ensure_dir(path)` creates nested dirs and returns `Path`
- [x] `retry` with `delay=0.0` retries exactly N times then raises
- [x] `format_table` renders aligned columns
- [x] All 10 tests pass: `pytest tests/tools/test_implementation_helpers.py`

## Validation Command
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/tools/test_implementation_helpers.py -v
```
