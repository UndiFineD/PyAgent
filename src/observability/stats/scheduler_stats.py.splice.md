# Splice: src/observability/stats/scheduler_stats.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricExportFormat
- PrefixCacheStats
- SpecDecodingStats
- CUDAGraphStats
- PerfStats
- KVCacheEvictionEvent
- SchedulerStats
- SchedulerStatsCollector

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
