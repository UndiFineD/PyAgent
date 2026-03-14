r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/mixins/MapBuilderMixin.description.md

# MapBuilderMixin

**File**: `src\\logic\agents\\system\\mixins\\MapBuilderMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for MapBuilderMixin.

## Classes (1)

### `MapBuilderMixin`

Mixin for mapping and parsing code entities in TopologicalNavigator.

**Methods** (3):
- `_get_entity_id(self, file_path, entity_name)`
- `build_dependency_map(self, target_dir)`
- `_parse_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `ast`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.system.TopologicalNavigator.TopologicalNavigator`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/mixins/MapBuilderMixin.improvements.md

# Improvements for MapBuilderMixin

**File**: `src\\logic\agents\\system\\mixins\\MapBuilderMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MapBuilderMixin_test.py` with pytest tests

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
