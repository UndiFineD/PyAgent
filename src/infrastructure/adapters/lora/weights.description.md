# weights

**File**: `src\infrastructure\adapters\lora\weights.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 107  
**Complexity**: 9 (moderate)

## Overview

LoRA layer weight implementations.

## Classes (2)

### `LoRALayerWeights`

LoRA weights for a single layer.

**Methods** (6):
- `rank(self)`
- `in_features(self)`
- `out_features(self)`
- `forward(self, x, apply_dropout)`
- `merge_into_base(self, base_weight)`
- `get_memory_bytes(self)`

### `PackedLoRAWeights`

Packed LoRA weights for fused QKV or gate+up projections.

**Methods** (3):
- `from_individual(cls, layer_weights)`
- `unpack(self)`
- `num_layers(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `numpy`
- `numpy.typing.NDArray`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
