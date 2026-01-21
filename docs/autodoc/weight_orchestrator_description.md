# Description: `WeightOrchestrator.py`

## Module purpose

WeightOrchestrator for PyAgent.
Manages the lifecycle of neural weights (LoRA/QLoRA adapters) across the fleet.
Coordinates between the ModelForgeAgent and individual agents to hot-swap capabilities.

## Location
- Path: `src\infrastructure\orchestration\WeightOrchestrator.py`

## Public surface
- Classes: WeightOrchestrator
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `__future__`, `logging`, `json`, `pathlib`, `typing`, `src.core.base.BaseAgent`, `src.core.base.utilities`

## Metadata

- SHA256(source): `029dc74f05341b56`
- Last updated: `2026-01-11 10:15:51`
- File: `src\infrastructure\orchestration\WeightOrchestrator.py`