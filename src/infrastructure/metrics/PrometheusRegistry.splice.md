# Class Breakdown: PrometheusRegistry

**File**: `src\infrastructure\metrics\PrometheusRegistry.py`  
**Classes**: 14

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MetricType`

**Line**: 34  
**Inherits**: Enum  
**Methods**: 0

Types of metrics.

[TIP] **Suggested split**: Move to `metrictype.py`

---

### 2. `MetricsBackend`

**Line**: 42  
**Inherits**: Enum  
**Methods**: 0

Metrics backend types.

[TIP] **Suggested split**: Move to `metricsbackend.py`

---

### 3. `MetricSpec`

**Line**: 51  
**Methods**: 1

Specification for a metric.

[TIP] **Suggested split**: Move to `metricspec.py`

---

### 4. `MetricValue`

**Line**: 72  
**Methods**: 0

Container for metric value with labels.

[TIP] **Suggested split**: Move to `metricvalue.py`

---

### 5. `MetricCollector`

**Line**: 79  
**Inherits**: ABC  
**Methods**: 4

Abstract base for metric collectors.

[TIP] **Suggested split**: Move to `metriccollector.py`

---

### 6. `Counter`

**Line**: 103  
**Inherits**: MetricCollector  
**Methods**: 7

Thread-safe counter metric.

[TIP] **Suggested split**: Move to `counter.py`

---

### 7. `Gauge`

**Line**: 140  
**Inherits**: MetricCollector  
**Methods**: 8

Thread-safe gauge metric.

[TIP] **Suggested split**: Move to `gauge.py`

---

### 8. `HistogramBucket`

**Line**: 181  
**Methods**: 0

Single histogram bucket.

[TIP] **Suggested split**: Move to `histogrambucket.py`

---

### 9. `Histogram`

**Line**: 187  
**Inherits**: MetricCollector  
**Methods**: 9

Thread-safe histogram metric with configurable buckets.

[TIP] **Suggested split**: Move to `histogram.py`

---

### 10. `Summary`

**Line**: 251  
**Inherits**: MetricCollector  
**Methods**: 8

Thread-safe summary metric with quantiles.

[TIP] **Suggested split**: Move to `summary.py`

---

### 11. `MetricsRegistry`

**Line**: 317  
**Methods**: 12

Central registry for all metrics.

Features:
- Thread-safe metric registration
- Multiprocessing support
- Multiple backend support
- Automatic cleanup

[TIP] **Suggested split**: Move to `metricsregistry.py`

---

### 12. `SampledCounter`

**Line**: 510  
**Inherits**: Counter  
**Methods**: 2

Counter with sampling for high-frequency operations.

Beyond vLLM: Rate-limited counter to prevent cardinality explosion.

[TIP] **Suggested split**: Move to `sampledcounter.py`

---

### 13. `RateLimitedGauge`

**Line**: 530  
**Inherits**: Gauge  
**Methods**: 2

Gauge with rate limiting for updates.

Beyond vLLM: Prevents excessive updates in hot paths.

[TIP] **Suggested split**: Move to `ratelimitedgauge.py`

---

### 14. `VLLMMetrics`

**Line**: 555  
**Methods**: 1

Collection of vLLM-compatible metrics.

[TIP] **Suggested split**: Move to `vllmmetrics.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
