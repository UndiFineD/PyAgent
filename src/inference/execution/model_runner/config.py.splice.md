# Splice: src/inference/execution/model_runner/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RunnerState
- ModelInput
- ModelOutput
- SchedulerOutput

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
