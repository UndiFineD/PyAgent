# models

**File**: `src\infrastructure\pooling\models.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 11 imports  
**Lines**: 103  
**Complexity**: 4 (simple)

## Overview

Data models and Enums for the Pooling Engine.

## Classes (6)

### `PoolingTask`

**Inherits from**: Enum

Supported pooling tasks.

### `PoolingStrategy`

**Inherits from**: Enum

Pooling strategies for sequence representations.

### `PoolingConfig`

Configuration for pooling operations.

**Methods** (1):
- `with_dimension(self, dim)`

### `PoolingResult`

Result from pooling operation.

**Methods** (2):
- `shape(self)`
- `dimension(self)`

### `EmbeddingOutput`

Output for embedding tasks.

**Methods** (1):
- `to_list(self)`

### `ClassificationOutput`

Output for classification tasks.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
