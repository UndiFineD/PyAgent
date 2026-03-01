# writer

**File**: `src\infrastructure\tensorizer\core\writer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 163  
**Complexity**: 9 (moderate)

## Overview

Writer for tensorizer file format.

## Classes (1)

### `TensorizerWriter`

Writes tensors to a tensorizer file format.

Supports streaming writes, compression, and checksums.

**Methods** (9):
- `__init__(self, path, config)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `open(self)`
- `close(self)`
- `_write_header(self)`
- `_finalize(self)`
- `write_tensor(self, name, tensor)`
- `write_model(self, tensors, progress_callback)`

## Dependencies

**Imports** (17):
- `compression.compress_data`
- `config.DTYPE_MAP`
- `config.TENSORIZER_MAGIC`
- `config.TENSORIZER_VERSION`
- `config.TensorDtype`
- `config.TensorizerConfig`
- `hashlib`
- `metadata.TensorMetadata`
- `numpy`
- `pathlib.Path`
- `struct`
- `typing.BinaryIO`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
