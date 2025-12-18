# Description: `agent-improvements.py`

## Module purpose

Improves and maintains `*.improvements.md` “improvement suggestion” files.

In addition to delegating to the LLM (via `BaseAgent`), this module includes a
large set of supporting enums, dataclasses, and helper classes for organizing
and managing improvement work (priorities/categories/status, templates, impact
scoring, dependencies, scheduling, validation, rollback tracking, SLA
management, merge detection, archiving, and branch comparison).

## Location

- Path: `src/agent-improvements.py`

## Public surface (high level)

- CLI:

  - `main` (created via `create_main_function(...)`)

- Primary class:

  - `ImprovementsAgent(BaseAgent)`

## Behavior summary

- Input is typically `something.improvements.md`.
- Emits a warning if the file name does not end with `.improvements.md`.
- Best-effort checks for an associated code file with the same stem next to the

  improvements file (exact match or common extensions like `.py`, `.sh`, `.js`,
  `.ts`, `.md`).
- `improve_content()` augments the prompt to encourage actionable markdown

  checkbox items and grouping by priority before delegating to
  `BaseAgent.improve_content()`.

## How to run

```bash
python src/agent-improvements.py path/to/file.improvements.md
```

## Key dependencies

- `base_agent.BaseAgent`
- `base_agent.create_main_function`

## File fingerprint

- SHA256(source): `2120b52c2f6fa66279340952c3f00ba6a246bf2c82e4a3097bc8998efb5673a3`
