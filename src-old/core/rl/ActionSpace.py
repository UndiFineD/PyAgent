#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/rl/ActionSpace.description.md

# ActionSpace

**File**: `src\\core\rl\\ActionSpace.py`  
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
## Source: src-old/core/rl/ActionSpace.improvements.md

# Improvements for ActionSpace

**File**: `src\\core\rl\\ActionSpace.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 120 lines (medium)  
**Complexity**: 21 score (complex)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ActionSpace_test.py` with pytest tests

### Code Organization
- [TIP] **6 classes in one file** - Consider splitting into separate modules

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Reinforcement Learning Action Space Definition - Phase 319 Enhanced
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np


@dataclass
class ActionMetadata:
    """Rich metadata for actions."""

    name: str
    description: str = ""
    cost: float = 0.0  # Resource cost of taking this action
    cooldown: float = 0.0  # Time before action can be repeated
    prerequisites: List[str] = field(default_factory=list)


class ActionSpace:
    """Defines the set of possible actions an agent can take."""

    def __init__(
        self,
        actions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, ActionMetadata]] = None,
    ):
        self.actions = actions or []
        self.metadata = metadata or {}
        self._action_history: List[Tuple[str, float]] = []
        self._cooldowns: Dict[str, float] = {}

    def sample(self) -> str:
        """Returns a random action from the space."""
        available = self.get_available_actions()
        return random.choice(available) if available else ""

    def contains(self, action: str) -> bool:
        """Checks if the action is valid."""
        return action in self.actions

    def get_available_actions(self, current_time: Optional[float] = None) -> List[str]:
        """Returns actions not on cooldown."""
        import time

        now = current_time or time.time()
        return [a for a in self.actions if self._cooldowns.get(a, 0) <= now]

    def record_action(self, action: str, timestamp: Optional[float] = None) -> None:
        """Records an action and applies cooldown."""
        import time

        now = timestamp or time.time()
        self._action_history.append((action, now))
        if action in self.metadata:
            self._cooldowns[action] = now + self.metadata[action].cooldown

    def get_action_stats(self) -> Dict[str, int]:
        """Returns frequency of each action."""
        stats = {a: 0 for a in self.actions}
        for action, _ in self._action_history:
            if action in stats:
                stats[action] += 1
        return stats

    def mask_actions(self, mask: List[bool]) -> List[str]:
        """Returns subset of actions based on boolean mask."""
        return [a for a, m in zip(self.actions, mask) if m]


class DiscreteActionSpace(ActionSpace):
    """Discrete action space (fixed set of choices)."""

    def __init__(self, n: int, action_names: Optional[List[str]] = None):
        names = action_names or [str(i) for i in range(n)]
        super().__init__(names)
        self.n = n

    def sample(self) -> str:
        """Returns a random action name."""
        return random.choice(self.actions) if self.actions else ""

    def action_to_index(self, action: str) -> int:
        """Returns index of the given action."""
        return self.actions.index(action) if action in self.actions else -1

    def index_to_action(self, index: int) -> str:
        """Returns action name for given index."""
        return self.actions[index] if 0 <= index < len(self.actions) else ""


class BoxActionSpace:
    """Continuous action space within bounds."""

    def __init__(
        self,
        low: Union[float, np.ndarray],
        high: Union[float, np.ndarray],
        shape: tuple,
        dtype=np.float32,
    ):
        """Defines a continuous action space with given bounds."""
        self.low = (
            np.full(shape, low, dtype=dtype)
            if np.isscalar(low)
            else np.array(low, dtype=dtype)
        )
        self.high = (
            np.full(shape, high, dtype=dtype)
            if np.isscalar(high)
            else np.array(high, dtype=dtype)
        )
        self.shape = shape
        self.dtype = dtype

    def sample(self) -> np.ndarray:
        """Returns a random action within bounds."""
        return np.random.uniform(self.low, self.high, self.shape).astype(self.dtype)

    def contains(self, action: np.ndarray) -> bool:
        """Checks if action is within bounds."""
        return bool(np.all(action >= self.low) and np.all(action <= self.high))

    def clip(self, action: np.ndarray) -> np.ndarray:
        """Clips action to valid bounds."""
        return np.clip(action, self.low, self.high)


class MultiDiscreteActionSpace:
    """Multiple discrete action spaces (e.g., for multi-headed agents)."""

    def __init__(self, nvec: List[int]):
        """Nvec specifies the number of discrete actions for each dimension."""
        self.nvec = np.array(nvec)
        self.shape = (len(nvec),)

    def sample(self) -> np.ndarray:
        """Returns a random action vector."""
        return np.array([random.randint(0, n - 1) for n in self.nvec])

    def contains(self, action: np.ndarray) -> bool:
        """Checks if action is within bounds."""
        return all(0 <= a < n for a, n in zip(action, self.nvec))


class DictActionSpace:
    """Hierarchical action space with named sub-spaces."""

    def __init__(self, spaces: Dict[str, ActionSpace]):
        self.spaces = spaces

    def sample(self) -> Dict[str, Any]:
        """Samples a random action from each sub-space."""
        return {k: v.sample() for k, v in self.spaces.items()}

    def contains(self, action: Dict[str, Any]) -> bool:
        """Checks if action is valid within each sub-space."""
        return all(
            self.spaces[k].contains(v) for k, v in action.items() if k in self.spaces
        )
