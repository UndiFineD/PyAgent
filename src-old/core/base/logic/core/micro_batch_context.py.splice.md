# Splice: src/core/base/logic/core/micro_batch_context.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StreamType
- MicroBatchState
- StreamHandle
- MicroBatchInfo
- StreamManager
- MicroBatchContext
- AdaptiveMicroBatchContext

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
