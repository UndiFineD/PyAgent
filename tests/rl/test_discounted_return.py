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

"""Red-phase tests for RL discounted return behavior contracts."""

from __future__ import annotations

import math
from collections.abc import Callable

import pytest

import rl


def _discounted_return_callable() -> Callable[[list[float], float], float]:
    """Return the `rl.discounted_return` callable under test.

    Returns:
        Callable[[list[float], float], float]: The discounted return function.

    """
    candidate = getattr(rl, "discounted_return", None)
    assert callable(candidate), "Expected rl.discounted_return() to exist and be callable."
    return candidate


def test_discounted_return_computes_expected_value() -> None:
    """Verify discounted sum calculation for a deterministic reward sequence."""
    discounted_return = _discounted_return_callable()
    rewards = [1.0, 2.0, 3.0]
    gamma = 0.9

    result = discounted_return(rewards, gamma)

    expected = 1.0 + (2.0 * 0.9) + (3.0 * 0.9 * 0.9)
    assert result == pytest.approx(expected)


def test_discounted_return_returns_zero_for_empty_rewards() -> None:
    """Verify empty reward input returns 0.0 exactly."""
    discounted_return = _discounted_return_callable()

    result = discounted_return([], 0.75)

    assert result == 0.0


@pytest.mark.parametrize("gamma", [-0.01, 1.01])
def test_discounted_return_rejects_invalid_gamma(gamma: float) -> None:
    """Verify out-of-range gamma values raise ValueError.

    Args:
        gamma: Invalid gamma value outside inclusive [0.0, 1.0] bounds.

    """
    discounted_return = _discounted_return_callable()

    with pytest.raises(ValueError):
        discounted_return([1.0, 2.0], gamma)


@pytest.mark.parametrize("bad_reward", [math.nan, math.inf, -math.inf])
def test_discounted_return_rejects_non_finite_rewards(bad_reward: float) -> None:
    """Verify non-finite reward values raise ValueError.

    Args:
        bad_reward: A non-finite reward candidate.

    """
    discounted_return = _discounted_return_callable()

    with pytest.raises(ValueError):
        discounted_return([1.0, bad_reward], 0.9)
