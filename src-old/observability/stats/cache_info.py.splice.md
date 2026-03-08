# Splice: src/observability/stats/cache_info.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CacheStats
- CacheEntry
- LRUCache
- TTLLRUCache

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
