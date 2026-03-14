#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/ToolRegistry.description.md

# ToolRegistry

**File**: `src\classes\orchestration\ToolRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 65  
**Complexity**: 5 (moderate)

## Overview

Central registry for all agent tools and capabilities.

## Classes (1)

### `ToolRegistry`

A registry that allows agents to discover and invoke tools across the fleet.
Shell for ToolCore.

**Methods** (5):
- `__new__(cls)`
- `register_tool(self, owner_name, func, category, priority)`
- `list_tools(self, category)`
- `get_tool(self, name)`
- `call_tool(self, name)`

## Dependencies

**Imports** (10):
- `ToolCore.ToolCore`
- `ToolCore.ToolMetadata`
- `inspect`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/ToolRegistry.improvements.md

# Improvements for ToolRegistry

**File**: `src\classes\orchestration\ToolRegistry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 65 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ToolRegistry_test.py` with pytest tests

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

r"""Central registry for all agent tools and capabilities."""
