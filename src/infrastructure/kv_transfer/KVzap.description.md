# KVzap

**File**: `src\infrastructure\kv_transfer\KVzap.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 95  
**Complexity**: 6 (moderate)

## Overview

KVzap: Surrogate-model-based KV cache pruning.
Implemented based on arXiv:2601.07891 (NVIDIA research, Jan 2026).

## Classes (3)

### `KVzapConfig`

Configuration for KVzap pruning.

### `KVzapSurrogate`

**Inherits from**: Module

Lightweight surrogate model to predict KV importance scores from hidden states.
Efficiently predicts which tokens can be safely pruned from the cache.

**Methods** (2):
- `__init__(self, config)`
- `forward(self, hidden_states)`

### `KVzapPruner`

Orchestrates KV cache pruning using the surrogate model.

**Methods** (4):
- `__init__(self, config)`
- `get_importance_scores(self, hidden_states)`
- `create_pruning_mask(self, scores)`
- `prune_kv(self, hidden_states, keys, values)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `torch`
- `torch.nn`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
