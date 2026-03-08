# apply_ast_patches

**File**: `src\tools\apply_ast_patches.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 4 imports  
**Lines**: 141  
**Complexity**: 4 (simple)

## Overview

Apply unified-diff patches from .external/patches_ast to workspace files.

This script applies patches conservatively: it verifies context lines before applying
and backs up original files as `.bak` when a patch is applied.

## Functions (4)

### `parse_patch(patch_text)`

### `apply_hunks_to_source(orig_lines, hunks)`

### `apply_patch_file(patch_path)`

### `main()`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `pathlib.Path`
- `re`
- `sys`

---
*Auto-generated documentation*
