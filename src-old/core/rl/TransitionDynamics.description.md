# TransitionDynamics

**File**: `src\core\rl\TransitionDynamics.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 12 imports  
**Lines**: 297  
**Complexity**: 19 (moderate)

## Overview

Python module containing implementation for TransitionDynamics.

## Classes (3)

### `TransitionRecord`

Records a single state transition with metadata.

### `StateActionStats`

Statistics for a state-action pair.

**Methods** (1):
- `avg_reward(self)`

### `TransitionDynamics`

Models the probability of moving from state S to S' given action A.
Supports empirical estimation, model learning, and uncertainty quantification.

**Methods** (18):
- `__init__(self, smoothing)`
- `state_space_size(self)`
- `action_space_size(self)`
- `transition_count(self)`
- `record_transition(self, state, action, next_state, reward, done)`
- `get_transition_probability(self, state, action, next_state)`
- `get_transition_distribution(self, state, action)`
- `predict_next_state(self, state, action)`
- `predict_expected_reward(self, state, action)`
- `get_reachable_states(self, state, depth)`
- ... and 8 more methods

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `math`
- `random`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
