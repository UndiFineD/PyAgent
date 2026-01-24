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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class ImpactScorer:
    """Scores improvements based on weighted impact factors."""

    def __init__(self) -> None:
        self.weights: dict[str, float] = {
            "complexity": 0.34,
            "reach": 0.33,
            "urgency": 0.33,
        }

    def set_weights(self, weights: dict[str, float]) -> None:
        self.weights = dict(weights)

    def calculate_weighted_score(self, factors: dict[str, float]) -> float:
        score = 0.0
        for key, weight in self.weights.items():
            score += float(factors.get(key, 0.0)) * float(weight)
        return score

    def calculate_score(self, improvement: Improvement) -> float:
        """Compute a 0..100 score based on simple heuristics."""
        text = f"{improvement.title} {improvement.description}".lower()

        urgency = 80.0 if "urgent" in text or "critical" in text else 50.0
        reach = 75.0 if "api" in text or "endpoint" in text else 55.0
        complexity = 60.0 if "refactor" in text or "architecture" in text else 45.0

        # Nudge by priority when present.
        try:
            urgency += float(getattr(improvement.priority, "value", 0)) * 2
        except Exception:
            pass

        base = self.calculate_weighted_score(
            {
                "complexity": complexity,
                "reach": reach,
                "urgency": urgency,
            }
        )
        return float(max(0.0, min(100.0, base)))
