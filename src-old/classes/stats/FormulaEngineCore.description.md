# FormulaEngineCore

**File**: `src\classes\stats\FormulaEngineCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 86  
**Complexity**: 4 (simple)

## Overview

FormulaEngineCore logic for PyAgent.
Pure logic for safe mathematical evaluation via AST.
No I/O or side effects.

## Classes (1)

### `FormulaEngineCore`

Pure logic core for formula calculations.

**Methods** (4):
- `__init__(self)`
- `_eval_node(self, node)`
- `calculate_logic(self, formula, variables)`
- `validate_logic(self, formula)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `ast`
- `operator`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
