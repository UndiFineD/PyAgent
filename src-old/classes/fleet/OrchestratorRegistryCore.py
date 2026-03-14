r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/OrchestratorRegistryCore.description.md

# OrchestratorRegistryCore

**File**: `src\\classes\fleet\\OrchestratorRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for OrchestratorRegistryCore.

## Classes (1)

### `OrchestratorRegistryCore`

Pure logic core for Orchestrator Registry.
Handles dynamic discovery of orchestrator classes.

**Methods** (5):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `_to_snake_case(self, name)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `os`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/OrchestratorRegistryCore.improvements.md

# Improvements for OrchestratorRegistryCore

**File**: `src\\classes\fleet\\OrchestratorRegistryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 112 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OrchestratorRegistryCore_test.py` with pytest tests

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
