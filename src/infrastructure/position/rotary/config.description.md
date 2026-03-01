# config

**File**: `src\infrastructure\position\rotary\config.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 47  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for config.

## Classes (3)

### `RoPEVariant`

**Inherits from**: Enum

Supported RoPE variants.

### `RoPEScalingType`

**Inherits from**: Enum

Supported position scaling types.

### `RoPEConfig`

Configuration for Rotary Position Embeddings.

**Methods** (1):
- `__post_init__(self)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `typing.Any`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
