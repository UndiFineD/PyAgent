#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reinforcement learning module for PyAgent."""

from __future__ import annotations

import math
import warnings


def discounted_return(rewards: list[float], gamma: float = 0.99) -> float:
    """Compute the discounted return for a reward sequence.

    Args:
        rewards: Ordered rewards where index 0 is the immediate reward.
        gamma: Discount factor in the inclusive range [0.0, 1.0].

    Returns:
        float: Discounted sum across all rewards.

    Raises:
        ValueError: If gamma is out of range or any reward is non-finite.

    """
    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be within [0.0, 1.0]")
    if not all(math.isfinite(reward) for reward in rewards):
        raise ValueError("rewards must contain only finite values")

    return sum(reward * (gamma**index) for index, reward in enumerate(rewards))


def validate() -> bool:
    """Validate RL package compatibility during deprecation window.

    Returns:
        bool: Always True for compatibility during Slice 1.

    """
    warnings.warn(
        "Use rl.discounted_return(); validate() will be removed in Slice 2.",
        DeprecationWarning,
        stacklevel=2,
    )
    return True


__all__ = ["discounted_return", "validate"]
