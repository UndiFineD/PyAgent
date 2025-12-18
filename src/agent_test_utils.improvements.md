# Improvements: `agent_test_utils.py`

This document tracks realistic, maintenance-oriented improvements for
`src/agent_test_utils.py`. Feature history belongs in
`agent_test_utils.changes.md`.

## Updated in this pass (2025-12-18)

- Documentation accuracy:
  - Companion docs now point at `src/agent_test_utils.py` (not an older
    `scripts/...` path).
  - Description doc reflects the current public surface and current SHA256
    fingerprint.
  - Error report documents current limitations and failure modes.

## Suggested next improvements

### Reduce “mega-module” coupling

- `agent_test_utils.py` contains many unrelated utilities in one file.
  Consider splitting into smaller modules (e.g. `snapshot_utils.py`,
  `fixtures.py`, `mock_backend.py`, `imports.py`) to reduce import time and keep
  dependencies clearer.

### Clarify which APIs are stable

- Add a short “stable vs legacy” section in the module docstring and/or
  `description.md` identifying:
  - recommended modern entrypoints
  - legacy helpers preserved for older tests

### Improve safety of import helpers

- Consider adding an option to prevent `load_agent_module()` from overwriting an
  existing `sys.modules[name]` entry, or to always namespace it.
- For `agent_sys_path()` and `agent_dir_on_path()`, consider a re-entrancy guard
  or clearer naming to avoid accidental global-state leaks in tests.

### Add focused unit tests for the legacy loaders

- Tests should cover:
  - filename normalization for hyphenated module names
  - cleanup of `sys.modules` on import failure
  - `sys.path` restoration on exceptions

## Notes

- File: `src/agent_test_utils.py`
