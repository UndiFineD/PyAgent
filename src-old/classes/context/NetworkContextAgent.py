#!/usr/bin/env python3

r"""
LLM_CONTEXT_START

## Source: src-old/classes/context/NetworkContextAgent.description.md

# NetworkContextAgent

**File**: `src\classes\context\NetworkContextAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 100  
**Complexity**: 4 (simple)

## Overview

Agent that maps the codebase into a graph of relationships.

## Classes (1)

### `NetworkContextAgent`

**Inherits from**: BaseAgent

Scans the codebase to build a graph of imports and class hierarchies.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_project(self)`
- `analyze_impact(self, file_path)`

## Dependencies

**Imports** (10):
- `GraphContextEngine.GraphContextEngine`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/NetworkContextAgent.improvements.md

# Improvements for NetworkContextAgent

**File**: `src\classes\context\NetworkContextAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 100 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NetworkContextAgent_test.py` with pytest tests

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

r"""Agent that maps the codebase into a graph of relationships."""
