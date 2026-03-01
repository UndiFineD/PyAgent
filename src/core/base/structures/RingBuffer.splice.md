# Class Breakdown: RingBuffer

**File**: `src\core\base\structures\RingBuffer.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RingBuffer`

**Line**: 23  
**Inherits**: Unknown  
**Methods**: 15

Fixed-size circular buffer with O(1) operations.

When full, new items overwrite the oldest items.

Example:
    >>> rb = RingBuffer(capacity=5)
    >>> for i in range(10):
    ...     rb.append(i)
  ...

[TIP] **Suggested split**: Move to `ringbuffer.py`

---

### 2. `ThreadSafeRingBuffer`

**Line**: 197  
**Inherits**: Unknown  
**Methods**: 10

Thread-safe version of RingBuffer.

Uses locking for safe concurrent access.

[TIP] **Suggested split**: Move to `threadsaferingbuffer.py`

---

### 3. `TimestampedValue`

**Line**: 257  
**Inherits**: Unknown  
**Methods**: 1

Value with timestamp for time-series data.

[TIP] **Suggested split**: Move to `timestampedvalue.py`

---

### 4. `TimeSeriesBuffer`

**Line**: 268  
**Inherits**: Unknown  
**Methods**: 6

Ring buffer with time-based operations.

Useful for metrics collection with time windows.

Example:
    >>> ts = TimeSeriesBuffer(capacity=1000, max_age_seconds=60.0)
    >>> 
    >>> ts.append(100.5)...

[TIP] **Suggested split**: Move to `timeseriesbuffer.py`

---

### 5. `SlidingWindowAggregator`

**Line**: 363  
**Methods**: 13

Efficient sliding window aggregation for streaming metrics.

Supports multiple aggregation functions with O(1) updates.

Example:
    >>> agg = SlidingWindowAggregator(window_seconds=60.0)
    >>> 
  ...

[TIP] **Suggested split**: Move to `slidingwindowaggregator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
