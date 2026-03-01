# Class Breakdown: config

**File**: `src\infrastructure\quantization\engine\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `QuantScheme`

**Line**: 4  
**Inherits**: Enum  
**Methods**: 0

Quantization scheme types.

[TIP] **Suggested split**: Move to `quantscheme.py`

---

### 2. `QuantStrategy`

**Line**: 13  
**Inherits**: Enum  
**Methods**: 0

Quantization granularity strategy.

[TIP] **Suggested split**: Move to `quantstrategy.py`

---

### 3. `QuantConfig`

**Line**: 21  
**Methods**: 5

Configuration for quantization.

[TIP] **Suggested split**: Move to `quantconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
