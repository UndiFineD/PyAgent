# Class Breakdown: config

**File**: `src\infrastructure\compute\tensorizer\core\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TensorDtype`

**Line**: 26  
**Inherits**: Enum  
**Methods**: 0

Supported tensor data types.

[TIP] **Suggested split**: Move to `tensordtype.py`

---

### 2. `CompressionType`

**Line**: 38  
**Inherits**: Enum  
**Methods**: 0

Supported compression types.

[TIP] **Suggested split**: Move to `compressiontype.py`

---

### 3. `TensorizerConfig`

**Line**: 64  
**Methods**: 0

Configuration for tensorizer operations.

[TIP] **Suggested split**: Move to `tensorizerconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
