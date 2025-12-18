# Errors: `agent-coder.py`

This file tracks known issues and limitations in `src/agent-coder.py`.

## Known issues

- Temporary file cleanup is silent on failure:
  - `_validate_flake8()` catches `OSError` when deleting the temp file and ignores it.
  - This can hide filesystem/permission problems.

## Limitations / footguns

- Style validation is best-effort:
  - If `flake8` is not installed, style validation is skipped.
  - If `flake8` reports issues, the agent logs a warning but still proceeds.
- Hard-coded `flake8` ignores:
  - `_validate_flake8()` runs `flake8 --ignore=E501,W293` on the temp file, which may not
    match project policy.
- Import path expectations:
  - The module imports `BaseAgent` via `from base_agent import ...`; the runtime must
    have the repo’s `src/` on `sys.path` (or otherwise resolve that import).

## Status

- Last reviewed: 2025-12-18
