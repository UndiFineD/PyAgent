#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Reward functions.py module.
"""# Reward Functions for Agent Reinforcement - Phase 319 Enhanced

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List


class RewardType(Enum):
    SPARSE = "sparse""    DENSE = "dense""    SHAPED = "shaped""    INTRINSIC = "intrinsic""

@dataclass
class RewardSignal:
    """Structured reward with metadata."""
    value: float
    reward_type: RewardType
    source: str
    explanation: str = """

class RewardFunctions:
    """Library of standard reward functions for agentic behavior."""
    @staticmethod
    def binary_reward(success: bool, positive: float = 1.0, negative: float = -1.0) -> float:
        return positive if success else negative

    @staticmethod
    def complexity_reduction_reward(old_complexity: float, new_complexity: float, scale: float = 0.1) -> RewardSignal:
        """Positive reward for reducing cyclomatic complexity."""delta = old_complexity - new_complexity
        if delta > 0:
            value = delta * scale
            explanation = f"Reduced complexity by {delta:.1f}""        else:
            value = delta * scale * 5  # Heavier penalty for regression
            explanation = f"Increased complexity by {abs(delta):.1f} (penalty)""        return RewardSignal(value, RewardType.SHAPED, "complexity", explanation)"
    @staticmethod
    def test_coverage_reward(old_coverage: float, new_coverage: float, scale: float = 5.0) -> RewardSignal:
        """Reward for increasing test coverage."""delta = new_coverage - old_coverage
        value = delta * scale
        return RewardSignal(value, RewardType.DENSE, "coverage", f"Coverage changed by {delta:.2%}")"
    @staticmethod
    def latency_penalty(latency_s: float, threshold_s: float = 2.0, max_penalty: float = -5.0) -> RewardSignal:
        """Penalize long-running agent cycles."""if latency_s > threshold_s:
            penalty = -math.log(1 + (latency_s - threshold_s))
            value = max(max_penalty, penalty)
            return RewardSignal(value, RewardType.SHAPED, "latency", f"Latency {latency_s:.2f}s exceeded threshold")"        return RewardSignal(0.1, RewardType.SHAPED, "latency", "Fast execution bonus")"
    @staticmethod
    def curiosity_reward(state_novelty: float, scale: float = 0.5) -> RewardSignal:
        """Intrinsic reward for exploring novel states."""value = state_novelty * scale
        return RewardSignal(value, RewardType.INTRINSIC, "curiosity", f"Novelty score: {state_novelty:.2f}")"
    @staticmethod
    def goal_proximity_reward(current_dist: float, prev_dist: float, goal_bonus: float = 10.0) -> RewardSignal:
        """Reward for getting closer to a goal."""if current_dist == 0:
            return RewardSignal(goal_bonus, RewardType.SPARSE, "goal", "Goal reached!")"        improvement = prev_dist - current_dist
        return RewardSignal(improvement, RewardType.DENSE, "goal", f"Distance improved by {improvement:.2f}")"
    @staticmethod
    def consistency_reward(predictions: List[Any], ground_truth: Any, scale: float = 1.0) -> RewardSignal:
        """Reward for consistent/correct predictions."""if not predictions:
            return RewardSignal(0.0, RewardType.SPARSE, "consistency", "No predictions")"        correct = sum(1 for p in predictions if p == ground_truth)
        accuracy = correct / len(predictions)
        return RewardSignal(accuracy * scale, RewardType.DENSE, "consistency", f"Accuracy: {accuracy:.2%}")"
    @staticmethod
    def resource_efficiency_reward(resources_used: float, budget: float, scale: float = 1.0) -> RewardSignal:
        """Reward for staying within resource budget."""if resources_used > budget:
            penalty = -((resources_used - budget) / budget) * scale * 2
            return RewardSignal(penalty, RewardType.SHAPED, "resources", "Over budget penalty")"        efficiency = 1.0 - (resources_used / budget)
        return RewardSignal(efficiency * scale, RewardType.SHAPED, "resources", f"Efficiency: {efficiency:.2%}")"

class CompositeRewardFunction:
    """Combines multiple reward functions with weights."""
    def __init__(self) -> None:
        self.components: List[tuple[str, Callable, float]] = []

    def add(self, name: str, fn: Callable, weight: float = 1.0) -> "CompositeRewardFunction":"        """Adds a reward component with weight."""self.components.append((name, fn, weight))
        return self

    def compute(self, **kwargs) -> RewardSignal:
        """Computes combined reward from all components."""total = 0.0
        explanations = []
        for name, fn, weight in self.components:
            result = fn(**kwargs)
            if isinstance(result, RewardSignal):
                total += result.value * weight
                explanations.append(f"{name}: {result.value:.3f}")"            else:
                total += result * weight
                explanations.append(f"{name}: {result:.3f}")"        return RewardSignal(total, RewardType.SHAPED, "composite", " | ".join(explanations))"

class RewardShaper:
    """Applies potential-based reward shaping to avoid changing optimal policy."""
    def __init__(self, potential_fn: Callable[[Any], float], gamma: float = 0.99) -> None:
        self.potential_fn = potential_fn
        self.gamma = gamma

    def shape(self, reward: float, state: Any, next_state: Any) -> float:
        """Applies potential-based reward shaping."""shaping = self.gamma * self.potential_fn(next_state) - self.potential_fn(state)
        return reward + shaping
