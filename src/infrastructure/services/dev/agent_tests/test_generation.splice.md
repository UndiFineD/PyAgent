# Class Breakdown: test_generation

**File**: `src\infrastructure\services\dev\agent_tests\test_generation.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TestGenerator`

**Line**: 31  
**Methods**: 7

Generate tests from specifications.

[TIP] **Suggested split**: Move to `testgenerator.py`

---

### 2. `TestCaseMinimizer`

**Line**: 162  
**Methods**: 4

Minimize test cases for debugging.

[TIP] **Suggested split**: Move to `testcaseminimizer.py`

---

### 3. `TestDocGenerator`

**Line**: 220  
**Methods**: 6

Generates documentation from tests.

[TIP] **Suggested split**: Move to `testdocgenerator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
