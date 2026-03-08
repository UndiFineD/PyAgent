# RegressionAgent

**File**: `src\logic\agents\specialists\RegressionAgent.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 16 imports  
**Lines**: 375  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for RegressionAgent.

## Classes (3)

### `RegressionType`

**Inherits from**: Enum

Class RegressionType implementation.

### `RegressionResult`

Stores regression analysis results.

### `RegressionAgent`

**Inherits from**: BaseAgent

Agent specializing in predicting continuous values and analyzing relationships
between variables (e.g., predicting code complexity growth, performance trends).

**Methods** (6):
- `__init__(self, file_path)`
- `_linear_regression(self, history, steps)`
- `_polynomial_regression(self, history, steps, degree)`
- `_exponential_regression(self, history, steps)`
- `_moving_average(self, history, steps, window)`
- `_rank(self, data)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `math`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
