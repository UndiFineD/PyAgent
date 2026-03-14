#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/LintingAgent.description.md

# LintingAgent

**File**: `src\classes\coder\LintingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in code quality, linting, and style enforcement.

## Classes (1)

### `LintingAgent`

**Inherits from**: BaseAgent

Ensures code adheres to quality standards by running linters.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `run_flake8(self, target_path)`
- `run_mypy(self, target_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/LintingAgent.improvements.md

# Improvements for LintingAgent

**File**: `src\classes\coder\LintingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LintingAgent_test.py` with pytest tests

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

r"""Agent specializing in code quality, linting, and style enforcement."""
