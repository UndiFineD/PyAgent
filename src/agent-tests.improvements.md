# Improvements: `agent-tests.py`

## Documentation notes

This module is very large and mixes the `TestsAgent` CLI with many supporting types and utilities.
Some helper classes near the end are lightweight compatibility implementations (e.g., `TestRecorder`, `DataFactory`) intended to satisfy the unit-test surface; they may not be production-ready.

## Suggested improvements

- Split the module into smaller units (e.g., `tests_agent.py`, `models.py`, `scheduling.py`) to reduce maintenance risk.
- Remove or update the legacy source-file lookup under `scripts/agent/` (prefer `src/` layout, or make the lookup configurable).
- Replace stubbed helper implementations with real behavior or clearly mark them as placeholders in public docs.
- Add focused unit tests for:

  - `_find_source_file()` lookup precedence and expected mappings.
  - `improve_content()` revert-on-syntax-failure behavior.
  - `_validate_test_structure()` warnings for missing assertions.

- Consider adding an optional “dry-run” mode that shows a diff without writing changes.
- Consider exposing configuration knobs (flakiness threshold, parallelism) via CLI flags if they are intended to be user-controlled.
