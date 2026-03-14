#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/move_external_to_src.description.md

# move_external_to_src

**File**: `src\tools\\move_external_to_src.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 6 imports  
**Lines**: 55  
**Complexity**: 0 (simple)

## Overview

Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `os`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/move_external_to_src.improvements.md

# Improvements for move_external_to_src

**File**: `src\tools\\move_external_to_src.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 55 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `move_external_to_src_test.py` with pytest tests

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


"""Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.
"""
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = ROOT / "src" / "external_candidates"
SRC_TOP = ROOT / "external_candidates"


def main() -> int:
    """
    """
