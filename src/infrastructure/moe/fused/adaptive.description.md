# adaptive

**File**: `src\infrastructure\moe\fused\adaptive.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 110  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for adaptive.

## Classes (2)

### `AdaptiveMoELayer`

**Inherits from**: FusedMoELayer

Adaptive MoE layer with dynamic top-k selection and capacity management.

**Methods** (2):
- `__init__(self, config)`
- `forward(self, x, router_logits, context_score)`

### `HierarchicalMoELayer`

Two-level hierarchical MoE for extreme scale.

**Methods** (3):
- `__init__(self, config, num_clusters, cluster_top_k)`
- `forward(self, x)`
- `_softmax(self, x)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `config.FusedMoEConfig`
- `layer.FusedMoELayer`
- `numpy`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
