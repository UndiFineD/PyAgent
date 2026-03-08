"""
LLM_CONTEXT_START

## Source: src-old/core/rl/RewardFunctions.description.md

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
## Source: src-old/core/rl/RewardFunctions.improvements.md

# Improvements for RewardFunctions

**File**: `src\core\rl\RewardFunctions.py`  
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

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Reward Functions for Agent Reinforcement - Phase 319 Enhanced

import math
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RewardType(Enum):
    SPARSE = "sparse"
    DENSE = "dense"
    SHAPED = "shaped"
    INTRINSIC = "intrinsic"


@dataclass
class RewardSignal:
    """Structured reward with metadata."""

    value: float
    reward_type: RewardType
    source: str
    explanation: str = ""


class RewardFunctions:
    """Library of standard reward functions for agentic behavior."""

    @staticmethod
    def binary_reward(
        success: bool, positive: float = 1.0, negative: float = -1.0
    ) -> float:
        return positive if success else negative

    @staticmethod
    def complexity_reduction_reward(
        old_complexity: float, new_complexity: float, scale: float = 0.1
    ) -> RewardSignal:
        """Positive reward for reducing cyclomatic complexity."""
        delta = old_complexity - new_complexity
        if delta > 0:
            value = delta * scale
            explanation = f"Reduced complexity by {delta:.1f}"
        else:
            value = delta * scale * 5  # Heavier penalty for regression
            explanation = f"Increased complexity by {abs(delta):.1f} (penalty)"
        return RewardSignal(value, RewardType.SHAPED, "complexity", explanation)

    @staticmethod
    def test_coverage_reward(
        old_coverage: float, new_coverage: float, scale: float = 5.0
    ) -> RewardSignal:
        """Reward for increasing test coverage."""
        delta = new_coverage - old_coverage
        value = delta * scale
        return RewardSignal(
            value, RewardType.DENSE, "coverage", f"Coverage changed by {delta:.2%}"
        )

    @staticmethod
    def latency_penalty(
        latency_s: float, threshold_s: float = 2.0, max_penalty: float = -5.0
    ) -> RewardSignal:
        """Penalize long-running agent cycles."""
        if latency_s > threshold_s:
            penalty = -math.log(1 + (latency_s - threshold_s))
            value = max(max_penalty, penalty)
            return RewardSignal(
                value,
                RewardType.SHAPED,
                "latency",
                f"Latency {latency_s:.2f}s exceeded threshold",
            )
        return RewardSignal(0.1, RewardType.SHAPED, "latency", "Fast execution bonus")

    @staticmethod
    def curiosity_reward(state_novelty: float, scale: float = 0.5) -> RewardSignal:
        """Intrinsic reward for exploring novel states."""
        value = state_novelty * scale
        return RewardSignal(
            value,
            RewardType.INTRINSIC,
            "curiosity",
            f"Novelty score: {state_novelty:.2f}",
        )

    @staticmethod
    def goal_proximity_reward(
        current_dist: float, prev_dist: float, goal_bonus: float = 10.0
    ) -> RewardSignal:
        """Reward for getting closer to a goal."""
        if current_dist == 0:
            return RewardSignal(goal_bonus, RewardType.SPARSE, "goal", "Goal reached!")
        improvement = prev_dist - current_dist
        return RewardSignal(
            improvement,
            RewardType.DENSE,
            "goal",
            f"Distance improved by {improvement:.2f}",
        )

    @staticmethod
    def consistency_reward(
        predictions: List[Any], ground_truth: Any, scale: float = 1.0
    ) -> RewardSignal:
        """Reward for consistent/correct predictions."""
        if not predictions:
            return RewardSignal(0.0, RewardType.SPARSE, "consistency", "No predictions")
        correct = sum(1 for p in predictions if p == ground_truth)
        accuracy = correct / len(predictions)
        return RewardSignal(
            accuracy * scale,
            RewardType.DENSE,
            "consistency",
            f"Accuracy: {accuracy:.2%}",
        )

    @staticmethod
    def resource_efficiency_reward(
        resources_used: float, budget: float, scale: float = 1.0
    ) -> RewardSignal:
        """Reward for staying within resource budget."""
        if resources_used > budget:
            penalty = -((resources_used - budget) / budget) * scale * 2
            return RewardSignal(
                penalty, RewardType.SHAPED, "resources", "Over budget penalty"
            )
        efficiency = 1.0 - (resources_used / budget)
        return RewardSignal(
            efficiency * scale,
            RewardType.SHAPED,
            "resources",
            f"Efficiency: {efficiency:.2%}",
        )


class CompositeRewardFunction:
    """Combines multiple reward functions with weights."""

    def __init__(self):
        self.components: List[tuple[str, Callable, float]] = []

    def add(
        self, name: str, fn: Callable, weight: float = 1.0
    ) -> "CompositeRewardFunction":
        self.components.append((name, fn, weight))
        return self

    def compute(self, **kwargs) -> RewardSignal:
        total = 0.0
        explanations = []
        for name, fn, weight in self.components:
            result = fn(**kwargs)
            if isinstance(result, RewardSignal):
                total += result.value * weight
                explanations.append(f"{name}: {result.value:.3f}")
            else:
                total += result * weight
                explanations.append(f"{name}: {result:.3f}")
        return RewardSignal(
            total, RewardType.SHAPED, "composite", " | ".join(explanations)
        )


class RewardShaper:
    """Applies potential-based reward shaping to avoid changing optimal policy."""

    def __init__(self, potential_fn: Callable[[Any], float], gamma: float = 0.99):
        self.potential_fn = potential_fn
        self.gamma = gamma

    def shape(self, reward: float, state: Any, next_state: Any) -> float:
        """F(s,s') = γΦ(s') - Φ(s)"""
        shaping = self.gamma * self.potential_fn(next_state) - self.potential_fn(state)
        return reward + shaping
