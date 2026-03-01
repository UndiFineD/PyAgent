# Class Breakdown: scheduling

**File**: `src\infrastructure\services\dev\agent_tests\scheduling.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CrossBrowserRunner`

**Line**: 31  
**Methods**: 5

Cross-browser testing configuration and execution.

[TIP] **Suggested split**: Move to `crossbrowserrunner.py`

---

### 2. `TestScheduler`

**Line**: 89  
**Methods**: 7

Test scheduling and load balancing.

[TIP] **Suggested split**: Move to `testscheduler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
