# Splice: src/infrastructure/swarm/parallel/dp/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DPRole
- WorkerHealth
- LoadBalanceStrategy
- DPConfig
- WorkerState
- StepState
- WaveState

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
