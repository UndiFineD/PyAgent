# PrometheusRegistry

**File**: `src\infrastructure\metrics\PrometheusRegistry.py`  
**Type**: Python Module  
**Summary**: 14 classes, 1 functions, 20 imports  
**Lines**: 670  
**Complexity**: 55 (very_complex)

## Overview

Phase 45: Prometheus Metrics Registry
vLLM-inspired prometheus integration with multiprocessing support.

Beyond vLLM:
- Multi-backend support (Prometheus, StatsD, OpenTelemetry)
- Automatic metric aggregation
- Custom histogram buckets
- Metric sampling for high-frequency counters
- Rate limiting for cardinality protection

## Classes (14)

### `MetricType`

**Inherits from**: Enum

Types of metrics.

### `MetricsBackend`

**Inherits from**: Enum

Metrics backend types.

### `MetricSpec`

Specification for a metric.

**Methods** (1):
- `full_name(self)`

### `MetricValue`

Container for metric value with labels.

### `MetricCollector`

**Inherits from**: ABC

Abstract base for metric collectors.

**Methods** (4):
- `increment(self, value, labels)`
- `set(self, value, labels)`
- `observe(self, value, labels)`
- `get(self, labels)`

### `Counter`

**Inherits from**: MetricCollector

Thread-safe counter metric.

**Methods** (7):
- `__init__(self, spec)`
- `_label_key(self, labels)`
- `increment(self, value, labels)`
- `set(self, value, labels)`
- `observe(self, value, labels)`
- `get(self, labels)`
- `get_all(self)`

### `Gauge`

**Inherits from**: MetricCollector

Thread-safe gauge metric.

**Methods** (8):
- `__init__(self, spec)`
- `_label_key(self, labels)`
- `increment(self, value, labels)`
- `decrement(self, value, labels)`
- `set(self, value, labels)`
- `observe(self, value, labels)`
- `get(self, labels)`
- `get_all(self)`

### `HistogramBucket`

Single histogram bucket.

### `Histogram`

**Inherits from**: MetricCollector

Thread-safe histogram metric with configurable buckets.

**Methods** (9):
- `__init__(self, spec)`
- `_label_key(self, labels)`
- `_get_or_create(self, key)`
- `increment(self, value, labels)`
- `set(self, value, labels)`
- `observe(self, value, labels)`
- `get(self, labels)`
- `get_sum(self, labels)`
- `get_buckets(self, labels)`

### `Summary`

**Inherits from**: MetricCollector

Thread-safe summary metric with quantiles.

**Methods** (8):
- `__init__(self, spec, max_age_seconds, max_samples)`
- `_label_key(self, labels)`
- `_prune(self, samples, now)`
- `increment(self, value, labels)`
- `set(self, value, labels)`
- `observe(self, value, labels)`
- `get(self, labels)`
- `get_quantile(self, quantile, labels)`

### `MetricsRegistry`

Central registry for all metrics.

Features:
- Thread-safe metric registration
- Multiprocessing support
- Multiple backend support
- Automatic cleanup

**Methods** (12):
- `__init__(self, backend)`
- `get_instance(cls, backend)`
- `setup_multiprocess(self)`
- `register(self, spec)`
- `get(self, name)`
- `counter(self, name, description, labels, namespace, subsystem)`
- `gauge(self, name, description, labels, namespace, subsystem)`
- `histogram(self, name, description, labels, buckets, namespace, subsystem)`
- `summary(self, name, description, labels, namespace, subsystem)`
- `collect_all(self)`
- ... and 2 more methods

### `SampledCounter`

**Inherits from**: Counter

Counter with sampling for high-frequency operations.

Beyond vLLM: Rate-limited counter to prevent cardinality explosion.

**Methods** (2):
- `__init__(self, spec, sample_rate)`
- `increment(self, value, labels)`

### `RateLimitedGauge`

**Inherits from**: Gauge

Gauge with rate limiting for updates.

Beyond vLLM: Prevents excessive updates in hot paths.

**Methods** (2):
- `__init__(self, spec, min_interval)`
- `set(self, value, labels)`

### `VLLMMetrics`

Collection of vLLM-compatible metrics.

**Methods** (1):
- `__init__(self, registry)`

## Functions (1)

### `get_metrics()`

Get the global VLLMMetrics instance.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `os`
- `rust_core`
- `tempfile`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 5 more

---
*Auto-generated documentation*
