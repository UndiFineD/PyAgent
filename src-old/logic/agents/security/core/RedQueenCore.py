r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/security/core/RedQueenCore.description.md

# RedQueenCore

**File**: `src\\logic\agents\\security\\core\\RedQueenCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for RedQueenCore.

## Classes (2)

### `AttackVector`

Class AttackVector implementation.

### `RedQueenCore`

Pure logic for the 'Digital Red Queen' adversarial evolution.
Generates and mutates prompts to test security guardrails.

**Methods** (3):
- `mutate_prompt(self, base_prompt, strategy)`
- `evaluate_bypass(self, response, forbidden_patterns)`
- `select_parent_attacks(self, archive, count)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `re`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/security/core/RedQueenCore.improvements.md

# Improvements for RedQueenCore

**File**: `src\\logic\agents\\security\\core\\RedQueenCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: AttackVector

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RedQueenCore_test.py` with pytest tests

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
