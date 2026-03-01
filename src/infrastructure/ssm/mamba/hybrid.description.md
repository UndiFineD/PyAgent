# hybrid

**File**: `src\infrastructure\ssm\mamba\hybrid.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 101  
**Complexity**: 2 (simple)

## Overview

Hybrid Mamba Mixer - Combining SSM with Attention.

## Classes (1)

### `HybridMambaMixer`

Hybrid layer combining Mamba SSM with attention.

**Methods** (2):
- `__init__(self, config, num_attention_heads, attention_ratio)`
- `forward(self, hidden_states, state)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `math`
- `numpy`
- `src.infrastructure.ssm.mamba.config.MambaConfig`
- `src.infrastructure.ssm.mamba.config.MambaOutput`
- `src.infrastructure.ssm.mamba.config.MambaState`
- `src.infrastructure.ssm.mamba.mixer.MambaMixer`

---
*Auto-generated documentation*
