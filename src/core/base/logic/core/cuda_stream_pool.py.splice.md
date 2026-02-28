# Splice: src/core/base/logic/core/cuda_stream_pool.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StreamPriority
- StreamState
- StreamStats
- PooledStream
- PooledEvent
- EventPool
- CudaStreamPool

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
