# Description: `MetaOrchestratorAgent.py`

## Module purpose

High-level goal manager and recursive orchestrator.
Manages complex objectives by breaking them down into sub-goals and delegating to specialized agents.

## Location
- Path: `infrastructure\orchestration\MetaOrchestratorAgent.py`

## Public surface
- Classes: MetaOrchestratorAgent
- Functions: (none)

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `__future__`, `logging`, `json`, `pathlib`, `typing`, `src.core.base.BaseAgent`, `src.infrastructure.fleet.FleetManager`, `src.infrastructure.orchestration.ToolRegistry`, `src.logic.agents.cognitive.context.engines.GlobalContextEngine`

## Metadata

- SHA256(source): `e09b8acf41898d02`
- Last updated: `2026-01-11 12:53:53`
- File: `infrastructure\orchestration\MetaOrchestratorAgent.py`