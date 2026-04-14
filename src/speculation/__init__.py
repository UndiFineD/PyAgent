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

"""Speculation module for PyAgent."""

from __future__ import annotations

import math
import warnings


def select_candidate(scores: dict[str, float], threshold: float = 0.0) -> str | None:
    """Select the best candidate at or above a score threshold.

    Args:
        scores: Candidate score mapping keyed by candidate name.
        threshold: Minimum score required for candidacy.

    Returns:
        str | None: Best candidate key or None if no key passes threshold.

    Raises:
        ValueError: If any score value is non-finite.

    """
    if not all(math.isfinite(score) for score in scores.values()):
        raise ValueError("scores must contain only finite values")

    filtered = [(key, score) for key, score in scores.items() if score >= threshold]

    if not filtered:
        return None

    # Max score first, then lexicographically smallest key for deterministic tie-breaks.
    return min(filtered, key=lambda item: (-item[1], item[0]))[0]


def validate() -> bool:
    """Validate speculation package compatibility during deprecation window.

    Returns:
        bool: Always True for compatibility during Slice 1.

    """
    warnings.warn(
        "Use speculation.select_candidate(); validate() will be removed in Slice 2.",
        DeprecationWarning,
        stacklevel=2,
    )
    return True


__all__ = ["select_candidate", "validate"]
