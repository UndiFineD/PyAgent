# goal_setting_core

**File**: `src\core\base\logic\core\goal_setting_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 13 imports  
**Lines**: 326  
**Complexity**: 5 (moderate)

## Overview

Goal Setting and Iterative Refinement Core

Implements goal-driven iterative improvement patterns for self-correcting agents.
Based on agentic design patterns with goal evaluation, iterative refinement, and
self-correction reasoning techniques.

## Classes (5)

### `GoalStatus`

**Inherits from**: str, Enum

Goal achievement status enumeration.

### `GoalPriority`

**Inherits from**: str, Enum

Goal priority levels.

### `Goal`

Represents a goal with evaluation criteria.

**Methods** (2):
- `is_achieved(self)`
- `should_continue_iteration(self)`

### `IterationResult`

Result of a single iteration.

### `GoalSettingCore`

**Inherits from**: BaseCore

Core for goal-driven iterative refinement and self-correction.

Implements patterns from agentic design patterns including:
- Goal setting with evaluation criteria
- Iterative refinement with feedback loops
- Self-correction reasoning
- Goal achievement tracking

**Methods** (3):
- `__init__(self)`
- `register_evaluation_function(self, goal_type, func)`
- `register_refinement_function(self, goal_type, func)`

## Dependencies

**Imports** (13):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
