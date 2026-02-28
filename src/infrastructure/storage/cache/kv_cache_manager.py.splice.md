# Splice: src/infrastructure/storage/cache/kv_cache_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DeviceType
- DType
- KVCacheConfig
- KVCacheBlock
- KVCacheBlocks
- KVCacheAllocator
- PagedKVCache
- KVCacheTransfer
- KVCacheManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
