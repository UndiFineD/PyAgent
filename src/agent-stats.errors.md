# Errors: `agent-stats.py`

This file documents realistic failure modes and limitations of
`src/agent-stats.py`.

## Input validation and file handling

- Missing file paths:
  - `StatsAgent` logs a warning for missing input paths and filters them out.
  - If all inputs are invalid, it raises `ValueError`.
- Companion-file discovery is directory-local:
  - For each input file, it only checks for companions next to that file using
    the same `stem`. It does not search other directories.

## Optional dependencies

- `matplotlib`:
  - If missing, `visualize_stats()` logs a warning and does nothing.
  - The CLI still runs and prints the textual/JSON/CSV summary.

## Data format expectations

- `--coverage`:
  - Expects JSON and looks for `total_coverage`. Malformed JSON or an unexpected
    shape will raise an exception during `json.load()`.
- `--baseline`:
  - Expects JSON stats (a dict of counts). Malformed JSON will raise.

## Export and I/O errors

- `--export` writes files in the current working directory (e.g.
  `stats_output.json`). Permission issues or invalid paths will raise.
- SQLite export imports `sqlite3` and writes `stats_output.db`; database errors
  can surface as exceptions.

## Exception handling

- The CLI catches `ValueError` from validation and exits with code 1.
- Other exceptions (I/O failures, JSON decode errors, sqlite errors) are not
  explicitly caught and will bubble up.
