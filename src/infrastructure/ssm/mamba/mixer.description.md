# mixer

**File**: `src\infrastructure\ssm\mamba\mixer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 10 imports  
**Lines**: 187  
**Complexity**: 6 (moderate)

## Overview

Mamba Mixer - Implementation of Mamba-1 and Mamba-2 mixer layers.

## Classes (2)

### `MambaMixer`

Mamba-1 Mixer layer.

**Methods** (5):
- `__init__(self, config)`
- `_silu(self, x)`
- `_rms_norm(self, x, weight)`
- `forward(self, hidden_states, state)`
- `step(self, hidden_states, state)`

### `Mamba2Mixer`

**Inherits from**: MambaMixer

Mamba-2 Mixer with multi-head SSM.

**Methods** (1):
- `__init__(self, config, num_heads)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `math`
- `numpy`
- `src.infrastructure.ssm.mamba.config.MambaConfig`
- `src.infrastructure.ssm.mamba.config.MambaOutput`
- `src.infrastructure.ssm.mamba.config.MambaState`
- `src.infrastructure.ssm.mamba.ops.CausalConv1d`
- `src.infrastructure.ssm.mamba.ops.SelectiveScan`
- `torch`
- `torch.nn.functional`

---
*Auto-generated documentation*
