r"""LLM_CONTEXT_START

## Source: src-old/core/base/registry.description.md

# registry

**File**: `src\\core\base\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 6 (moderate)

## Overview

AgentRegistry: Central registry for all active agent instances.
Provides discovery and cross-agent communication.

## Classes (1)

### `AgentRegistry`

Singleton registry to track all active agents.

**Methods** (6):
- `__new__(cls)`
- `register(self, agent)`
- `unregister(self, name)`
- `get_agent(self, name)`
- `list_agents(self)`
- `active_count(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/core/base/registry.improvements.md

# Improvements for registry

**File**: `src\\core\base\registry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `registry_test.py` with pytest tests

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
