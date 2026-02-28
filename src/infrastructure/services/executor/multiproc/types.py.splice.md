# Splice: src/infrastructure/services/executor/multiproc/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ExecutorBackend
- WorkerState
- WorkerInfo
- TaskMessage
- ResultMessage

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
