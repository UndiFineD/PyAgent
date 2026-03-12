#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/FormulaEngine.description.md

# FormulaEngine

**File**: `src\classes\stats\FormulaEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 51  
**Complexity**: 6 (moderate)

## Overview

Shell for FormulaEngine using pure core logic.

## Classes (1)

### `FormulaEngine`

Processes metric formulas and calculations using safe AST evaluation.

Acts as the I/O Shell for FormulaEngineCore.

**Methods** (6):
- `__init__(self)`
- `define(self, name, formula)`
- `define_formula(self, name, formula)`
- `calculate(self, formula_or_name, variables)`
- `validate(self, formula)`
- `validate_formula(self, formula)`

## Dependencies

**Imports** (8):
- `FormulaEngineCore.FormulaEngineCore`
- `FormulaValidation.FormulaValidation`
- `__future__.annotations`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/stats/FormulaEngine.improvements.md

# Improvements for FormulaEngine

**File**: `src\classes\stats\FormulaEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 51 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FormulaEngine_test.py` with pytest tests

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

from __future__ import annotations

"""Shell for FormulaEngine using pure core logic."""

import logging
from typing import Any, Dict, List, Optional
from .FormulaValidation import FormulaValidation
from .FormulaEngineCore import FormulaEngineCore


class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation.

    Acts as the I/O Shell for FormulaEngineCore.
    """

    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        """Define a formula."""
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        """Define a formula (backward compat)."""
        self.define(name, formula)

    def calculate(
        self, formula_or_name: str, variables: Optional[Dict[str, Any]] = None
    ) -> float:
        """Calculate formula result via Core."""
        variables = variables or {}

        # If formula_or_name is in formulas dict, use stored formula
        formula = self.formulas.get(formula_or_name, formula_or_name)

        try:
            return self.core.calculate_logic(formula, variables)
        except Exception as e:
            logging.error(f"Formula calculation failed: {e}")
            return 0.0

    def validate(self, formula: str) -> FormulaValidation:
        """Validate formula syntax via Core."""
        result = self.core.validate_logic(formula)
        return FormulaValidation(is_valid=result["is_valid"], error=result["error"])

    def validate_formula(self, formula: str) -> bool:
        """Validate formula syntax (backward compat)."""
        return self.validate(formula).is_valid
