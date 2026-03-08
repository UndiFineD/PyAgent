# ContextCompressor

**File**: `src\classes\context\ContextCompressor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 2 (simple)

## Overview

Shell for ContextCompressorCore, handling File I/O and orchestration.

## Classes (1)

### `ContextCompressor`

Reduces the size of source files while preserving structural context.

Acts as the I/O Shell for ContextCompressorCore.

**Methods** (2):
- `__init__(self, workspace_root)`
- `compress_file(self, file_path_raw)`

## Dependencies

**Imports** (7):
- `logging`
- `pathlib.Path`
- `src.classes.context.ContextCompressorCore.ContextCompressorCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
