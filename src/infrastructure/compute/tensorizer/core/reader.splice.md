# Class Breakdown: reader

**File**: `src\infrastructure\compute\tensorizer\core\reader.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoadProgress`

**Line**: 39  
**Methods**: 2

Progress information for loading.

[TIP] **Suggested split**: Move to `loadprogress.py`

---

### 2. `TensorizerReader`

**Line**: 63  
**Methods**: 15

Reads tensors from a tensorizer file format.

Supports memory-mapped access and parallel loading.

[TIP] **Suggested split**: Move to `tensorizerreader.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
