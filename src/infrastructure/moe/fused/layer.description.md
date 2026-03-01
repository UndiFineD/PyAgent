# layer

**File**: `src\infrastructure\moe\fused\layer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 108  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for layer.

## Classes (1)

### `FusedMoELayer`

Fused Mixture of Experts layer.

**Methods** (5):
- `__init__(self, config, parallel_config, quant_config, method)`
- `forward(self, x, router_logits)`
- `_update_stats(self, router_logits)`
- `get_expert_utilization(self)`
- `_compute_load_balance_loss(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `config.FusedMoEConfig`
- `config.FusedMoEParallelConfig`
- `config.FusedMoEQuantConfig`
- `dispatcher.SparseDispatcher`
- `method.FusedMoEMethodBase`
- `method.UnquantizedFusedMoEMethod`
- `numpy`
- `threading`
- `typing.Any`
- `typing.Optional`
- `utils.determine_expert_map`

---
*Auto-generated documentation*
