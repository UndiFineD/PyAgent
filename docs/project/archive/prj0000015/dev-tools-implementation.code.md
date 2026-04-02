# dev-tools-implementation — Code Notes

_Status: COMPLETE_
_Coder: @6code | Updated: 2026-03-22_

## Changes Delivered

### `src/tools/common.py` (full rewrite)
- Added Apache copyright header.
- `load_config`: now dispatches on `.toml` extension; uses `tomllib` (stdlib 3.11+) or `tomli` fallback; graceful `RuntimeError` when neither is available.
- `get_logger`: added `level` parameter (default `WARNING`).
- NEW `ensure_dir(path)`: `Path.mkdir(parents=True, exist_ok=True)` wrapper; returns `Path`.
- NEW `retry(fn, *, max_attempts, delay, exceptions)`: loops up to `max_attempts`, sleeps `delay` between tries, re-raises last exception.
- NEW `format_table(rows, headers)`: computes column widths, renders header + separator + body; strips trailing whitespace per row.

### `tests/tools/test_implementation_helpers.py` (new file)
- 10 unit tests, zero external dependencies.

## Backward Compatibility
- `load_config(path)` still works for JSON — signature unchanged.
- `get_logger(name)` still works — `level` has a default.
