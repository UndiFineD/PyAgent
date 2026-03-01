# config

**File**: `src\infrastructure\moe\fused\config.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 4 imports  
**Lines**: 56  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for config.

## Classes (5)

### `ExpertPlacementStrategy`

**Inherits from**: str, Enum

Strategy for placing experts across devices.

### `MoEQuantMethod`

**Inherits from**: str, Enum

Quantization methods for MoE weights.

### `FusedMoEConfig`

Configuration for a Fused MoE layer.

**Methods** (1):
- `__post_init__(self)`

### `FusedMoEParallelConfig`

Parallelization configuration for MoE.

### `FusedMoEQuantConfig`

Quantization configuration for MoE.

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`

---
*Auto-generated documentation*
