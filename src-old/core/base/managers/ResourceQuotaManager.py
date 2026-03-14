r"""LLM_CONTEXT_START

## Source: src-old/core/base/managers/ResourceQuotaManager.description.md

# ResourceQuotaManager

**File**: `src\\core\base\\managers\\ResourceQuotaManager.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 88  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for ResourceQuotaManager.

## Classes (3)

### `QuotaConfig`

Configuration for agent resource quotas.

### `ResourceUsage`

Current resource usage for an agent session.

**Methods** (2):
- `total_tokens(self)`
- `elapsed_time(self)`

### `ResourceQuotaManager`

Manages resource quotas and budget enforcement for agent sessions.

Phase 245: RESOURCE QUOTAS & BUDGETS

**Methods** (6):
- `__init__(self, config)`
- `update_usage(self, tokens_input, tokens_output, cycles)`
- `check_quotas(self)`
- `is_interrupted(self)`
- `interrupt_reason(self)`
- `get_report(self)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/ResourceQuotaManager.improvements.md

# Improvements for ResourceQuotaManager

**File**: `src\\core\base\\managers\\ResourceQuotaManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 88 lines (small)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResourceQuotaManager_test.py` with pytest tests

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
