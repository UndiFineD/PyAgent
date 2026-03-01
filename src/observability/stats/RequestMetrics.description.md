# RequestMetrics

**File**: `src\observability\stats\RequestMetrics.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 363  
**Complexity**: 31 (complex)

## Overview

RequestMetrics - Comprehensive timing breakdown for request processing.

Inspired by vLLM's sequence.py RequestMetrics for production latency analysis.

Phase 17: vLLM Pattern Integration

## Classes (3)

### `RequestState`

**Inherits from**: Enum

States a request can be in.

### `RequestMetrics`

Comprehensive timing metrics for request processing.

Tracks detailed timing breakdown from arrival to completion:
- Queue time: How long request waited in queue
- Schedule time: Time to schedule/route the request
- Processing time: Model/compute time
- Total time: End-to-end latency

Example:
    >>> metrics = RequestMetrics()
    >>> metrics.mark_queued()
    >>> # ... process ...
    >>> metrics.mark_scheduled()
    >>> metrics.mark_processing()
    >>> metrics.mark_completed()
    >>> print(metrics.summary())

**Methods** (21):
- `mark_queued(self)`
- `mark_scheduled(self)`
- `mark_processing(self)`
- `mark_first_token(self)`
- `mark_token(self)`
- `mark_completed(self)`
- `mark_failed(self, error)`
- `mark_cancelled(self)`
- `increment_retry(self)`
- `time_in_queue_ms(self)`
- ... and 11 more methods

### `RequestMetricsAggregator`

Aggregates metrics from multiple requests for analysis.

Example:
    >>> aggregator = RequestMetricsAggregator()
    >>> aggregator.add(metrics1)
    >>> aggregator.add(metrics2)
    >>> print(aggregator.summary())

**Methods** (10):
- `add(self, metric)`
- `clear(self)`
- `total_requests(self)`
- `completed_requests(self)`
- `failed_requests(self)`
- `success_rate(self)`
- `_percentile(self, values, p)`
- `latency_stats(self)`
- `throughput_stats(self)`
- `summary(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Optional`

---
*Auto-generated documentation*
