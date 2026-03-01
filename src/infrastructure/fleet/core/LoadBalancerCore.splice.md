# Class Breakdown: LoadBalancerCore

**File**: `src\infrastructure\fleet\core\LoadBalancerCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentMetrics`

**Line**: 7  
**Methods**: 0

[TIP] **Suggested split**: Move to `agentmetrics.py`

---

### 2. `LoadBalancerCore`

**Line**: 13  
**Methods**: 3

Pure logic for cognitive load balancing across the agent fleet.
Calculates cognitive pressure and suggests optimal task routing.

[TIP] **Suggested split**: Move to `loadbalancercore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
