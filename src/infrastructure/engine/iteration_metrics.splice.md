# Class Breakdown: iteration_metrics

**File**: `src\infrastructure\engine\iteration_metrics.py`  
**Classes**: 14

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MetricType`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Type of metric.

[TIP] **Suggested split**: Move to `metrictype.py`

---

### 2. `BaseCacheStats`

**Line**: 51  
**Methods**: 1

Base class for cache statistics.

[TIP] **Suggested split**: Move to `basecachestats.py`

---

### 3. `PrefixCacheStats`

**Line**: 68  
**Inherits**: BaseCacheStats  
**Methods**: 1

Statistics for prefix cache.

[TIP] **Suggested split**: Move to `prefixcachestats.py`

---

### 4. `MultiModalCacheStats`

**Line**: 93  
**Inherits**: BaseCacheStats  
**Methods**: 1

Statistics for multi-modal cache.

[TIP] **Suggested split**: Move to `multimodalcachestats.py`

---

### 5. `KVCacheEvictionEvent`

**Line**: 104  
**Methods**: 0

Single KV cache block eviction sample.

[TIP] **Suggested split**: Move to `kvcacheevictionevent.py`

---

### 6. `CachingMetrics`

**Line**: 114  
**Methods**: 5

Metrics for caching with sliding window aggregation.

Tracks hit rates over recent N requests.

[TIP] **Suggested split**: Move to `cachingmetrics.py`

---

### 7. `RequestStateStats`

**Line**: 174  
**Methods**: 2

Stats tracked across request lifecycle.

[TIP] **Suggested split**: Move to `requeststatestats.py`

---

### 8. `FinishedRequestStats`

**Line**: 205  
**Methods**: 1

Stats for a completed request.

[TIP] **Suggested split**: Move to `finishedrequeststats.py`

---

### 9. `SchedulerStats`

**Line**: 236  
**Methods**: 0

Stats from the scheduler.

[TIP] **Suggested split**: Move to `schedulerstats.py`

---

### 10. `IterationStats`

**Line**: 262  
**Methods**: 1

Comprehensive stats for a single iteration.

[TIP] **Suggested split**: Move to `iterationstats.py`

---

### 11. `PercentileTracker`

**Line**: 316  
**Methods**: 10

Track percentiles over a sliding window.

Efficiently computes p50, p90, p95, p99 without storing all values.

[TIP] **Suggested split**: Move to `percentiletracker.py`

---

### 12. `TrendAnalyzer`

**Line**: 389  
**Methods**: 3

Analyze trends in metrics over time.

Detects increasing, decreasing, or stable trends.

[TIP] **Suggested split**: Move to `trendanalyzer.py`

---

### 13. `AnomalyDetector`

**Line**: 437  
**Methods**: 4

Detect anomalies in metric values using z-score.

[TIP] **Suggested split**: Move to `anomalydetector.py`

---

### 14. `MetricsCollector`

**Line**: 495  
**Methods**: 7

Comprehensive metrics collection.

Aggregates all metrics types with thread safety.

[TIP] **Suggested split**: Move to `metricscollector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
