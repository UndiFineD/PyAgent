# Class Breakdown: TensorSchema

**File**: `src\core\base\validation\TensorSchema.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DynamicDim`

**Line**: 38  
**Methods**: 4

Marker for dynamic dimensions that can vary at runtime.

[TIP] **Suggested split**: Move to `dynamicdim.py`

---

### 2. `TensorShape`

**Line**: 57  
**Methods**: 5

Represents a tensor shape with symbolic dimensions.

Dimensions can be:
- int: Fixed size
- str: Named symbolic dimension (resolved at runtime)
- DynamicDim: Dimension that can vary (not validated)

E...

[TIP] **Suggested split**: Move to `tensorshape.py`

---

### 3. `TensorSchema`

**Line**: 156  
**Methods**: 5

Schema for validating multiple tensors with related dimensions.

Example:
    >>> schema = TensorSchema(
    ...     input_ids=TensorShape("batch", "seq_len"),
    ...     attention_mask=TensorShape("...

[TIP] **Suggested split**: Move to `tensorschema.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
