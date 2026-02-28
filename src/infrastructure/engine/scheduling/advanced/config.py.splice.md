# Splice: src/infrastructure/engine/scheduling/advanced/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RequestPriority
- RequestState
- PreemptionReason
- SchedulerConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
