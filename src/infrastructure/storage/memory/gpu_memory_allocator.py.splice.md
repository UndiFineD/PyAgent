# Splice: src/infrastructure/storage/memory/gpu_memory_allocator.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MemoryState
- AllocationStrategy
- MemoryRegion
- MemorySnapshot
- MemoryPoolConfig
- MemoryPressureEvent
- CuMemAllocator
- MultiGPUMemoryBalancer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
