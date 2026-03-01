# KVCacheMetrics

**File**: `src\infrastructure\cache\KVCacheMetrics.py`  
**Type**: Python Module  
**Summary**: 9 classes, 1 functions, 15 imports  
**Lines**: 597  
**Complexity**: 32 (complex)

## Overview

KV Cache Metrics Collector for Block Lifecycle Tracking.

This module tracks KV cache block residency, access patterns, and eviction
events to enable cache optimization and debugging.

Features beyond vLLM:
- Rich block lifecycle analytics
- Access pattern trend detection
- Anomaly detection for cache behavior
- Configurable sampling rates
- Export to various formats

## Classes (9)

### `MetricType`

**Inherits from**: Enum

Types of metrics collected.

### `AlertLevel`

**Inherits from**: Enum

Alert severity levels.

### `MetricsConfig`

Configuration for metrics collection.

**Methods** (1):
- `__post_init__(self)`

### `BlockMetricsState`

Tracks lifecycle metrics for a single KV cache block.

**Methods** (5):
- `record_access(self)`
- `get_lifetime_seconds(self)`
- `get_idle_time_seconds(self)`
- `get_reuse_gaps_seconds(self)`
- `get_access_frequency(self)`

### `KVCacheEvictionEvent`

Event for block eviction.

**Methods** (1):
- `to_dict(self)`

### `CacheAlert`

Alert for cache anomalies.

### `CacheMetricsSummary`

Summary of cache metrics.

**Methods** (1):
- `to_dict(self)`

### `KVCacheMetricsCollector`

Collects KV cache residency metrics with sampling.

Implements vLLM's KVCacheMetricsCollector with extensions:
- Trend detection
- Anomaly detection
- Rich analytics
- Export functionality

**Methods** (14):
- `__init__(self, config)`
- `should_sample_block(self)`
- `on_block_allocated(self, block_id)`
- `on_block_accessed(self, block_id)`
- `on_block_evicted(self, block_id, reason)`
- `_check_anomalies(self, event)`
- `get_summary(self)`
- `get_lifetime_distribution(self, buckets)`
- `get_access_pattern_analysis(self)`
- `detect_trends(self)`
- ... and 4 more methods

### `BatchMetricsCollector`

Batch-optimized metrics collection for high-throughput scenarios.

Beyond vLLM: Efficient batch event processing with reduced overhead.

**Methods** (9):
- `__init__(self, sample_rate)`
- `batch_allocate(self, block_ids)`
- `batch_access(self, block_ids)`
- `batch_evict(self, block_ids, reason)`
- `_flush_allocations(self)`
- `_flush_accesses(self)`
- `_flush_evictions(self)`
- `flush_all(self)`
- `get_summary(self)`

## Functions (1)

### `create_metrics_collector(sample_rate, batch_mode)`

Factory function to create metrics collector.

Args:
    sample_rate: Fraction of blocks to sample
    batch_mode: Use batch-optimized collector
    **kwargs: Additional config options

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `numpy.typing.NDArray`
- `random`
- `rust_core`
- `statistics`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
