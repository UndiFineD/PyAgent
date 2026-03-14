#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/LongTermMemory.description.md

# LongTermMemory

**File**: `src\\classes\agent\\LongTermMemory.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Long-term memory for agents using vector storage.

## Classes (1)

### `LongTermMemory`

Manages persistent conversational and factual memory for agents.

**Methods** (5):
- `__init__(self, collection_name, persist_directory)`
- `_init_db(self)`
- `store(self, content, metadata, tags)`
- `query(self, query_text, n_results, filter_tags)`
- `clear(self)`

## Dependencies

**Imports** (10):
- `chromadb`
- `chromadb.config.Settings`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/LongTermMemory.improvements.md

# Improvements for LongTermMemory

**File**: `src\\classes\agent\\LongTermMemory.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 112 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LongTermMemory_test.py` with pytest tests

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

r"""Long-term memory for agents using vector storage."""
