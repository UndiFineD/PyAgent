# Class Breakdown: config

**File**: `src\infrastructure\position\rotary\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RoPEVariant`

**Line**: 5  
**Inherits**: Enum  
**Methods**: 0

Supported RoPE variants.

[TIP] **Suggested split**: Move to `ropevariant.py`

---

### 2. `RoPEScalingType`

**Line**: 13  
**Inherits**: Enum  
**Methods**: 0

Supported position scaling types.

[TIP] **Suggested split**: Move to `ropescalingtype.py`

---

### 3. `RoPEConfig`

**Line**: 21  
**Methods**: 1

Configuration for Rotary Position Embeddings.

[TIP] **Suggested split**: Move to `ropeconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
