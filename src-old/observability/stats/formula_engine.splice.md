# Class Breakdown: formula_engine

**File**: `src\observability\stats\formula_engine.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FormulaValidation`

**Line**: 27  
**Methods**: 0

Result of a formula validation check.

[TIP] **Suggested split**: Move to `formulavalidation.py`

---

### 2. `FormulaEngineCore`

**Line**: 34  
**Inherits**: FormulaCore  
**Methods**: 2

Extended formula core for observability specific needs (e.g. AVG).

[TIP] **Suggested split**: Move to `formulaenginecore.py`

---

### 3. `FormulaEngine`

**Line**: 91  
**Methods**: 6

Processes metric formulas and calculations using safe AST evaluation.

[TIP] **Suggested split**: Move to `formulaengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
