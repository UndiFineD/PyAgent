# Description: `agent-errors.py`

## Module purpose

Improves and maintains `*.errors.md` “error report” files.

In addition to delegating to the LLM (via `BaseAgent`), this module includes a
large set of supporting enums, dataclasses, and helper classes for organizing
and analyzing errors (severity/category, clustering, patterns, suppression,
annotations, statistics, and export).

## Location

- Path: `src/agent-errors.py`

## Public surface (high level)

- CLI:

  - `main` (created via `create_main_function(...)`)

- Primary class:

  - `ErrorsAgent(BaseAgent)`

- Key types (selected):

  - Enums: `ErrorSeverity`, `ErrorCategory`, `NotificationChannel`, `ExternalReporter`, `TrendDirection`
  - Dataclasses: `ErrorEntry`, `ErrorCluster`, `ErrorPattern`, `SuppressionRule`, `NotificationConfig`

## Behavior summary

- Input is typically `something.errors.md`.
- Emits a warning if the file name does not end with `.errors.md`.
- Best-effort checks for an associated code file with the same stem next to the

  errors file (exact match or common extensions like `.py`, `.sh`, `.js`, `.ts`, `.md`).
- `improve_content()` delegates to `BaseAgent.improve_content()`; fallback behavior

  when Copilot is unavailable is handled in `BaseAgent`.

## How to run

```bash
python src/agent-errors.py path/to/file.errors.md
```

## Key dependencies

- `base_agent.BaseAgent`
- `base_agent.create_main_function`

## File fingerprint

- SHA256(source): `f22ef91c3b7b356dc621d7b389f7ae53c017de966e1d1c56fc77178f18dd0dc7`
