# models

**File**: `src\infrastructure\execution\batch\models.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 11 imports  
**Lines**: 130  
**Complexity**: 5 (moderate)

## Overview

Data models for batch orchestration.

## Classes (5)

### `MoveDirectionality`

**Inherits from**: Enum

Direction of request movement in batch.

### `CachedRequestState`

Per-request state cache matching vLLM's CachedRequestState.

**Methods** (1):
- `num_tokens(self)`

### `BatchUpdateBuilder`

Tracks request movements within a batch for logits processors.

**Methods** (4):
- `reset(self)`
- `record_swap(self, i1, i2)`
- `record_add(self, req_id, index)`
- `record_remove(self, req_id, index)`

### `SamplingMetadata`

GPU-resident sampling parameters for a batch.

### `InputBatch`

Complete batch representation for model execution.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
