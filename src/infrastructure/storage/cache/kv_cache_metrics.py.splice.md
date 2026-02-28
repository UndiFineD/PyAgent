# Splice: src/infrastructure/storage/cache/kv_cache_metrics.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricType
- AlertLevel
- MetricsConfig
- BlockMetricsState
- KVCacheEvictionEvent
- CacheAlert
- CacheMetricsSummary
- KVCacheMetricsCollector
- BatchMetricsCollector

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
