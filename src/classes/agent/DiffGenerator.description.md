# DiffGenerator

**File**: `src\classes\agent\DiffGenerator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 178  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `DiffGenerator`

Generates diffs to preview changes before applying them.

Creates human - readable diffs in various formats to allow
users to review changes before they are applied.

Attributes:
    output_format: Default output format for diffs.
    context_lines: Number of context lines in diff.

**Methods** (4):
- `__init__(self, output_format, context_lines)`
- `generate_diff(self, file_path, original, modified)`
- `format_diff(self, diff_result, output_format)`
- `print_diff(self, diff_result)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `difflib`
- `pathlib.Path`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.core.base.models.DiffOutputFormat`
- `src.core.base.models.DiffResult`
- `sys`

---
*Auto-generated documentation*
