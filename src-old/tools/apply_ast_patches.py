#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/apply_ast_patches.description.md

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
## Source: src-old/tools/apply_ast_patches.improvements.md

# Improvements for apply_ast_patches

**File**: `src\tools\apply_ast_patches.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 141 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `apply_ast_patches_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""
from __future__ import annotations


r"""Apply unified-diff patches from .external/patches_ast to workspace files.

This script applies patches conservatively: it verifies context lines before applying
and backs up original files as `.bak` when a patch is applied.
"""
