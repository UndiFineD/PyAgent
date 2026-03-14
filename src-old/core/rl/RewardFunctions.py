r"""LLM_CONTEXT_START

## Source: src-old/core/rl/RewardFunctions.description.md

# RewardFunctions

**File**: `src\\core\rl\\RewardFunctions.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 9 imports  
**Lines**: 124  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for RewardFunctions.

## Classes (5)

### `RewardType`

**Inherits from**: Enum

Class RewardType implementation.

### `RewardSignal`

Structured reward with metadata.

### `RewardFunctions`

Library of standard reward functions for agentic behavior.

**Methods** (8):
- `binary_reward(success, positive, negative)`
- `complexity_reduction_reward(old_complexity, new_complexity, scale)`
- `test_coverage_reward(old_coverage, new_coverage, scale)`
- `latency_penalty(latency_s, threshold_s, max_penalty)`
- `curiosity_reward(state_novelty, scale)`
- `goal_proximity_reward(current_dist, prev_dist, goal_bonus)`
- `consistency_reward(predictions, ground_truth, scale)`
- `resource_efficiency_reward(resources_used, budget, scale)`

### `CompositeRewardFunction`

Combines multiple reward functions with weights.

**Methods** (3):
- `__init__(self)`
- `add(self, name, fn, weight)`
- `compute(self)`

### `RewardShaper`

Applies potential-based reward shaping to avoid changing optimal policy.

**Methods** (2):
- `__init__(self, potential_fn, gamma)`
- `shape(self, reward, state, next_state)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `enum.Enum`
- `math`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/rl/RewardFunctions.improvements.md

# Improvements for RewardFunctions

**File**: `src\\core\rl\\RewardFunctions.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 124 lines (medium)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: RewardType

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RewardFunctions_test.py` with pytest tests

### Code Organization
- [TIP] **5 classes in one file** - Consider splitting into separate modules

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
