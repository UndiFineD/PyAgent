#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/SecurityGuardAgent.description.md

# SecurityGuardAgent

**File**: `src\classes\coder\SecurityGuardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 123  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in security validation and safety checks.

## Classes (1)

### `SecurityGuardAgent`

**Inherits from**: BaseAgent

Protects the workspace by validating diffs and commands.

**Methods** (9):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_for_secrets(self, content)`
- `audit_command(self, command)`
- `validate_shell_script(self, script_content)`
- `scan_for_injection(self, content)`
- `generate_safety_report(self, task, code_changes, commands)`
- `detect_jailbreak(self, prompt)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `SecurityCore.SecurityCore`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/SecurityGuardAgent.improvements.md

# Improvements for SecurityGuardAgent

**File**: `src\classes\coder\SecurityGuardAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 123 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityGuardAgent_test.py` with pytest tests

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

r"""Agent specializing in security validation and safety checks."""
