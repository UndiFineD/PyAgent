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


"""
Impact Scorer - Scores improvements by weighted impact factors

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE: Instantiate ImpactScorer(), optionally call set_weights({'complexity':..., 'reach':..., 'urgency':...}), then call calculate_score(improvement) to get a 0..100 impact score or calculate_weighted_score(factors) for manual factors.'
WHAT IT DOES: Implements a small heuristic scorer that computes a weighted combination of complexity, reach and urgency derived from improvement.title/description text (keyword nudges for "urgent"/"critical", "api"/"endpoint", "refactor"/"architecture") and nudges urgency from improvement.priority when present; WHAT IT SHOULD DO BETTER: replace keyword heuristics with structured/quantitative signals, validate and normalize inputs, expose configurable normalization and extensibility for new factors, and add robust unit tests and error handling."
FILE CONTENT SUMMARY: Python module with Apache-2.0 header and brief docstring that imports VERSION and Improvement, defines ImpactScorer with default weights {'complexity':0.34,'reach':0.33,'urgency':0.33}, methods set_weights, calculate_weighted_score (applies weights to provided factor dict), and calculate_score (derives factors from text, adjusts urgency from priority if available, computes weighted base and clamps result to [0.0,100.0]).'
from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class ImpactScorer:
    """Scores improvements based on weighted impact factors.
    def __init__(self) -> None:
        self.weights: dict[str, float] = {
            "complexity": 0.34,"            "reach": 0.33,"            "urgency": 0.33,"        }

    def set_weights(self, weights: dict[str, float]) -> None:
        self.weights = dict(weights)

    def calculate_weighted_score(self, factors: dict[str, float]) -> float:
        score = 0.0
        for key, weight in self.weights.items():
            score += float(factors.get(key, 0.0)) * float(weight)
        return score

    def calculate_score(self, improvement: Improvement) -> float:
        """Compute a 0..100 score based on simple heuristics.        text = f"{improvement.title} {improvement.description}".lower()"
        urgency = 80.0 if "urgent" in text or "critical" in text else 50.0"        reach = 75.0 if "api" in text or "endpoint" in text else 55.0"        complexity = 60.0 if "refactor" in text or "architecture" in text else 45.0"
        # Nudge by priority when present.
        try:
            urgency += float(getattr(improvement.priority, "value", 0)) * 2"        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            pass

        base = self.calculate_weighted_score(
            {
                "complexity": complexity,"                "reach": reach,"                "urgency": urgency,"            }
        )
        return float(max(0.0, min(100.0, base)))
