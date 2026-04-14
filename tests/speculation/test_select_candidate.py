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

"""Red-phase tests for speculation candidate selection behavior contracts."""

from __future__ import annotations

import math
from collections.abc import Callable

import pytest

import speculation


def _select_candidate_callable() -> Callable[[dict[str, float], float], str | None]:
    """Return the `speculation.select_candidate` callable under test.

    Returns:
        Callable[[dict[str, float], float], str | None]: The candidate selection function.

    """
    candidate = getattr(speculation, "select_candidate", None)
    assert callable(candidate), "Expected speculation.select_candidate() to exist and be callable."
    return candidate


def test_select_candidate_applies_threshold_and_picks_highest_score() -> None:
    """Verify threshold filtering and highest-score candidate selection."""
    select_candidate = _select_candidate_callable()
    scores = {"alpha": 0.20, "beta": 0.85, "gamma": 0.70}

    result = select_candidate(scores, threshold=0.50)

    assert result == "beta"


def test_select_candidate_returns_none_for_empty_input() -> None:
    """Verify empty score input returns None."""
    select_candidate = _select_candidate_callable()

    result = select_candidate({}, threshold=0.0)

    assert result is None


def test_select_candidate_returns_none_when_no_scores_meet_threshold() -> None:
    """Verify None is returned when all scores are below threshold."""
    select_candidate = _select_candidate_callable()
    scores = {"alpha": 0.20, "beta": 0.30}

    result = select_candidate(scores, threshold=0.90)

    assert result is None


def test_select_candidate_uses_lexicographic_tie_break_deterministically() -> None:
    """Verify ties choose lexicographically smallest key in repeated runs."""
    select_candidate = _select_candidate_callable()
    scores = {"beta": 1.0, "alpha": 1.0, "gamma": 0.5}

    observed = [select_candidate(scores, threshold=0.0) for _ in range(20)]

    assert observed == ["alpha"] * 20


@pytest.mark.parametrize("bad_score", [math.nan, math.inf, -math.inf])
def test_select_candidate_rejects_non_finite_scores(bad_score: float) -> None:
    """Verify non-finite score values raise ValueError.

    Args:
        bad_score: A non-finite score candidate.

    """
    select_candidate = _select_candidate_callable()

    with pytest.raises(ValueError):
        select_candidate({"alpha": 1.0, "beta": bad_score}, threshold=0.0)
