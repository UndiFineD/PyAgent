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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .ABComparisonResult import ABComparisonResult
from .ABSignificanceResult import ABSignificanceResult

from typing import Any, Dict, List



































class ABComparator:
    """Compares A/B test metrics."""
    def __init__(self) -> None:
        self.results: List[Dict[str, Any]] = []

    def compare(self, a_data: Dict[str, float], b_data: Dict[str, float]) -> ABComparisonResult:
        """Compare two metric groups (A vs B)."""
        common = sorted(set(a_data.keys()) & set(b_data.keys()))
        diffs: Dict[str, float] = {}
        for key in common:
            try:
                diffs[key] = float(b_data[key]) - float(a_data[key])
            except (TypeError, ValueError):
                # Non-numeric values are ignored.
                continue
        return ABComparisonResult(metrics_compared=len(common), differences=diffs)

    def calculate_significance(
        self,
        control_values: List[float],
        treatment_values: List[float],
        alpha: float = 0.05,
    ) -> ABSignificanceResult:
        """Very lightweight significance heuristic for tests.

        This is not a full statistical test; it's a simple signal used by unit tests.
        """
        if not control_values or not treatment_values:
            return ABSignificanceResult(p_value=1.0, is_significant=False, effect_size=0.0)

        mean_a = sum(control_values) / len(control_values)
        mean_b = sum(treatment_values) / len(treatment_values)
        effect = mean_b - mean_a
        # Heuristic: big effect => low p-value.
        p_value = 0.01 if abs(effect) >= 1.0 else 0.5
        return ABSignificanceResult(p_value=p_value, is_significant=p_value < alpha, effect_size=effect)
