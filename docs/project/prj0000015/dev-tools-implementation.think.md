# dev-tools-implementation — Think Notes

_Status: COMPLETE_
_Analyst: @2think | Updated: 2026-03-22_

## Problem Statement
`common.py` had 2 functions: `load_config` (JSON only) and `get_logger`. Every tool that needed TOML config, directory creation, retry logic, or table formatting duplicated this code inline.

## Alternatives Considered

### Option A — Single `common.py` with stdlib only (CHOSEN)
Pro: no new dependencies, ships with Python 3.11+; `tomllib` fallback to `tomli` only needed on 3.10-.
Con: `retry` is basic compared to `tenacity`.

### Option B — Add `tenacity` for retry, `tabulate` for tables
Pro: richer API.
Con: adds 2 transitive dependencies to a zero-dep tools module.

### Option C — Separate `config.py`, `io_utils.py`, `fmt_utils.py`
Pro: concerns separated.
Con: many small imports for callers; overhead not justified with 4 functions.

## Decision
**Option A.** Keep `common.py` as the single shared utility file; add `tomllib`/`tomli` detection pattern so older Python still gets a clear error instead of a cryptic import failure.
