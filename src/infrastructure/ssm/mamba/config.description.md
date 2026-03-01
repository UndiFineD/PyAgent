# config

**File**: `src\infrastructure\ssm\mamba\config.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 95  
**Complexity**: 5 (moderate)

## Overview

Mamba Configuration and State Classes.

## Classes (3)

### `MambaConfig`

Configuration for Mamba mixer.

**Methods** (3):
- `__post_init__(self)`
- `d_inner(self)`
- `dt_rank(self)`

### `MambaState`

State for Mamba recurrence.

**Methods** (2):
- `zeros(cls, batch_size, config, dtype)`
- `clone(self)`

### `MambaOutput`

**Inherits from**: NamedTuple

Output from Mamba forward pass.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `math`
- `numpy`
- `typing.NamedTuple`

---
*Auto-generated documentation*
