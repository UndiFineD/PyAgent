#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/run_pipeline_until_stable.description.md

# run_pipeline_until_stable

**File**: `src\tools\run_pipeline_until_stable.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 5 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `subprocess`
- `sys`
- `time`

---
*Auto-generated documentation*
## Source: src-old/tools/run_pipeline_until_stable.improvements.md

# Improvements for run_pipeline_until_stable

**File**: `src\tools\run_pipeline_until_stable.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_pipeline_until_stable_test.py` with pytest tests

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


"""Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RFP = ROOT / "src" / "tools" / "run_full_pipeline.py"
PY = sys.executable


def main() -> int:
    """
    """
