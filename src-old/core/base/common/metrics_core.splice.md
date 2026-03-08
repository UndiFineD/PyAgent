# Class Breakdown: metrics_core

**File**: `src\core\base\common\metrics_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MetricRecord`

**Line**: 41  
**Methods**: 0

Represents a single metric data point.

[TIP] **Suggested split**: Move to `metricrecord.py`

---

### 2. `AgentMetrics`

**Line**: 51  
**Methods**: 5

Manages execution metrics and statistics for an agent.

[TIP] **Suggested split**: Move to `agentmetrics.py`

---

### 3. `MetricsCore`

**Line**: 112  
**Inherits**: BaseCore  
**Methods**: 17

Authoritative engine for agent metrics collection and performance analysis.

[TIP] **Suggested split**: Move to `metricscore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
