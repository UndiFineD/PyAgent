# Splice: src/infrastructure/swarm/distributed/nccl/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ReduceOp
- NCCLConfig
- NCCLStats

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
