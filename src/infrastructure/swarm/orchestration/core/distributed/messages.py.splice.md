# Splice: src/infrastructure/swarm/orchestration/core/distributed/messages.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CoordinatorMessage
- RequestMessage
- ResponseMessage
- ControlMessage
- MetricsMessage

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
