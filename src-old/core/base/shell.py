r"""LLM_CONTEXT_START

## Source: src-old/core/base/shell.description.md

# shell

**File**: `src\\core\base\\shell.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 175  
**Complexity**: 2 (simple)

## Overview

Shell execution core for agents.
Handles subprocess spawning, environment propagation, and interaction recording.

## Classes (2)

### `EnvironmentSanitizer`

Filters environment variables to prevent secret leakage (Phase 266).

**Methods** (1):
- `sanitize(cls, env)`

### `ShellExecutor`

Safely executes shell commands and records outcomes.

**Methods** (1):
- `run_command(cmd, workspace_root, agent_name, models_config, recorder, timeout, max_retries)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `os`
- `src.core.base.sandbox.SandboxManager`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/shell.improvements.md

# Improvements for shell

**File**: `src\\core\base\\shell.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 175 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `shell_test.py` with pytest tests

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
