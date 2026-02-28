# Splice: src/infrastructure/swarm/orchestration/core/distributed/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EngineState
- WorkerState
- LoadBalancingStrategy
- ParallelConfig
- EngineIdentity
- WorkerIdentity

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
