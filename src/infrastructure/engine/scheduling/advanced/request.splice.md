# Class Breakdown: request

**File**: `src\infrastructure\engine\scheduling\advanced\request.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestMetrics`

**Line**: 29  
**Methods**: 2

Metrics for a single request.

[TIP] **Suggested split**: Move to `requestmetrics.py`

---

### 2. `ScheduledRequest`

**Line**: 56  
**Methods**: 6

A request scheduled for inference.

[TIP] **Suggested split**: Move to `scheduledrequest.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
