r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/ModelRegistryCore.description.md

# ModelRegistryCore

**File**: `src\\logic\agents\\system\\core\\ModelRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 68  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for ModelRegistryCore.

## Classes (1)

### `ModelRegistryCore`

ModelRegistryCore manages the PEFT (LoRA/QLoRA) adapter registry.
It maps request types to specific expert adapters.
Phase 289: Model Registry Self-Healing.

**Methods** (6):
- `__init__(self)`
- `self_heal(self)`
- `get_adapter_for_task(self, task_type)`
- `should_trigger_finetuning(self, quality_history, threshold)`
- `register_new_adapter(self, name, path)`
- `list_adapters(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/ModelRegistryCore.improvements.md

# Improvements for ModelRegistryCore

**File**: `src\\logic\agents\\system\\core\\ModelRegistryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ModelRegistryCore_test.py` with pytest tests

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
