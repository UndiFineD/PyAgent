# ContextCompressorCore

**File**: `src\classes\context\ContextCompressorCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 97  
**Complexity**: 5 (moderate)

## Overview

ContextCompressorCore logic for PyAgent.
Pure logic for reducing the size of source files while preserving structural context.
No I/O or side effects.

## Classes (1)

### `ContextCompressorCore`

Pure logic core for code and document compression.

**Methods** (5):
- `compress_python(content)`
- `regex_fallback_compress(content)`
- `summarize_markdown(content)`
- `get_summary_header(filename, mode)`
- `decide_compression_mode(filename)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `ast`
- `re`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
