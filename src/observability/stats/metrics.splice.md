# Class Breakdown: metrics

**File**: `src\observability\stats\metrics.py`  
**Classes**: 17

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MetricType`

**Line**: 21  
**Inherits**: Enum  
**Methods**: 0

Types of metrics.

[TIP] **Suggested split**: Move to `metrictype.py`

---

### 2. `Metric`

**Line**: 31  
**Methods**: 2

A single metric.

[TIP] **Suggested split**: Move to `metric.py`

---

### 3. `AgentMetric`

**Line**: 53  
**Methods**: 0

Telemetry data for a single agent operation.

[TIP] **Suggested split**: Move to `agentmetric.py`

---

### 4. `MetricSnapshot`

**Line**: 73  
**Methods**: 0

A snapshot of metrics at a point in time.

[TIP] **Suggested split**: Move to `metricsnapshot.py`

---

### 5. `AggregationType`

**Line**: 86  
**Inherits**: Enum  
**Methods**: 0

Types of metric aggregation for rollups.

[TIP] **Suggested split**: Move to `aggregationtype.py`

---

### 6. `AggregationResult`

**Line**: 100  
**Inherits**: Unknown  
**Methods**: 2

Compatibility class that behaves like both a dict and a float.

[TIP] **Suggested split**: Move to `aggregationresult.py`

---

### 7. `MetricNamespace`

**Line**: 112  
**Methods**: 0

Namespace for organizing metrics.

[TIP] **Suggested split**: Move to `metricnamespace.py`

---

### 8. `MetricAnnotation`

**Line**: 124  
**Methods**: 0

Annotation or comment on a metric.

[TIP] **Suggested split**: Move to `metricannotation.py`

---

### 9. `MetricCorrelation`

**Line**: 135  
**Methods**: 0

Correlation between two metrics.

[TIP] **Suggested split**: Move to `metriccorrelation.py`

---

### 10. `MetricSubscription`

**Line**: 146  
**Methods**: 0

Subscription for metric change notifications.

[TIP] **Suggested split**: Move to `metricsubscription.py`

---

### 11. `StatsNamespace`

**Line**: 158  
**Methods**: 3

Represents a namespace for metric isolation.

[TIP] **Suggested split**: Move to `statsnamespace.py`

---

### 12. `StatsSnapshot`

**Line**: 178  
**Methods**: 0

A persisted snapshot for StatsSnapshotManager.

[TIP] **Suggested split**: Move to `statssnapshot.py`

---

### 13. `StatsSubscription`

**Line**: 187  
**Methods**: 0

A subscription entry for StatsSubscriptionManager.

[TIP] **Suggested split**: Move to `statssubscription.py`

---

### 14. `DerivedMetric`

**Line**: 198  
**Methods**: 0

Definition for a metric calculated from other metrics.

[TIP] **Suggested split**: Move to `derivedmetric.py`

---

### 15. `RetentionPolicy`

**Line**: 208  
**Methods**: 0

Policy for data retention.

[TIP] **Suggested split**: Move to `retentionpolicy.py`

---

### 16. `ABComparisonResult`

**Line**: 222  
**Methods**: 0

[TIP] **Suggested split**: Move to `abcomparisonresult.py`

---

### 17. `ABSignificanceResult`

**Line**: 228  
**Methods**: 0

[TIP] **Suggested split**: Move to `absignificanceresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
