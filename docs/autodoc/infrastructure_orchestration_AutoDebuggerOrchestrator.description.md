# Description: `AutoDebuggerOrchestrator.py`

## Module purpose

AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.

## Location
- Path: `infrastructure\orchestration\AutoDebuggerOrchestrator.py`

## Public surface
- Classes: AutoDebuggerOrchestrator
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `__future__`, `logging`, `os`, `sys`, `subprocess`, `typing`, `src.logic.agents.security.ImmuneSystemAgent`, `src.logic.agents.development.CoderAgent`, `src.core.base.utilities`, `pathlib`

## Metadata

- SHA256(source): `891dbc219eb04de8`
- Last updated: `2026-01-11 12:53:47`
- File: `infrastructure\orchestration\AutoDebuggerOrchestrator.py`