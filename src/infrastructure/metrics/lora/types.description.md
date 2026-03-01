# types

**File**: `src\infrastructure\metrics\lora\types.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 9 imports  
**Lines**: 127  
**Complexity**: 5 (moderate)

## Overview

LoRA Stats Types - Enums and DataClasses for LoRA adapter tracking.

## Classes (5)

### `LoRALoadState`

**Inherits from**: Enum

State of a LoRA adapter.

### `RequestStatus`

**Inherits from**: Enum

Status of a request in the system.

### `LoRAAdapterInfo`

Information about a LoRA adapter.

**Methods** (1):
- `mark_used(self)`

### `LoRARequestState`

State of a LoRA request.

Tracks per-request LoRA adapter usage and timing.

**Methods** (4):
- `load_latency(self)`
- `queue_latency(self)`
- `execution_latency(self)`
- `total_latency(self)`

### `LoRAStats`

Aggregate statistics for LoRA operations.

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Dict`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
