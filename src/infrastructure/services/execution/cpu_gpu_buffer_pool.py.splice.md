# Splice: src/infrastructure/services/execution/cpu_gpu_buffer_pool.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MemoryPlacement
- CpuGpuBuffer
- UvaBufferPool
- PinnedMemoryManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
