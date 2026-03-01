# utils

**File**: `src\infrastructure\adapters\lora\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 8 imports  
**Lines**: 107  
**Complexity**: 4 (simple)

## Overview

Utility functions for LoRA initialization and analysis.

## Functions (4)

### `create_lora_weights(in_features, out_features, rank, alpha, module_name, init_method)`

Create initialized LoRA layer weights.

### `create_lora_model(model_id, layer_dims, config)`

Create a LoRA model with initialized weights.

### `merge_lora_weights(base_weights, lora_model)`

Merge LoRA weights into base model weights.

### `compute_effective_rank(lora_a, lora_b, threshold)`

Compute effective rank of LoRA matrices.

## Dependencies

**Imports** (8):
- `config.LoRAConfig`
- `math`
- `model.LoRAModel`
- `numpy`
- `numpy.typing.NDArray`
- `typing.Any`
- `typing.TYPE_CHECKING`
- `weights.LoRALayerWeights`

---
*Auto-generated documentation*
