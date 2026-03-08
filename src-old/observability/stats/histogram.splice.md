# Class Breakdown: histogram

**File**: `src\observability\stats\histogram.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HistogramBucket`

**Line**: 37  
**Methods**: 1

A single histogram bucket.

[TIP] **Suggested split**: Move to `histogrambucket.py`

---

### 2. `Histogram`

**Line**: 50  
**Methods**: 16

Fixed-bucket histogram for efficient distribution tracking.

Provides approximate percentiles with constant memory.

Example:
    >>> h = Histogram(min_value=1.0, max_value=10000.0, num_buckets=100)
 ...

[TIP] **Suggested split**: Move to `histogram.py`

---

### 3. `ExponentialHistogram`

**Line**: 277  
**Methods**: 10

Histogram with exponentially growing bucket boundaries.

Based on OpenTelemetry exponential histogram spec.
Better accuracy for wide value ranges.

Example:
    >>> h = ExponentialHistogram(scale=2)
 ...

[TIP] **Suggested split**: Move to `exponentialhistogram.py`

---

### 4. `LatencyHistogram`

**Line**: 419  
**Inherits**: Histogram  
**Methods**: 1

Pre-configured histogram for latency tracking (microseconds to seconds).

Common for API response time monitoring.

Example:
    >>> latency = LatencyHistogram()
    >>>
    >>> start = time.perf_coun...

[TIP] **Suggested split**: Move to `latencyhistogram.py`

---

### 5. `SizeHistogram`

**Line**: 445  
**Inherits**: Histogram  
**Methods**: 1

Pre-configured histogram for size tracking (bytes).

Common for request/response size monitoring.

Example:
    >>> sizes = SizeHistogram()
    >>>
    >>> sizes.add(len(response_body))
    >>>
    >>...

[TIP] **Suggested split**: Move to `sizehistogram.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
