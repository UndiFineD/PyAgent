# Description: `AutoDebuggerOrchestrator.py`

## Module purpose

AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.

## Location
- Path: `src\classes\orchestration\AutoDebuggerOrchestrator.py`

## Public surface
- Classes: AutoDebuggerOrchestrator
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `logging`, `os`, `sys`, `subprocess`, `typing`, `src.classes.specialized.ImmuneSystemAgent`, `src.classes.coder.CoderAgent`, `src.classes.base_agent.utilities`, `pathlib`

## Metadata

- SHA256(source): `188d4f7e695e1415`
- Last updated: `2026-01-08 22:53:23`
- File: `src\classes\orchestration\AutoDebuggerOrchestrator.py`