# Class Breakdown: manager

**File**: `src\infrastructure\engine\quantization\manager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `QuantizationMode`

**Line**: 32  
**Inherits**: Enum  
**Methods**: 0

Supported quantization modes.

[TIP] **Suggested split**: Move to `quantizationmode.py`

---

### 2. `QuantizationManager`

**Line**: 44  
**Methods**: 5

Manages quantization states and hardware-accelerated kernels.
Integrates with rust_core for fast bit-unpacking and scale application.

[TIP] **Suggested split**: Move to `quantizationmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
