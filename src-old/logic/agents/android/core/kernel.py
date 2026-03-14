r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/android/core/kernel.description.md

# kernel

**File**: `src\\logic\agents\android\\core\\kernel.py`  
**Type**: Python Module  
**Summary**: 0 classes, 5 functions, 8 imports  
**Lines**: 131  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for kernel.

## Functions (5)

### `run_adb_command(command)`

Executes a shell command via ADB.

### `get_screen_state()`

Dumps the current UI XML and returns the sanitized JSON string.

### `execute_action(action)`

Executes the action decided by the LLM.

### `get_llm_decision(goal, screen_context)`

Sends screen context to LLM and asks for the next move.

### `run_agent(goal, max_steps)`

## Dependencies

**Imports** (8):
- `json`
- `openai.OpenAI`
- `os`
- `sanitizer`
- `subprocess`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/android/core/kernel.improvements.md

# Improvements for kernel

**File**: `src\\logic\agents\android\\core\\kernel.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `kernel_test.py` with pytest tests

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
