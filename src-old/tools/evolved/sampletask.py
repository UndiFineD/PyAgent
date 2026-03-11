"""LLM_CONTEXT_START

## Source: src-old/tools/evolved/sampletask.description.md

# sampletask

**File**: `src\tools\\evolved\\sampletask.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 13  
**Complexity**: 1 (simple)

## Overview

A sample automated GUI task.

## Functions (1)

### `sample_automated_task()`

Automated task from sample recording.

## Dependencies

**Imports** (3):
- `pyautogui`
- `src.classes.base_agent.utilities.as_tool`
- `src.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/tools/evolved/sampletask.improvements.md

# Improvements for sampletask

**File**: `src\tools\\evolved\\sampletask.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 13 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `sampletask_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""A sample automated GUI task."""

import pyautogui
from src.classes.base_agent.utilities import as_tool


@as_tool
def sample_automated_task() -> None:
    """Automated task from sample recording."""
    pyautogui.click(100, 200)
    pyautogui.press("a")
    pyautogui.press("enter")
    pyautogui.click(150, 250)
