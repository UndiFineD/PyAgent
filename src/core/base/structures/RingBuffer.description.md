# RingBuffer

**File**: `src\core\base\structures\RingBuffer.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 10 imports  
**Lines**: 546  
**Complexity**: 45 (complex)

## Overview

RingBuffer - Fixed-size circular buffer for efficient streaming data.

Goes beyond vLLM with lock-free ring buffer patterns:
- O(1) append and pop operations
- Fixed memory footprint for unbounded streams
- Sliding window metrics aggregation
- Time-series data collection

Phase 18: Beyond vLLM - Advanced Data Structures

## Classes (5)

### `RingBuffer`

**Inherits from**: Unknown

Fixed-size circular buffer with O(1) operations.

When full, new items overwrite the oldest items.

Example:
    >>> rb = RingBuffer(capacity=5)
    >>> for i in range(10):
    ...     rb.append(i)
    >>> 
    >>> list(rb)  # [5, 6, 7, 8, 9] (oldest 0-4 overwritten)

**Methods** (15):
- `__init__(self, capacity)`
- `capacity(self)`
- `size(self)`
- `is_empty(self)`
- `is_full(self)`
- `append(self, item)`
- `pop(self)`
- `peek(self)`
- `peek_newest(self)`
- `clear(self)`
- ... and 5 more methods

### `ThreadSafeRingBuffer`

**Inherits from**: Unknown

Thread-safe version of RingBuffer.

Uses locking for safe concurrent access.

**Methods** (10):
- `__init__(self, capacity)`
- `capacity(self)`
- `size(self)`
- `append(self, item)`
- `pop(self)`
- `peek(self)`
- `clear(self)`
- `__len__(self)`
- `to_list(self)`
- `get_stats(self)`

### `TimestampedValue`

**Inherits from**: Unknown

Value with timestamp for time-series data.

**Methods** (1):
- `now(cls, value)`

### `TimeSeriesBuffer`

**Inherits from**: Unknown

Ring buffer with time-based operations.

Useful for metrics collection with time windows.

Example:
    >>> ts = TimeSeriesBuffer(capacity=1000, max_age_seconds=60.0)
    >>> 
    >>> ts.append(100.5)  # Response time
    >>> ts.append(98.2)
    >>> 
    >>> print(ts.get_window_stats(window_seconds=10.0))

**Methods** (6):
- `__init__(self, capacity, max_age_seconds)`
- `append(self, value, timestamp)`
- `get_values_in_window(self, window_seconds, now)`
- `get_window_stats(self, window_seconds, now)`
- `size(self)`
- `clear(self)`

### `SlidingWindowAggregator`

Efficient sliding window aggregation for streaming metrics.

Supports multiple aggregation functions with O(1) updates.

Example:
    >>> agg = SlidingWindowAggregator(window_seconds=60.0)
    >>> 
    >>> agg.add(100.0)
    >>> agg.add(150.0)
    >>> agg.add(120.0)
    >>> 
    >>> print(f"Avg: {agg.mean()}, P99: {agg.percentile(99)}")

**Methods** (13):
- `__init__(self, window_seconds, bucket_seconds)`
- `_empty_bucket()`
- `_rotate_buckets(self)`
- `add(self, value)`
- `_get_all_values(self)`
- `count(self)`
- `sum(self)`
- `mean(self)`
- `min(self)`
- `max(self)`
- ... and 3 more methods

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `collections.abc.Iterator`
- `dataclasses.dataclass`
- `statistics`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.TypeVar`

---
*Auto-generated documentation*
