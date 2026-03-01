# multimodal

**File**: `src\infrastructure\position\rotary\multimodal.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 127  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for multimodal.

## Classes (1)

### `MRotaryEmbedding`

**Inherits from**: RotaryEmbeddingBase

Multimodal Rotary Position Embedding.

Applies separate rotary embeddings for different modality sections:
- Temporal (time/frame index)
- Height (spatial y)
- Width (spatial x)

**Methods** (5):
- `__init__(self, config)`
- `_compute_inv_freq(self)`
- `_compute_cos_sin_cache(self, max_len)`
- `forward_native(self, positions, query, key)`
- `_apply_rotation(self, q, k, cos, sin)`

## Dependencies

**Imports** (6):
- `base.HAS_TORCH`
- `base.RotaryEmbeddingBase`
- `config.RoPEConfig`
- `torch`
- `typing.Any`
- `typing.Tuple`

---
*Auto-generated documentation*
