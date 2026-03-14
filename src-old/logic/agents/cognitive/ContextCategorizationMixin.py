#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/ContextCategorizationMixin.description.md

# ContextCategorizationMixin

**File**: `src\\logic\agents\\cognitive\\ContextCategorizationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 127  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for ContextCategorizationMixin.

## Classes (1)

### `ContextCategorizationMixin`

Categorization, priority, and metadata methods for ContextAgent.

**Methods** (10):
- `set_priority(self, priority)`
- `get_priority(self)`
- `calculate_priority_score(self)`
- `set_category(self, category)`
- `get_category(self)`
- `auto_categorize(self)`
- `set_metadata(self, key, value)`
- `get_metadata(self, key)`
- `get_all_metadata(self)`
- `export_metadata(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `json`
- `re`
- `src.logic.agents.cognitive.context.models.ContextPriority.ContextPriority`
- `src.logic.agents.cognitive.context.models.FileCategory.FileCategory`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/ContextCategorizationMixin.improvements.md

# Improvements for ContextCategorizationMixin

**File**: `src\\logic\agents\\cognitive\\ContextCategorizationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 127 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextCategorizationMixin_test.py` with pytest tests

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
from __future__ import annotations


import json

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
import re
from typing import Any

from src.logic.agents.cognitive.context.models.ContextPriority import ContextPriority
from src.logic.agents.cognitive.context.models.FileCategory import FileCategory


class ContextCategorizationMixin:
    """
    """
