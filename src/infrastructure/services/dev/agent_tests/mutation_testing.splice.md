# Class Breakdown: mutation_testing

**File**: `src\infrastructure\services\dev\agent_tests\mutation_testing.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MutationTester`

**Line**: 30  
**Methods**: 6

Test mutation analysis.

[TIP] **Suggested split**: Move to `mutationtester.py`

---

### 2. `MutationRunner`

**Line**: 123  
**Methods**: 4

Run mutation testing analysis.

[TIP] **Suggested split**: Move to `mutationrunner.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
