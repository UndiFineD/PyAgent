# Class Breakdown: enums

**File**: `src\infrastructure\services\dev\agent_tests\enums.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TestPriority`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

Test priority levels.

[TIP] **Suggested split**: Move to `testpriority.py`

---

### 2. `TestStatus`

**Line**: 42  
**Inherits**: Enum  
**Methods**: 0

Test execution status.

[TIP] **Suggested split**: Move to `teststatus.py`

---

### 3. `CoverageType`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

Types of coverage to track.

[TIP] **Suggested split**: Move to `coveragetype.py`

---

### 4. `BrowserType`

**Line**: 64  
**Inherits**: Enum  
**Methods**: 0

Browser types for cross-browser testing.

[TIP] **Suggested split**: Move to `browsertype.py`

---

### 5. `TestSourceType`

**Line**: 75  
**Inherits**: Enum  
**Methods**: 0

Types of test result sources for aggregation.

[TIP] **Suggested split**: Move to `testsourcetype.py`

---

### 6. `MutationOperator`

**Line**: 86  
**Inherits**: Enum  
**Methods**: 0

Mutation operators for mutation testing.

[TIP] **Suggested split**: Move to `mutationoperator.py`

---

### 7. `ExecutionMode`

**Line**: 96  
**Inherits**: Enum  
**Methods**: 0

Test execution replay modes.

[TIP] **Suggested split**: Move to `executionmode.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
