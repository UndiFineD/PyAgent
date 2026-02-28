# Splice: src/infrastructure/engine/iteration_metrics.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricType
- BaseCacheStats
- PrefixCacheStats
- MultiModalCacheStats
- KVCacheEvictionEvent
- CachingMetrics
- RequestStateStats
- FinishedRequestStats
- SchedulerStats
- IterationStats
- PercentileTracker
- TrendAnalyzer
- AnomalyDetector
- MetricsCollector

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
