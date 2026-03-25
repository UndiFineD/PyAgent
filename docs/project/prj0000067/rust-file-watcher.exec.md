# rust-file-watcher — Exec Log

_Owner: @7exec_

## Commands run

```
pytest tests/test_file_watcher.py -v
```

## Expected output

```
tests/test_file_watcher.py::test_filewatcher_scan_uses_rust_when_available PASSED
tests/test_file_watcher.py::test_filewatcher_scan_falls_back_to_python PASSED
tests/test_file_watcher.py::test_get_changes_returns_and_clears PASSED
tests/test_file_watcher.py::test_invalid_root_raises_on_scan PASSED
tests/test_file_watcher.py::test_start_stop_lifecycle PASSED
5 passed
```
