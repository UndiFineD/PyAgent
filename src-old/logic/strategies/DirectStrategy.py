#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/logic/strategies/DirectStrategy.description.md

# DirectStrategy

**File**: `src\logic\strategies\DirectStrategy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 28  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for DirectStrategy.

## Classes (1)

### `DirectStrategy`

**Inherits from**: AgentStrategy

Standard Zero-Shot strategy: Prompt -> Response.

## Dependencies

**Imports** (8):
- `AgentStrategy.AgentStrategy`
- `__future__.annotations`
- `collections.abc.Callable`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/strategies/DirectStrategy.improvements.md

# Improvements for DirectStrategy

**File**: `src\logic\strategies\DirectStrategy.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 28 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DirectStrategy_test.py` with pytest tests

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
# Copyright 2026 PyAgent Authors
# Apache 2.0 License
from collections.abc import Callable

from src.core.base.version import VERSION

from .AgentStrategy import AgentStrategy

BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class DirectStrategy(AgentStrategy):
    """
    """
