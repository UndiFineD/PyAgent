# base

**File**: `src\infrastructure\position\rotary\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 67  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for base.

## Classes (1)

### `RotaryEmbeddingBase`

**Inherits from**: ABC

Base class for all RoPE implementations.

**Methods** (5):
- `__init__(self, config)`
- `forward_native(self, positions, query, key)`
- `forward(self, positions, query, key, use_cuda)`
- `_ensure_cache(self, seq_len)`
- `_compute_cos_sin_cache(self, max_len)`

## Dependencies

**Imports** (16):
- `abc.ABC`
- `abc.abstractmethod`
- `config.RoPEConfig`
- `config.RoPEVariant`
- `math`
- `numpy`
- `os`
- `torch`
- `torch.nn`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- ... and 1 more

---
*Auto-generated documentation*
