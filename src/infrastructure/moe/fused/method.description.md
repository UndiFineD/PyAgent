# method

**File**: `src\infrastructure\moe\fused\method.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 166  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for method.

## Classes (2)

### `FusedMoEMethodBase`

**Inherits from**: ABC

Base class for MoE computation methods.

**Methods** (2):
- `create_weights(self, config, parallel_config, device)`
- `apply(self, x, router_logits, top_k, renormalize, weights)`

### `UnquantizedFusedMoEMethod`

**Inherits from**: FusedMoEMethodBase

Unquantized MoE computation method.

**Methods** (4):
- `create_weights(self, config, parallel_config, device)`
- `apply(self, x, router_logits, top_k, renormalize, weights)`
- `_apply_numpy(self, x, router_logits, top_k, renormalize, weights)`
- `_apply_torch(self, x, router_logits, top_k, renormalize, weights)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `config.FusedMoEConfig`
- `config.FusedMoEParallelConfig`
- `numpy`
- `torch`
- `torch.nn.functional`
- `typing.Any`
- `typing.TYPE_CHECKING`
- `utils.determine_expert_map`

---
*Auto-generated documentation*
