# TensorSchema

**File**: `src\core\base\validation\TensorSchema.py`  
**Type**: Python Module  
**Summary**: 3 classes, 2 functions, 11 imports  
**Lines**: 329  
**Complexity**: 16 (moderate)

## Overview

TensorSchema - Tensor shape validation with symbolic dimensions.

Implements vLLM's tensor schema pattern for validating tensor shapes
with symbolic dimension names that can be resolved at runtime.

Phase 23: Advanced Serialization & Validation

## Classes (3)

### `DynamicDim`

Marker for dynamic dimensions that can vary at runtime.

**Methods** (4):
- `__init__(self, name)`
- `__repr__(self)`
- `__eq__(self, other)`
- `__hash__(self)`

### `TensorShape`

Represents a tensor shape with symbolic dimensions.

Dimensions can be:
- int: Fixed size
- str: Named symbolic dimension (resolved at runtime)
- DynamicDim: Dimension that can vary (not validated)

Example:
    >>> shape = TensorShape("batch", "seq_len", 768)
    >>> resolved = shape.resolve(batch=32, seq_len=512)
    >>> print(resolved)  # (32, 512, 768)

**Methods** (5):
- `__init__(self)`
- `resolve(self)`
- `matches(self, shape)`
- `__len__(self)`
- `__repr__(self)`

### `TensorSchema`

Schema for validating multiple tensors with related dimensions.

Example:
    >>> schema = TensorSchema(
    ...     input_ids=TensorShape("batch", "seq_len"),
    ...     attention_mask=TensorShape("batch", "seq_len"),
    ...     hidden_states=TensorShape("batch", "seq_len", 768),
    ... )
    >>> schema.validate(input_ids=input_tensor, attention_mask=mask_tensor)

**Methods** (5):
- `__init__(self, validate, resolve_bindings)`
- `validate(self)`
- `_get_shape(self, tensor)`
- `_get_nested_shape(self, nested, depth)`
- `__repr__(self)`

## Functions (2)

### `validate_tensor(tensor)`

Validate a single tensor's shape.

Args:
    tensor: Tensor to validate
    *dims: Expected dimensions
    dynamic_dims: Set of dynamic dimension names
    **bindings: Dimension bindings
    
Returns:
    True if valid
    
Raises:
    ValueError: If shape doesn't match

### `validate_tensor_shape(shape, expected, dynamic_dims)`

Validate a shape tuple against expected pattern.

Args:
    shape: Actual shape tuple
    expected: Expected shape pattern
    dynamic_dims: Dynamic dimension names
    **bindings: Dimension bindings
    
Returns:
    True if valid

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `torch`
- `typing.Annotated`
- `typing.Any`
- `typing.Union`
- `typing.get_args`
- `typing.get_origin`
- `typing.get_type_hints`

---
*Auto-generated documentation*
