# IterationMetrics

**File**: `src\infrastructure\engine\IterationMetrics.py`  
**Type**: Python Module  
**Summary**: 14 classes, 0 functions, 14 imports  
**Lines**: 572  
**Complexity**: 36 (complex)

## Overview

Iteration Metrics - Comprehensive per-iteration statistics and metrics.

Implements vLLM's metrics patterns with PyAgent enhancements:
- Cache hit/miss statistics
- Request lifecycle metrics
- Performance counters
- Eviction event tracking

Beyond vLLM:
- Sliding window aggregation
- Percentile tracking
- Anomaly detection
- Trend analysis

## Classes (14)

### `MetricType`

**Inherits from**: Enum

Type of metric.

### `BaseCacheStats`

Base class for cache statistics.

**Methods** (1):
- `hit_rate(self)`

### `PrefixCacheStats`

**Inherits from**: BaseCacheStats

Statistics for prefix cache.

**Methods** (1):
- `record(self, num_tokens, num_hits, preempted)`

### `MultiModalCacheStats`

**Inherits from**: BaseCacheStats

Statistics for multi-modal cache.

**Methods** (1):
- `record(self, num_items, num_hits)`

### `KVCacheEvictionEvent`

Single KV cache block eviction sample.

### `CachingMetrics`

Metrics for caching with sliding window aggregation.

Tracks hit rates over recent N requests.

**Methods** (5):
- `__init__(self, max_recent_requests)`
- `observe(self, stats)`
- `reset(self)`
- `hit_rate(self)`
- `empty(self)`

### `RequestStateStats`

Stats tracked across request lifecycle.

**Methods** (2):
- `record_first_token(self, timestamp)`
- `record_token(self, timestamp)`

### `FinishedRequestStats`

Stats for a completed request.

**Methods** (1):
- `mean_time_per_output_token(self)`

### `SchedulerStats`

Stats from the scheduler.

### `IterationStats`

Comprehensive stats for a single iteration.

**Methods** (1):
- `record_finished(self, request_id, finish_reason, e2e_latency, num_prompt_tokens, num_generation_tokens, num_cached_tokens, is_corrupted)`

### `PercentileTracker`

Track percentiles over a sliding window.

Efficiently computes p50, p90, p95, p99 without storing all values.

**Methods** (10):
- `__init__(self, window_size)`
- `record(self, value)`
- `_ensure_sorted(self)`
- `percentile(self, p)`
- `p50(self)`
- `p90(self)`
- `p95(self)`
- `p99(self)`
- `mean(self)`
- `std(self)`

### `TrendAnalyzer`

Analyze trends in metrics over time.

Detects increasing, decreasing, or stable trends.

**Methods** (3):
- `__init__(self, window_size)`
- `record(self, value, timestamp)`
- `get_trend(self)`

### `AnomalyDetector`

Detect anomalies in metric values using z-score.

**Methods** (4):
- `__init__(self, window_size, z_threshold)`
- `record(self, value)`
- `mean(self)`
- `std(self)`

### `MetricsCollector`

Comprehensive metrics collection.

Aggregates all metrics types with thread safety.

**Methods** (7):
- `__init__(self)`
- `increment(self, name, value)`
- `set_gauge(self, name, value)`
- `record_histogram(self, name, value)`
- `record_trend(self, name, value)`
- `check_anomaly(self, name, value)`
- `get_summary(self)`

## Dependencies

**Imports** (14):
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `statistics`
- `threading`
- `time`
- `typing.Any`
- `typing.Deque`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
