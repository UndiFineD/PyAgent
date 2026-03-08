# Class Breakdown: config

**File**: `src\inference\speculation\engine\config.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SpecMethod`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

Speculative decoding method types.

[TIP] **Suggested split**: Move to `specmethod.py`

---

### 2. `SpeculativeConfig`

**Line**: 42  
**Methods**: 1

Configuration regarding speculative decoding.

[TIP] **Suggested split**: Move to `speculativeconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
