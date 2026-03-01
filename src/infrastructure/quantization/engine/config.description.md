# config

**File**: `src\infrastructure\quantization\engine\config.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 2 imports  
**Lines**: 56  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for config.

## Classes (3)

### `QuantScheme`

**Inherits from**: Enum

Quantization scheme types.

### `QuantStrategy`

**Inherits from**: Enum

Quantization granularity strategy.

### `QuantConfig`

Configuration for quantization.

**Methods** (5):
- `__post_init__(self)`
- `_validate(self)`
- `pack_factor(self)`
- `qmin(self)`
- `qmax(self)`

## Dependencies

**Imports** (2):
- `dataclasses.dataclass`
- `enum.Enum`

---
*Auto-generated documentation*
