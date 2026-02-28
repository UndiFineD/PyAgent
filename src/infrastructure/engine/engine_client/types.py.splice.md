# Splice: src/infrastructure/engine/engine_client/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ClientMode
- WorkerState
- EngineClientConfig
- SchedulerOutput
- EngineOutput
- WorkerInfo

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
