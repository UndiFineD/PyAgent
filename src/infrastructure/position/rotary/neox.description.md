# neox

**File**: `src\infrastructure\position\rotary\neox.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 132  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for neox.

## Classes (1)

### `NeoxRotaryEmbedding`

**Inherits from**: RotaryEmbeddingBase

NeoX style rotary position embedding.

Rotates pairs of dimensions (0, d/2), (1, d/2+1), etc.
This is the standard implementation used in Llama, Mistral, and others.

**Methods** (6):
- `__init__(self, config)`
- `_compute_inv_freq(self)`
- `_compute_cos_sin_cache(self, max_len)`
- `forward_native(self, positions, query, key)`
- `_forward_torch(self, positions, query, key)`
- `_forward_numpy(self, positions, query, key)`

## Dependencies

**Imports** (8):
- `base.HAS_NUMPY`
- `base.HAS_TORCH`
- `base.RotaryEmbeddingBase`
- `config.RoPEConfig`
- `numpy`
- `torch`
- `typing.Any`
- `typing.Tuple`

---
*Auto-generated documentation*
