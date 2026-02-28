# Splice: src/infrastructure/engine/scheduling/disaggregated/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- InstanceInfo
- DCPConfig
- KVTransferParams
- ScheduledRequest

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
