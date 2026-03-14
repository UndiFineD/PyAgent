#!/usr/bin/env python3
# Knowledge Mixin for BaseAgent
r"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/KnowledgeMixin.description.md

# KnowledgeMixin

**File**: `src\\core\base\\mixins\\KnowledgeMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 87  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for KnowledgeMixin.

## Classes (1)

### `KnowledgeMixin`

Handles knowledge engines, memory, sharded storage, and templates.

**Methods** (12):
- `__init__(self, agent_name, workspace_root)`
- `take_note(self, content)`
- `get_notes(self)`
- `clear_notes(self)`
- `register_template(self, name, template)`
- `get_template(self, name)`
- `add_to_history(self, role, content)`
- `clear_history(self)`
- `get_history(self)`
- `_build_prompt_with_history(self, prompt)`
- ... and 2 more methods

## Dependencies

**Imports** (6):
- `pathlib.Path`
- `src.core.base.ShardedKnowledgeCore.ShardedKnowledgeCore`
- `src.core.knowledge.knowledge_engine.KnowledgeEngine`
- `src.logic.agents.cognitive.LongTermMemory.LongTermMemory`
- `src.logic.agents.cognitive.context.engines.GlobalContextEngine.GlobalContextEngine`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/KnowledgeMixin.improvements.md

# Improvements for KnowledgeMixin

**File**: `src\\core\base\\mixins\\KnowledgeMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 87 lines (small)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeMixin_test.py` with pytest tests

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
from pathlib import Path
from typing import Any

from src.core.base.ShardedKnowledgeCore import ShardedKnowledgeCore


class KnowledgeMixin:
    """
    """
