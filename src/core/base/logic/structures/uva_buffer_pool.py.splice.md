# Splice: src/core/base/logic/structures/uva_buffer_pool.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BufferState
- AllocationStrategy
- BufferStats
- UvaBuffer
- UvaBufferPool
- UvaBackedTensor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
