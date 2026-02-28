# Splice: src/infrastructure/storage/cache/prefix_cache.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EvictionPolicy
- PrefixCacheConfig
- CacheBlock
- PrefixCacheStats
- PrefixCacheManager
- BlockHasher

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
