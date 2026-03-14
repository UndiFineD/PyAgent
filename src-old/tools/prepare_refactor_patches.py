#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/prepare_refactor_patches.description.md

# prepare_refactor_patches

**File**: `src\tools\\prepare_refactor_patches.py`  
**Type**: Python Module  
**Summary**: 0 classes, 7 functions, 6 imports  
**Lines**: 132  
**Complexity**: 7 (moderate)

## Overview

Generate prioritized bandit report and prepare AST-based refactor patch proposals.

Produces:
- .external/static_checks/bandit_report.md  (summary, prioritized)
- .external/patches/<sanitized_filename>.patch  (human-review patch proposals)

This script does NOT apply patches; it only writes suggestions for reviewers.

## Functions (7)

### `sanitize_name(p)`

### `load_bandit()`

### `aggregate(results)`

### `make_report(agg, top_n)`

### `create_patch_proposal(filename, findings)`

### `suggest_replacement(line)`

### `main()`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `ast`
- `json`
- `pathlib.Path`
- `re`
- `shutil`

---
*Auto-generated documentation*
## Source: src-old/tools/prepare_refactor_patches.improvements.md

# Improvements for prepare_refactor_patches

**File**: `src\tools\\prepare_refactor_patches.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 132 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `prepare_refactor_patches_test.py` with pytest tests

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


r"""Generate prioritized bandit report and prepare AST-based refactor patch proposals.

Produces:
- .external/static_checks/bandit_report.md  (summary, prioritized)
- .external/patches/<sanitized_filename>.patch  (human-review patch proposals)

This script does NOT apply patches; it only writes suggestions for reviewers.
"""
