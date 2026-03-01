# engine

**File**: `src\infrastructure\position\rotary\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 14 imports  
**Lines**: 122  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (1)

### `RotaryEmbeddingEngine`

Unified engine for rotary position embeddings.

Provides automatic variant detection and unified interface
for all RoPE implementations.

**Methods** (7):
- `__init__(self, config)`
- `_get_or_create_embedding(self, variant)`
- `set_variant(self, variant)`
- `embedding(self)`
- `forward(self, positions, query, key, use_cuda)`
- `from_model_config(cls, model_config)`
- `list_variants(cls)`

## Functions (1)

### `create_rope_embedding(head_dim, max_position, base, variant)`

Create a RoPE embedding instance.

## Dependencies

**Imports** (14):
- `base.RotaryEmbeddingBase`
- `config.RoPEConfig`
- `config.RoPEScalingType`
- `config.RoPEVariant`
- `dynamic.XDRotaryEmbedding`
- `gptj.GptJRotaryEmbedding`
- `multimodal.MRotaryEmbedding`
- `neox.NeoxRotaryEmbedding`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
