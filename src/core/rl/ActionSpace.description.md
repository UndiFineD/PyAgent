# ActionSpace

**File**: `src\core\rl\ActionSpace.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 12 imports  
**Lines**: 120  
**Complexity**: 21 (complex)

## Overview

Python module containing implementation for ActionSpace.

## Classes (6)

### `ActionMetadata`

Rich metadata for actions.

### `ActionSpace`

Defines the set of possible actions an agent can take.

**Methods** (7):
- `__init__(self, actions, metadata)`
- `sample(self)`
- `contains(self, action)`
- `get_available_actions(self, current_time)`
- `record_action(self, action, timestamp)`
- `get_action_stats(self)`
- `mask_actions(self, mask)`

### `DiscreteActionSpace`

**Inherits from**: ActionSpace

Discrete action space (fixed set of choices).

**Methods** (4):
- `__init__(self, n, action_names)`
- `sample(self)`
- `action_to_index(self, action)`
- `index_to_action(self, index)`

### `BoxActionSpace`

Continuous action space within bounds.

**Methods** (4):
- `__init__(self, low, high, shape, dtype)`
- `sample(self)`
- `contains(self, action)`
- `clip(self, action)`

### `MultiDiscreteActionSpace`

Multiple discrete action spaces (e.g., for multi-headed agents).

**Methods** (3):
- `__init__(self, nvec)`
- `sample(self)`
- `contains(self, action)`

### `DictActionSpace`

Hierarchical action space with named sub-spaces.

**Methods** (3):
- `__init__(self, spaces)`
- `sample(self)`
- `contains(self, action)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `numpy`
- `random`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
