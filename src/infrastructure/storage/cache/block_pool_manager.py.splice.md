# Splice: src/infrastructure/storage/cache/block_pool_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BlockState
- Block
- BlockPoolConfig
- EvictionEvent
- CacheMetrics
- KVCacheMetricsCollector
- ARCPolicy
- BlockPool

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
