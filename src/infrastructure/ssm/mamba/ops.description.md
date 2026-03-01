# ops

**File**: `src\infrastructure\ssm\mamba\ops.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 155  
**Complexity**: 6 (moderate)

## Overview

Mamba Operations - Causal Convolution and Selective Scan.

## Classes (2)

### `CausalConv1d`

Causal 1D convolution layer.

**Methods** (3):
- `__init__(self, in_channels, kernel_size, bias)`
- `forward(self, x, conv_state)`
- `update(self, x, conv_state)`

### `SelectiveScan`

Selective scan operation for Mamba.

**Methods** (3):
- `__init__(self, d_inner, ssm_state_size)`
- `forward(self, x, dt, B, C, ssm_state)`
- `update(self, x, dt, B, C, ssm_state)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `math`
- `numpy`

---
*Auto-generated documentation*
