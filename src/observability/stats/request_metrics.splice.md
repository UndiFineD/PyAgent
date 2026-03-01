# Class Breakdown: request_metrics

**File**: `src\observability\stats\request_metrics.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestState`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

States a request can be in.

[TIP] **Suggested split**: Move to `requeststate.py`

---

### 2. `RequestMetrics`

**Line**: 45  
**Methods**: 21

Comprehensive timing metrics for request processing.

Tracks detailed timing breakdown from arrival to completion:
- Queue time: How long request waited in queue
- Schedule time: Time to schedule/rout...

[TIP] **Suggested split**: Move to `requestmetrics.py`

---

### 3. `RequestMetricsAggregator`

**Line**: 258  
**Methods**: 15

Aggregates metrics from multiple requests for analysis.

Example:
    >>> aggregator = RequestMetricsAggregator()
    >>> aggregator.add(metrics1)
    >>> aggregator.add(metrics2)
    >>> print(aggreg...

[TIP] **Suggested split**: Move to `requestmetricsaggregator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
