# Class Breakdown: dispatcher

**File**: `src\infrastructure\compute\moe\fused\dispatcher.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SparseDispatcher`

**Line**: 26  
**Methods**: 3

Sparse dispatcher for token-to-expert assignment.

[TIP] **Suggested split**: Move to `sparsedispatcher.py`

---

### 2. `DenseDispatcher`

**Line**: 97  
**Methods**: 2

Dense dispatcher using matrix operations.

[TIP] **Suggested split**: Move to `densedispatcher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
