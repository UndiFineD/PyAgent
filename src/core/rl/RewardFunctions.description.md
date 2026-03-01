# RewardFunctions

**File**: `src\core\rl\RewardFunctions.py`  
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
