# rust-file-watcher — Test Plan

_Owner: @5test_

## Tests in `tests/test_file_watcher.py`

| # | Name | Description |
|---|------|-------------|
| 1 | `test_filewatcher_scan_uses_rust_when_available` | Patches `src.tools.FileWatcher._HAS_RUST=True` + `rust_core.scan_changed_files` to return JSON; calls `_poll` directly; asserts changed files appear in pending |
| 2 | `test_filewatcher_scan_falls_back_to_python` | Patches `_HAS_RUST=False`; uses temp dir with a modified file; verifies fallback `_python_scan` returns its path |
| 3 | `test_get_changes_returns_and_clears` | Adds items to `_pending`; `get_changes()` returns them; second call returns `[]` |
| 4 | `test_invalid_root_raises_on_scan` | Passes nonexistent root to `_python_scan`; verifies returns `[]` (os.walk on nonexistent is empty, no crash) |
| 5 | `test_start_stop_lifecycle` | Starts watcher, asserts `_task` not None, stops it, asserts task cancelled |

## TDD NOTE
Tests are written first; impl fills them.
