# ContextCompressor

**File**: `src\logic\agents\cognitive\context\utils\ContextCompressor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 82  
**Complexity**: 4 (simple)

## Overview

Engine for compressing large code files into summarized signatures.

## Classes (1)

### `ContextCompressor`

Reduces the size of source files while preserving structural context.

This is useful for fitting large codebases into constrained LLM context windows.

**Methods** (4):
- `__init__(self, workspace_root)`
- `compress_python(self, content)`
- `summarize_markdown(self, content)`
- `compress_file(self, file_path)`

## Dependencies

**Imports** (8):
- `ast`
- `logging`
- `pathlib.Path`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
