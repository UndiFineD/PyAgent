# Splice: src/infrastructure/storage/cache/prefix_cache_optimizer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CacheTier
- PrefixCacheConfig
- PrefixEntry
- CacheHitResult
- RadixTreeNode
- PrefixTree
- PrefixCacheOptimizer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
