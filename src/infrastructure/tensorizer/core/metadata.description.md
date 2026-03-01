# metadata

**File**: `src\infrastructure\tensorizer\core\metadata.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 100  
**Complexity**: 2 (simple)

## Overview

Metadata structure for serialized tensors.

## Classes (1)

### `TensorMetadata`

Metadata for a serialized tensor.

**Methods** (2):
- `to_bytes(self)`
- `from_bytes(cls, data, pos)`

## Dependencies

**Imports** (5):
- `config.CompressionType`
- `config.TensorDtype`
- `dataclasses.dataclass`
- `struct`
- `typing.Tuple`

---
*Auto-generated documentation*
