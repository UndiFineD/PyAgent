# reader

**File**: `src\infrastructure\tensorizer\core\reader.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 23 imports  
**Lines**: 258  
**Complexity**: 17 (moderate)

## Overview

Reader for tensorizer file format.

## Classes (2)

### `LoadProgress`

Progress information for loading.

**Methods** (2):
- `tensor_progress(self)`
- `byte_progress(self)`

### `TensorizerReader`

Reads tensors from a tensorizer file format.

Supports memory-mapped access and parallel loading.

**Methods** (15):
- `__init__(self, path, config)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `open(self)`
- `close(self)`
- `_read_header(self)`
- `_read_metadata(self)`
- `tensor_names(self)`
- `num_tensors(self)`
- `get_metadata(self, name)`
- ... and 5 more methods

## Dependencies

**Imports** (23):
- `compression.decompress_data`
- `concurrent.futures.ThreadPoolExecutor`
- `config.CompressionType`
- `config.DTYPE_MAP`
- `config.TENSORIZER_MAGIC`
- `config.TENSORIZER_VERSION`
- `config.TensorizerConfig`
- `dataclasses.dataclass`
- `hashlib`
- `metadata.TensorMetadata`
- `mmap`
- `numpy`
- `pathlib.Path`
- `struct`
- `threading`
- ... and 8 more

---
*Auto-generated documentation*
