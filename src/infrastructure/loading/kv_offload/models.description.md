# models

**File**: `src\infrastructure\loading\kv_offload\models.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 10 imports  
**Lines**: 66  
**Complexity**: 2 (simple)

## Overview

Models and configurations for KV offloading.

## Classes (5)

### `OffloadMedium`

**Inherits from**: Enum

Storage medium types for offloading.

### `LoadStoreSpec`

Specification for load/store operations.

**Methods** (1):
- `num_blocks(self)`

### `BlockStatus`

Status of an offloaded block.

**Methods** (1):
- `is_pinned(self)`

### `OffloadingEvent`

Event for block offloading operations.

### `PrepareStoreOutput`

Output from prepare_store operation.

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
