# config

**File**: `src\infrastructure\models\registry\config.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 12 imports  
**Lines**: 165  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for config.

## Classes (8)

### `ModelCapability`

**Inherits from**: Flag

Model capability flags.

### `ModelArchitecture`

**Inherits from**: Enum

Known model architectures.

### `QuantizationType`

**Inherits from**: Enum

Quantization types.

### `ModelFormat`

**Inherits from**: Enum

Model file formats.

### `ModelConfig`

Model configuration.

**Methods** (1):
- `__hash__(self)`

### `ArchitectureSpec`

Architecture specification.

### `ModelInfo`

Information about a model.

**Methods** (3):
- `is_multimodal(self)`
- `has_gqa(self)`
- `to_dict(self)`

### `VRAMEstimate`

VRAM requirement estimation.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.Flag`
- `enum.auto`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
