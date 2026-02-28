# Splice: src/infrastructure/services/execution/async_output_handler.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AsyncState
- CudaEvent
- CudaStream
- AsyncOutput
- AsyncBarrier
- AsyncOutputHandler
- DoubleBuffer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
