# types

**File**: `src\infrastructure\kv_transfer\arc\types.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 8 imports  
**Lines**: 79  
**Complexity**: 2 (simple)

## Overview

Phase 45: ARC Offload Types
Data structures and enums for ARC offloading.

## Classes (6)

### `OffloadMedium`

**Inherits from**: Enum

Storage medium for offloaded blocks.

### `BlockState`

**Inherits from**: Enum

State of an offloaded block.

### `BlockStatus`

Status of a cached block.

**Methods** (2):
- `is_ready(self)`
- `can_evict(self)`

### `LoadStoreSpec`

Specification for load/store operation.

### `OffloadingEvent`

Event representing offloading operation.

### `PrepareStoreOutput`

Output from prepare_store operation.

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.List`
- `typing.Union`

---
*Auto-generated documentation*
