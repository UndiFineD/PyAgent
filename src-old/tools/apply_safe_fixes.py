#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/apply_safe_fixes.description.md

# apply_safe_fixes

**File**: `src\tools\apply_safe_fixes.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 9 imports  
**Lines**: 146  
**Complexity**: 6 (moderate)

## Overview

Apply safe, automated fixes over extracted candidate files.

Currently implements:
- Replace `yaml.load(` -> `yaml.safe_load(`
- Replace `from yaml import load` -> `from yaml import safe_load as load`

Writes unified diff patches to `.external/patches/` and optionally applies changes when
`--apply` is passed. Re-runs static checks and generated tests after applying fixes.

## Functions (6)

### `find_py_files(target)`

### `transform_text(text)`

### `remove_top_level_asserts(text)`

### `write_patch(orig_path, orig_text, new_text, patch_dir, base_dir)`

### `apply_fixes(apply, target_dir, patch_dir)`

### `main(argv)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `argparse`
- `ast`
- `difflib`
- `pathlib.Path`
- `re`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/apply_safe_fixes.improvements.md

# Improvements for apply_safe_fixes

**File**: `src\tools\apply_safe_fixes.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 146 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `apply_safe_fixes_test.py` with pytest tests

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


r"""Apply safe, automated fixes over extracted candidate files.

Currently implements:
- Replace `yaml.load(` -> `yaml.safe_load(`
- Replace `from yaml import load` -> `from yaml import safe_load as load`

Writes unified diff patches to `.external/patches/` and optionally applies changes when
`--apply` is passed. Re-runs static checks and generated tests after applying fixes.
"""
