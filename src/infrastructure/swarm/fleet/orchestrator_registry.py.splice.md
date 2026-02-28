# Splice: src/infrastructure/swarm/fleet/orchestrator_registry.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LazyOrchestratorMap
- OrchestratorRegistry

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
