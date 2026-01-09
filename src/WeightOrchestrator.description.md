# Description: `WeightOrchestrator.py`

## Module purpose

WeightOrchestrator for PyAgent.
Manages the lifecycle of neural weights (LoRA/QLoRA adapters) across the fleet.
Coordinates between the ModelForgeAgent and individual agents to hot-swap capabilities.

## Location
- Path: `src\classes\orchestration\WeightOrchestrator.py`

## Public surface
- Classes: WeightOrchestrator
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `logging`, `json`, `pathlib`, `typing`, `src.classes.base_agent`, `src.classes.base_agent.utilities`

## Metadata

- SHA256(source): `aac22c3c0c5b92a8`
- Last updated: `2026-01-08 22:53:32`
- File: `src\classes\orchestration\WeightOrchestrator.py`