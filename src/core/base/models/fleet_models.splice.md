# Class Breakdown: fleet_models

**File**: `src\core\base\models\fleet_models.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HealthCheckResult`

**Line**: 31  
**Methods**: 0

Result of agent health check.

[TIP] **Suggested split**: Move to `healthcheckresult.py`

---

### 2. `IncrementalState`

**Line**: 40  
**Methods**: 0

State for incremental processing.

[TIP] **Suggested split**: Move to `incrementalstate.py`

---

### 3. `RateLimitConfig`

**Line**: 48  
**Methods**: 0

Configuration for rate limiting.

[TIP] **Suggested split**: Move to `ratelimitconfig.py`

---

### 4. `TokenBudget`

**Line**: 57  
**Methods**: 4

Manages token allocation.

[TIP] **Suggested split**: Move to `tokenbudget.py`

---

### 5. `ShutdownState`

**Line**: 78  
**Methods**: 0

State for graceful shutdown.

[TIP] **Suggested split**: Move to `shutdownstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
