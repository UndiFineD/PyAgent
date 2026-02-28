# Splice: src/infrastructure/engine/kv_cache/data_classes.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BlockHash
- BlockHashWithGroupId
- KVCacheBlock
- KVCacheBlocks
- CacheGroupSpec
- CacheConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
