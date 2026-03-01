# dynamic

**File**: `src\infrastructure\position\rotary\dynamic.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 105  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for dynamic.

## Classes (1)

### `XDRotaryEmbedding`

**Inherits from**: RotaryEmbeddingBase

Extended Dynamic Rotary Position Embedding.

Implements dynamic NTK-aware scaling for extended context lengths.

**Methods** (5):
- `__init__(self, config)`
- `_compute_inv_freq(self, base)`
- `_compute_dynamic_base(self, seq_len)`
- `_compute_cos_sin_cache(self, max_len)`
- `forward_native(self, positions, query, key)`

## Dependencies

**Imports** (9):
- `base.HAS_NUMPY`
- `base.HAS_TORCH`
- `base.RotaryEmbeddingBase`
- `config.RoPEConfig`
- `numpy`
- `torch`
- `typing.Any`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
