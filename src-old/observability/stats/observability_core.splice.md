# Class Breakdown: observability_core

**File**: `src\observability\stats\observability_core.py`  
**Classes**: 25

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AlertSeverity`

**Line**: 44  
**Inherits**: Enum  
**Methods**: 0

Severity levels for observability alerts.

[TIP] **Suggested split**: Move to `alertseverity.py`

---

### 2. `Alert`

**Line**: 54  
**Methods**: 0

Represents an observability alert.

[TIP] **Suggested split**: Move to `alert.py`

---

### 3. `Threshold`

**Line**: 66  
**Methods**: 0

Defines a threshold for a metric.

[TIP] **Suggested split**: Move to `threshold.py`

---

### 4. `RetentionPolicy`

**Line**: 78  
**Methods**: 0

Policy for data retention.

[TIP] **Suggested split**: Move to `retentionpolicy.py`

---

### 5. `MetricSnapshot`

**Line**: 93  
**Methods**: 0

A snapshot of metrics at a point in time.

[TIP] **Suggested split**: Move to `metricsnapshot.py`

---

### 6. `AggregationType`

**Line**: 103  
**Inherits**: Enum  
**Methods**: 0

Types of metric aggregation for rollups.

[TIP] **Suggested split**: Move to `aggregationtype.py`

---

### 7. `MetricNamespace`

**Line**: 118  
**Methods**: 0

Namespace for organizing metrics.

[TIP] **Suggested split**: Move to `metricnamespace.py`

---

### 8. `MetricAnnotation`

**Line**: 129  
**Methods**: 0

Annotation or comment on a metric.

[TIP] **Suggested split**: Move to `metricannotation.py`

---

### 9. `MetricCorrelation`

**Line**: 140  
**Methods**: 0

Correlation between two metrics.

[TIP] **Suggested split**: Move to `metriccorrelation.py`

---

### 10. `MetricSubscription`

**Line**: 152  
**Methods**: 0

Subscription for metric change notifications.

[TIP] **Suggested split**: Move to `metricsubscription.py`

---

### 11. `ExportDestination`

**Line**: 163  
**Inherits**: Enum  
**Methods**: 0

Cloud monitoring export destinations.

[TIP] **Suggested split**: Move to `exportdestination.py`

---

### 12. `FederatedSource`

**Line**: 174  
**Methods**: 0

A source repository for stats federation.

[TIP] **Suggested split**: Move to `federatedsource.py`

---

### 13. `FederationMode`

**Line**: 186  
**Inherits**: Enum  
**Methods**: 0

Federation modes for multi-repo aggregation.

[TIP] **Suggested split**: Move to `federationmode.py`

---

### 14. `RollupConfig`

**Line**: 196  
**Methods**: 0

Configuration for metric rollups.

[TIP] **Suggested split**: Move to `rollupconfig.py`

---

### 15. `StreamingProtocol`

**Line**: 206  
**Inherits**: Enum  
**Methods**: 0

Protocols for real-time stats streaming.

[TIP] **Suggested split**: Move to `streamingprotocol.py`

---

### 16. `StreamingConfig`

**Line**: 216  
**Methods**: 0

Configuration for real-time stats streaming.

[TIP] **Suggested split**: Move to `streamingconfig.py`

---

### 17. `AgentMetric`

**Line**: 226  
**Methods**: 0

Represents a metric captured from an agent operation.

[TIP] **Suggested split**: Move to `agentmetric.py`

---

### 18. `ObservabilityCore`

**Line**: 242  
**Methods**: 6

Pure logic for processing agent telemetry data.

[TIP] **Suggested split**: Move to `observabilitycore.py`

---

### 19. `StatsCore`

**Line**: 321  
**Methods**: 6

Core logic for statistics processing, separated from the Agent shell.

[TIP] **Suggested split**: Move to `statscore.py`

---

### 20. `StatsNamespace`

**Line**: 427  
**Methods**: 5

Represents a namespace for metric isolation.

[TIP] **Suggested split**: Move to `statsnamespace.py`

---

### 21. `StatsNamespaceManager`

**Line**: 454  
**Methods**: 4

Manages multiple namespaces.

[TIP] **Suggested split**: Move to `statsnamespacemanager.py`

---

### 22. `StatsSnapshot`

**Line**: 476  
**Methods**: 0

A persisted snapshot for StatsSnapshotManager.

[TIP] **Suggested split**: Move to `statssnapshot.py`

---

### 23. `StatsSubscription`

**Line**: 485  
**Methods**: 0

A subscription entry for StatsSubscriptionManager.

[TIP] **Suggested split**: Move to `statssubscription.py`

---

### 24. `ThresholdAlert`

**Line**: 496  
**Methods**: 0

A single threshold alert emitted by ThresholdAlertManager.

[TIP] **Suggested split**: Move to `thresholdalert.py`

---

### 25. `DerivedMetric`

**Line**: 506  
**Methods**: 0

A metric derived from other metrics via a formula.

[TIP] **Suggested split**: Move to `derivedmetric.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
