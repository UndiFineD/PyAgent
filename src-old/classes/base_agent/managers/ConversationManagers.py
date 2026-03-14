#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/ConversationManagers.description.md

# ConversationManagers

**File**: `src\\classes\base_agent\\managers\\ConversationManagers.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 27  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ConversationManagers.

## Classes (1)

### `ConversationHistory`

Manages a conversation history with message storage and retrieval.

**Methods** (4):
- `__init__(self, max_messages)`
- `add(self, role, content)`
- `get_context(self)`
- `clear(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `models.ConversationMessage`
- `models.MessageRole`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers/ConversationManagers.improvements.md

# Improvements for ConversationManagers

**File**: `src\\classes\base_agent\\managers\\ConversationManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 27 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConversationManagers_test.py` with pytest tests

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


# Copyright (c) 2025 PyAgent contributors
from typing import List

from ..models import ConversationMessage, MessageRole


class ConversationHistory:
    """
    """
