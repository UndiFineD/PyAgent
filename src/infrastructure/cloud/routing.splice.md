# Class Breakdown: routing

**File**: `src\infrastructure\cloud\routing.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RoutingStrategy`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Strategy for selecting providers.

[TIP] **Suggested split**: Move to `routingstrategy.py`

---

### 2. `ProviderMetrics`

**Line**: 33  
**Methods**: 0

Metrics for a registered provider.

[TIP] **Suggested split**: Move to `providermetrics.py`

---

### 3. `RoutingConstraints`

**Line**: 46  
**Methods**: 0

Constraints for routing decisions.

[TIP] **Suggested split**: Move to `routingconstraints.py`

---

### 4. `IntelligentRouter`

**Line**: 56  
**Methods**: 12

Intelligent request router for multi-cloud AI providers.

Manages provider registration, health monitoring, and intelligent
routing based on various optimization strategies.

Example:
    router = Int...

[TIP] **Suggested split**: Move to `intelligentrouter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
