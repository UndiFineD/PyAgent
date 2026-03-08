# Splice: src/core/base/logic/structures/object_pool.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- Resettable
- PoolStats
- ObjectPool
- TypedObjectPool
- BufferPool
- TieredBufferPool
- PooledContextManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
