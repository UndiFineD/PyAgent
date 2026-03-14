#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/move_completed.description.md

# move_completed

**File**: `src\tools\\move_completed.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 3 imports  
**Lines**: 94  
**Complexity**: 3 (simple)

## Overview

Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.

## Functions (3)

### `parse_row(line)`

### `is_completed_status(s)`

### `main()`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `datetime`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/tools/move_completed.improvements.md

# Improvements for move_completed

**File**: `src\tools\\move_completed.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 94 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `move_completed_test.py` with pytest tests

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


r"""Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.
"""
