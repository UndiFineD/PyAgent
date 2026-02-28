# Splice: src/infrastructure/engine/core/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RequestStatus
- FinishReason
- Request
- SchedulerOutput
- ModelRunnerOutput
- EngineCoreOutput
- EngineCoreOutputs

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
