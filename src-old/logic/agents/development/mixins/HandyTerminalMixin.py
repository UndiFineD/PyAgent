r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/HandyTerminalMixin.description.md

# HandyTerminalMixin

**File**: `src\\logic\agents\\development\\mixins\\HandyTerminalMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 83  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for HandyTerminalMixin.

## Classes (1)

### `HandyTerminalMixin`

Mixin for terminal execution and slash command handling in HandyAgent.

**Methods** (2):
- `terminal_slash_command(self, command, args)`
- `execute_with_diagnosis(self, command)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `shlex`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.development.HandyAgent.HandyAgent`
- `subprocess`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/HandyTerminalMixin.improvements.md

# Improvements for HandyTerminalMixin

**File**: `src\\logic\agents\\development\\mixins\\HandyTerminalMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 83 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HandyTerminalMixin_test.py` with pytest tests

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
