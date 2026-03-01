# config

**File**: `src\infrastructure\lora\manager\config.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 10 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for config.

## Classes (7)

### `LoRAMethod`

**Inherits from**: Enum

LoRA method variants.

### `AdapterStatus`

**Inherits from**: Enum

Adapter lifecycle status.

### `TargetModule`

**Inherits from**: Enum

Common LoRA target modules.

### `LoRAConfig`

LoRA adapter configuration.

**Methods** (2):
- `computed_scaling(self)`
- `__hash__(self)`

### `LoRARequest`

Request to serve with a LoRA adapter.

**Methods** (1):
- `__hash__(self)`

### `LoRAInfo`

Information about a loaded adapter.

**Methods** (1):
- `to_dict(self)`

### `AdapterSlot`

GPU slot for a LoRA adapter.

**Methods** (1):
- `is_free(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
