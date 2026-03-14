#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/run_auto_tests.description.md

# run_auto_tests

**File**: `src\tools\run_auto_tests.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 7 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.

## Functions (2)

### `_run_file(path_str)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `argparse`
- `concurrent.futures`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/run_auto_tests.improvements.md

# Improvements for run_auto_tests

**File**: `src\tools\run_auto_tests.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_auto_tests_test.py` with pytest tests

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


r"""Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.
"""
