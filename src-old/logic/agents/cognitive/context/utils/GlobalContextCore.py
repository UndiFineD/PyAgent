r"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/utils/GlobalContextCore.description.md

# GlobalContextCore

**File**: `src\logic\agents\cognitive\context\utils\GlobalContextCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 85  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for GlobalContextCore.

## Classes (1)

### `GlobalContextCore`

Pure logic for GlobalContext.
Handles data merging, pruning, and summary formatting.
No I/O or direct disk access.

**Methods** (6):
- `partition_memory(self, memory, max_entries_per_shard)`
- `prepare_fact(self, key, value)`
- `prepare_insight(self, insight, source_agent)`
- `merge_entity_info(self, existing, new_attributes)`
- `prune_lessons(self, lessons, max_lessons)`
- `generate_markdown_summary(self, memory)`

## Dependencies

**Imports** (6):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `zlib`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/utils/GlobalContextCore.improvements.md

# Improvements for GlobalContextCore

**File**: `src\logic\agents\cognitive\context\utils\GlobalContextCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 85 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GlobalContextCore_test.py` with pytest tests

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
