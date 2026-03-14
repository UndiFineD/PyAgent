#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/ReasoningAgent.description.md

# ReasoningAgent

**File**: `src\classes\coder\ReasoningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 99  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in logical reasoning, chain-of-thought analysis, and problem decomposition.

## Classes (1)

### `ReasoningAgent`

**Inherits from**: BaseAgent

Analyzes complex problems and provides a logical blueprint before action.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze(self, problem, context)`
- `analyze_tot(self, problem)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/ReasoningAgent.improvements.md

# Improvements for ReasoningAgent

**File**: `src\classes\coder\ReasoningAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 99 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReasoningAgent_test.py` with pytest tests

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

r"""Agent specializing in logical reasoning, chain-of-thought analysis, and problem decomposition."""
