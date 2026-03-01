# utils

**File**: `src\infrastructure\tensorizer\core\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 10 imports  
**Lines**: 76  
**Complexity**: 3 (simple)

## Overview

Utility functions for tensorizer.

## Functions (3)

### `save_model(path, tensors, compression, verify)`

Convenience function to save a model.

Returns total bytes written.

### `load_model(path, parallel, verify)`

Convenience function to load a model.

### `get_model_info(path)`

Get information about a tensorizer file without loading tensors.

## Dependencies

**Imports** (10):
- `config.CompressionType`
- `config.TensorizerConfig`
- `numpy`
- `os`
- `pathlib.Path`
- `reader.TensorizerReader`
- `typing.Any`
- `typing.Dict`
- `typing.Union`
- `writer.TensorizerWriter`

---
*Auto-generated documentation*
