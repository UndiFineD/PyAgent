#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/ReflectionAgent.description.md

# ReflectionAgent

**File**: `src\classes\specialized\ReflectionAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 26  
**Complexity**: 3 (simple)

## Overview

Agent specializing in self-critique and reflection.

## Classes (1)

### `ReflectionAgent`

**Inherits from**: BaseAgent

Critique and refinement engine.

**Methods** (3):
- `__init__(self, file_path)`
- `critique(self, work)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (3):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/ReflectionAgent.improvements.md

# Improvements for ReflectionAgent

**File**: `src\classes\specialized\ReflectionAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 26 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReflectionAgent_test.py` with pytest tests

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

r"""Agent specializing in self-critique and reflection."""
