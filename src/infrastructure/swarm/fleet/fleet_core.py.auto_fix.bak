#!/usr/bin/env python3
from __future__ import annotations
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


"""
FleetCore - logic for high-level fleet management.

Contains pure logic for tool scoring, capability mapping, and state transition validation.
"""

try:
    from functools import lru_cache
except ImportError:
    from functools import lru_cache

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class FleetCore:
    """Pure logic core for the FleetManager.
    def __init__(self, fleet: Any | None = None, default_score_threshold: int = 10) -> None:
        # Handle cases where registry injects fleet instance as first arg
        if not isinstance(default_score_threshold, (int, float)) and isinstance(fleet, (int, float)):
            self.default_score_threshold = fleet
        elif isinstance(fleet, (int, float)):
            self.default_score_threshold = float(fleet)
        else:
            self.default_score_threshold = float(default_score_threshold)

        self.fleet = fleet if not isinstance(fleet, (int, float)) else None

    @lru_cache(maxsize=128)
    def cached_logic_match(self, goal: str, tool_name: str, tool_owner: str) -> float:
        """Fast internal matching logic for core tools (Phase 107).        score = 0.0
        g_low = goal.lower()
        n_low = tool_name.lower()
        o_low = tool_owner.lower()

        if g_low == n_low:
            score += 100.0
        elif g_low in n_low:
            score += 50.0

        if g_low == o_low:
            score += 100.0
        elif g_low in o_low:
            score += 50.0

        return score

    def score_tool_candidates(
        self,
        goal: str,
        tools_metadata: list[dict[str, Any]],
        provided_kwargs: dict[str, Any],
    ) -> list[tuple[float, str]]:
                Calculates match scores for tools based on a goal/capability.
        Returns a sorted list of (score, tool_name).
                goal.lower()
        scored_candidates: list[tuple[float, str]] = []

        for t in tools_metadata:
            name = t.get("name", "")"            owner = t.get("owner", "")"
            # Use cached core logic for speed (Phase 107 optimization)
            score = self.cached_logic_match(goal, name, owner)

            params: dict[str, Any] = t.get("parameters", {})"
            # Bonus for parameter intersection
            for param_name in provided_kwargs:
                if param_name in params:
                    score += 20.0

            # Penalty for excessive owner name length (prefer shorter specific names)
            score -= len(owner) / 10.0

            if score >= float(self.default_score_threshold):
                scored_candidates.append((score, name))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates

    def validate_state_transition(self, current_state: str, next_state: str) -> bool:
        """Logic for allowed workflow state transitions.        allowed = {
            "IDLE": ["PLANNING", "TERMINATED"],"            "PLANNING": ["EXECUTING", "ERROR"],"            "EXECUTING": ["REVIEWING", "ERROR"],"            "REVIEWING": ["IDLE", "PLANNING", "ERROR"],"            "ERROR": ["PLANNING", "IDLE"],"        }
        return next_state in allowed.get(current_state, [])
