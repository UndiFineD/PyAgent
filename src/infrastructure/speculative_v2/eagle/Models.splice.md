# Class Breakdown: Models

**File**: `src\infrastructure\speculative_v2\eagle\Models.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DraftOutput`

**Line**: 13  
**Methods**: 0

Output from draft model forward pass.

[TIP] **Suggested split**: Move to `draftoutput.py`

---

### 2. `DraftModelWrapper`

**Line**: 21  
**Inherits**: ABC  
**Methods**: 2

Abstract wrapper for draft model.

[TIP] **Suggested split**: Move to `draftmodelwrapper.py`

---

### 3. `SimpleDraftModel`

**Line**: 40  
**Inherits**: DraftModelWrapper  
**Methods**: 3

Simple mock draft model for testing.

[TIP] **Suggested split**: Move to `simpledraftmodel.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
