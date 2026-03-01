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
