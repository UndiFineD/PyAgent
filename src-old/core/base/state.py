r"""LLM_CONTEXT_START

## Source: src-old/core/base/state.description.md

# state

**File**: `src\\core\base\\state.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 129  
**Complexity**: 10 (moderate)

## Overview

State management for swarm agents.
Handles persistence of agent memory, history, and metadata.

## Classes (3)

### `EmergencyEventLog`

Phase 278: Ring buffer recording the last 10 filesystem actions for recovery.

**Methods** (3):
- `__init__(self, log_path)`
- `_load_buffer(self)`
- `record_action(self, action, details)`

### `StateTransaction`

Phase 267: Transactional context manager for agent file operations.

**Methods** (5):
- `__init__(self, target_files)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `commit(self)`
- `rollback(self)`

### `AgentStateManager`

Manages saving and loading agent state to/from disk.

**Methods** (2):
- `save_state(file_path, current_state, token_usage, state_data, history_len, path)`
- `load_state(file_path, path)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `collections`
- `json`
- `logging`
- `pathlib.Path`
- `shutil`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/state.improvements.md

# Improvements for state

**File**: `src\\core\base\\state.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 129 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `state_test.py` with pytest tests

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
