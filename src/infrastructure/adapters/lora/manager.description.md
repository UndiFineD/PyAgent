# manager

**File**: `src\infrastructure\adapters\lora\manager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 176  
**Complexity**: 11 (moderate)

## Overview

High-level manager for multi-adapter serving.

## Classes (1)

### `LoRAManager`

High-level manager for LoRA adapter serving.

**Methods** (11):
- `__init__(self, registry, default_config)`
- `load_adapter(self, model_id, weights, config, metadata)`
- `unload_adapter(self, model_id)`
- `set_request_adapter(self, request_id, model_id)`
- `get_request_adapter(self, request_id)`
- `clear_request(self, request_id)`
- `apply_lora(self, request_id, module_name, base_output, x)`
- `batched_apply_lora(self, request_ids, module_name, base_outputs, inputs)`
- `list_adapters(self)`
- `get_adapter_info(self, model_id)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `config.LoRAConfig`
- `model.LoRAModel`
- `numpy`
- `numpy.typing.NDArray`
- `registry.LoRARegistry`
- `typing.Any`
- `typing.TYPE_CHECKING`
- `weights.LoRALayerWeights`

---
*Auto-generated documentation*
