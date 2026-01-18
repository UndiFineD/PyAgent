# Copyright 2026 PyAgent Authors
# Reinforcement Learning Environment Framework - Phase 319 Enhanced

from __future__ import annotations
import abc
import logging
from typing import Any, Tuple, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from .ActionSpace import ActionSpace, DiscreteActionSpace
from .MDP import Transition

logger = logging.getLogger(__name__)

@dataclass
class EpisodeStats:
    """Statistics for a single episode."""
    episode_id: int
    total_reward: float = 0.0
    steps: int = 0
    done: bool = False
    info: Dict[str, Any] = field(default_factory=dict)

class RLEnvironment(abc.ABC):
    """
    Base class for any Reinforcement Learning environment in PyAgent.
    Inspired by Gymnasium but tuned for multi-agent autonomous code improvement.
    Enhanced with episode management, wrappers, and vectorized support.
    """

    def __init__(self, max_steps: int = 1000):
        self.action_space: ActionSpace | None = None
        self.observation_space: Any = None
        self.state: Any = None
        self.max_steps = max_steps
        self._current_step = 0
        self._episode_count = 0
        self._episode_rewards: List[float] = []
        self._current_episode_reward = 0.0
        self._reward_shaping_fn: Optional[Callable[[float, Any, Any], float]] = None
        self._terminated = False
        self._truncated = False

    @abc.abstractmethod
    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Any, Dict]:
        """
        Resets the environment to an initial state.
        Returns: (observation, info)
        """
        pass

    @abc.abstractmethod
    def step(self, action: Any) -> Tuple[Any, float, bool, bool, Dict[str, Any]]:
        """
        Executes an action in the environment.
        Returns: (observation, reward, terminated, truncated, info)
        """
        pass

    def render(self, mode: str = "human") -> Optional[Any]:
        """Visualizes the current state."""
        pass

    def close(self) -> None:
        """Clean up resources."""
        pass

    def seed(self, seed: int) -> List[int]:
        """Sets the random seed."""
        import random
        import numpy as np
        random.seed(seed)
        np.random.seed(seed)
        return [seed]

    def set_reward_shaping(self, fn: Callable[[float, Any, Any], float]) -> None:
        """Applies a custom reward shaping function."""
        self._reward_shaping_fn = fn

    def _shape_reward(self, reward: float, state: Any, next_state: Any) -> float:
        if self._reward_shaping_fn:
            return self._reward_shaping_fn(reward, state, next_state)
        return reward

    def get_episode_stats(self) -> Dict[str, Any]:
        return {
            "episode_count": self._episode_count,
            "avg_reward": sum(self._episode_rewards) / len(self._episode_rewards) if self._episode_rewards else 0.0,
            "total_episodes": len(self._episode_rewards),
            "best_episode_reward": max(self._episode_rewards) if self._episode_rewards else 0.0
        }

class CodeImprovementEnvironment(RLEnvironment):
    """
    Concrete RL environment for autonomous code improvement tasks.
    State: Current code metrics (complexity, coverage, etc.)
    Actions: Improvement strategies (refactor, add_tests, optimize, etc.)
    Reward: Delta in code quality metrics.
    """

    def __init__(self, initial_metrics: Dict[str, float] = None):
        super().__init__(max_steps=50)
        self.action_space = DiscreteActionSpace(5, [
            "refactor", "add_tests", "optimize", "document", "skip"
        ])
        self.initial_metrics = initial_metrics or {"complexity": 50.0, "coverage": 0.5, "quality": 0.6}
        self.metrics = dict(self.initial_metrics)
        self.state = self._get_state()

    def _get_state(self) -> Dict[str, float]:
        return dict(self.metrics)

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        if seed:
            self.seed(seed)
        self.metrics = dict(self.initial_metrics)
        self._current_step = 0
        self._current_episode_reward = 0.0
        self._terminated = False
        self._truncated = False
        self.state = self._get_state()
        self._episode_count += 1
        return self.state, {"episode": self._episode_count}

    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        self._current_step += 1
        old_metrics = dict(self.metrics)
        
        # Simulate action effects
        action_name = self.action_space.actions[action] if action < len(self.action_space.actions) else "skip"
        
        if action_name == "refactor":
            self.metrics["complexity"] = max(1, self.metrics["complexity"] - 5)
            self.metrics["quality"] = min(1.0, self.metrics["quality"] + 0.05)
        elif action_name == "add_tests":
            self.metrics["coverage"] = min(1.0, self.metrics["coverage"] + 0.1)
        elif action_name == "optimize":
            self.metrics["complexity"] = max(1, self.metrics["complexity"] - 2)
        elif action_name == "document":
            self.metrics["quality"] = min(1.0, self.metrics["quality"] + 0.03)
        # skip does nothing

        # Calculate reward
        reward = 0.0
        reward += (old_metrics["complexity"] - self.metrics["complexity"]) * 0.1
        reward += (self.metrics["coverage"] - old_metrics["coverage"]) * 5.0
        reward += (self.metrics["quality"] - old_metrics["quality"]) * 2.0
        
        reward = self._shape_reward(reward, old_metrics, self.metrics)
        self._current_episode_reward += reward
        self.state = self._get_state()

        # Check termination
        self._terminated = (
            self.metrics["complexity"] <= 10 and 
            self.metrics["coverage"] >= 0.9 and 
            self.metrics["quality"] >= 0.9
        )
        self._truncated = self._current_step >= self.max_steps

        if self._terminated or self._truncated:
            self._episode_rewards.append(self._current_episode_reward)

        info = {
            "step": self._current_step,
            "action": action_name,
            "metrics": dict(self.metrics)
        }

        return self.state, reward, self._terminated, self._truncated, info

    def render(self, mode: str = "human") -> Optional[str]:
        status = f"Step {self._current_step}: Complexity={self.metrics['complexity']:.1f}, Coverage={self.metrics['coverage']:.2f}, Quality={self.metrics['quality']:.2f}"
        if mode == "human":
            logger.info(status)
        return status
