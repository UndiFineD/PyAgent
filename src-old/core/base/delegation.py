r"""LLM_CONTEXT_START

## Source: src-old/core/base/delegation.description.md

# delegation

**File**: `src\\core\base\\delegation.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 101  
**Complexity**: 1 (simple)

## Overview

Delegation management for agent cascading.
Enables agents to launch sub-tasks by spawning other specialized agents.

## Classes (1)

### `AgentDelegator`

Handles cascading sub-tasks to other agents.

**Methods** (1):
- `delegate(agent_type, prompt, current_agent_name, current_file_path, current_model, target_file, context, priority)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `importlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.CascadeContext`
- `src.core.base.registry.AgentRegistry`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/delegation.improvements.md

# Improvements for delegation

**File**: `src\\core\base\\delegation.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `delegation_test.py` with pytest tests

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
