#!/usr/bin/env python3

r"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/utils/GraphContextEngine.description.md

# GraphContextEngine

**File**: `src\logic\agents\cognitive\context\utils\GraphContextEngine.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 150  
**Complexity**: 11 (moderate)

## Overview

Core engine for managing code relationships as a graph.

## Classes (2)

### `CodeGraphVisitor`

**Inherits from**: NodeVisitor

AST visitor to extract imports, classes, and function calls.

**Methods** (5):
- `__init__(self, file_path)`
- `visit_Import(self, node)`
- `visit_ImportFrom(self, node)`
- `visit_ClassDef(self, node)`
- `visit_Call(self, node)`

### `GraphContextEngine`

Manages an adjacency list of file and class dependencies.

**Methods** (6):
- `__init__(self, workspace_root)`
- `add_edge(self, source, target, relationship)`
- `scan_project(self, start_path)`
- `get_impact_radius(self, node, max_depth)`
- `save(self)`
- `load(self)`

## Dependencies

**Imports** (11):
- `ast`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/utils/GraphContextEngine.improvements.md

# Improvements for GraphContextEngine

**File**: `src\logic\agents\cognitive\context\utils\GraphContextEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 150 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GraphContextEngine_test.py` with pytest tests

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

r"""Core engine for managing code relationships as a graph."""
