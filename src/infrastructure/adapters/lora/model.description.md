# model

**File**: `src\infrastructure\adapters\lora\model.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 55  
**Complexity**: 5 (moderate)

## Overview

LoRA model container.

## Classes (1)

### `LoRAModel`

Complete LoRA model with all adapter weights.

**Methods** (5):
- `add_layer(self, layer)`
- `get_layer(self, module_name)`
- `forward(self, module_name, x, apply_dropout)`
- `get_memory_bytes(self)`
- `num_parameters(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `config.LoRAConfig`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `numpy.typing.NDArray`
- `typing.Any`
- `typing.TYPE_CHECKING`
- `weights.LoRALayerWeights`

---
*Auto-generated documentation*
