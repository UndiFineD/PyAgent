
"""
Action space.py module.
"""
# Copyright 2026 PyAgent Authors
# Reinforcement Learning Action Space Definition - Phase 319 Enhanced

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import numpy as np


@dataclass
class ActionMetadata:
    """Rich metadata for actions."""

    name: str
    description: str = ""
    cost: float = 0.0  # Resource cost of taking this action
    cooldown: float = 0.0  # Time before action can be repeated
    prerequisites: List[str] = None


class ActionSpace:
    """Defines the set of possible actions an agent can take."""

    def __init__(self, actions: List[str] = None, metadata: Dict[str, ActionMetadata] = None):
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

    def get_available_actions(self, current_time: float = None) -> List[str]:
        """Returns actions not on cooldown."""
        import time

        now = current_time or time.time()
        return [a for a in self.actions if self._cooldowns.get(a, 0) <= now]

    def record_action(self, action: str, timestamp: float = None) -> None:
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

    def __init__(self, n: int, action_names: List[str] = None):
        names = action_names or [str(i) for i in range(n)]
        super().__init__(names)
        self.n = n

    def sample(self) -> int:
        """Returns a random action index."""
        return random.randint(0, self.n - 1)

    def action_to_index(self, action: str) -> int:
        return self.actions.index(action) if action in self.actions else -1

    def index_to_action(self, index: int) -> str:
        return self.actions[index] if 0 <= index < len(self.actions) else ""


class BoxActionSpace:
    """Continuous action space within bounds."""

    def __init__(self, low: Union[float, np.ndarray], high: Union[float, np.ndarray], shape: tuple, dtype=np.float32):
        self.low = np.full(shape, low, dtype=dtype) if np.isscalar(low) else np.array(low, dtype=dtype)
        self.high = np.full(shape, high, dtype=dtype) if np.isscalar(high) else np.array(high, dtype=dtype)
        self.shape = shape
        self.dtype = dtype

    def sample(self) -> np.ndarray:
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
        self.nvec = np.array(nvec)
        self.shape = (len(nvec),)

    def sample(self) -> np.ndarray:
        return np.array([random.randint(0, n - 1) for n in self.nvec])

    def contains(self, action: np.ndarray) -> bool:
        return all(0 <= a < n for a, n in zip(action, self.nvec))


class DictActionSpace:
    """Hierarchical action space with named sub-spaces."""

    def __init__(self, spaces: Dict[str, ActionSpace]):
        self.spaces = spaces

    def sample(self) -> Dict[str, Any]:
        return {k: v.sample() for k, v in self.spaces.items()}

    def contains(self, action: Dict[str, Any]) -> bool:
        return all(self.spaces[k].contains(v) for k, v in action.items() if k in self.spaces)
