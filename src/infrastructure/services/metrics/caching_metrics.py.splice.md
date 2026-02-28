# Splice: src/infrastructure/services/metrics/caching_metrics.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CacheType
- EvictionReason
- CacheEvent
- EvictionEvent
- CacheStats
- SlidingWindowStats
- SlidingWindowMetrics
- CachingMetrics
- PrefixCacheStats
- MultiLevelCacheMetrics

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
