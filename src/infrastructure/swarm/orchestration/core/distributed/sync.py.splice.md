# Splice: src/infrastructure/swarm/orchestration/core/distributed/sync.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DistributedSyncProvider
- NixlSyncProvider
- TCPSyncProvider

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
