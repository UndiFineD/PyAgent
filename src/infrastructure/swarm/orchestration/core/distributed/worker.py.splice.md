# Splice: src/infrastructure/swarm/orchestration/core/distributed/worker.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BaseWorker
- WorkerProcess

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
