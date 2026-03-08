# LearningObjectives

**File**: `src\core\rl\LearningObjectives.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 11 imports  
**Lines**: 277  
**Complexity**: 18 (moderate)

## Overview

Python module containing implementation for LearningObjectives.

## Classes (5)

### `ObjectiveStatus`

**Inherits from**: Enum

Class ObjectiveStatus implementation.

### `ObjectiveType`

**Inherits from**: Enum

Class ObjectiveType implementation.

### `LearningObjective`

Represents a learning objective with tracking and evaluation.

**Methods** (3):
- `progress(self)`
- `is_achieved(self)`
- `update(self, new_value)`

### `ObjectiveConstraint`

Defines a constraint that must be satisfied.

**Methods** (1):
- `is_satisfied(self, value)`

### `ObjectiveTracker`

Manages high-level goals for the self-improving fleet.

**Methods** (14):
- `__init__(self)`
- `_recalculate_weights(self)`
- `add_objective(self, objective)`
- `remove_objective(self, name)`
- `update_objective(self, name, new_value)`
- `update_metric(self, metric, value)`
- `get_progress(self)`
- `get_priority_objective(self)`
- `get_bottleneck(self)`
- `check_constraints(self, metrics)`
- ... and 4 more methods

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `math`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
