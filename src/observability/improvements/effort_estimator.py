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


"""
Effort Estimator - Estimate effort for improvements

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.tools.effort_estimator import EffortEstimator
est = EffortEstimator()
est.add_historical_data("refactor", 4.0)
result = est.estimate(improvement, complexity="low", category="refactor")
print(result.hours)

WHAT IT DOES:
Provides a simple heuristic-based estimator that returns an EffortEstimateResult(hours: float) using (in order) per-category historical averages, configured base rates keyed by complexity ("low", "medium", "high"), and an optional EffortEstimate enum bias on top of the base value.

WHAT IT SHOULD DO BETTER:
- Persist and time-weight historical data (recency bias), use median and robust statistics instead of raw mean, and expose confidence/variance in the returned estimate.
- Validate inputs and categories more strictly, accept and normalize ImprovementCategory and string categories uniformly, and surface reasons/trace for the computed hours for explainability.
- Allow pluggable scoring (e.g., integrate static analysis complexity, team velocity) and support async/IO-friendly loading/saving of historical records (follow repository transactional FS conventions).

FILE CONTENT SUMMARY:
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

from typing import Any

from src.core.base.lifecycle.version import VERSION

from .effort_estimate import EffortEstimate
from .effort_estimate_result import EffortEstimateResult
from .improvement import Improvement
from .improvement_category import ImprovementCategory

__version__ = VERSION


class EffortEstimator:
    """Estimates effort for improvements."""

    def __init__(self) -> None:
        self.base_rates: dict[str, float] = {
            "low": 2.0,
            "medium": 6.0,
            "high": 16.0,
        }
        self.historical_data: dict[str, list[float]] = {}

    def add_historical_data(self, category: str, actual_hours: float) -> None:
        self.historical_data.setdefault(category, []).append(float(actual_hours))

    def estimate(self, improvement: Improvement, **kwargs: Any) -> EffortEstimateResult:
        complexity = str(kwargs.get("complexity", "medium")).lower()
        category = kwargs.get("category")
        if isinstance(category, ImprovementCategory):
            category_key = category.value
        else:
            category_key = str(category) if category is not None else ""

        if category_key and category_key in self.historical_data and self.historical_data[category_key]:
            base = sum(self.historical_data[category_key]) / len(self.historical_data[category_key])
        else:
            base = float(self.base_rates.get(complexity, self.base_rates["medium"]))

        # If an EffortEstimate enum is present, bias the base.
        effort = getattr(improvement, "effort", None)
        if isinstance(effort, EffortEstimate):
            scale = {
                EffortEstimate.TRIVIAL: 0.5,
                EffortEstimate.SMALL: 0.75,
                EffortEstimate.MEDIUM: 1.0,
                EffortEstimate.LARGE: 2.0,
                EffortEstimate.EPIC: 4.0,
            }.get(effort, 1.0)
            base *= scale

        return EffortEstimateResult(hours=float(base))
"""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

from .effort_estimate import EffortEstimate
from .effort_estimate_result import EffortEstimateResult
from .improvement import Improvement
from .improvement_category import ImprovementCategory

__version__ = VERSION


class EffortEstimator:
    """Estimates effort for improvements."""

    def __init__(self) -> None:
        self.base_rates: dict[str, float] = {
            "low": 2.0,
            "medium": 6.0,
            "high": 16.0,
        }
        self.historical_data: dict[str, list[float]] = {}

    def add_historical_data(self, category: str, actual_hours: float) -> None:
        self.historical_data.setdefault(category, []).append(float(actual_hours))

    def estimate(self, improvement: Improvement, **kwargs: Any) -> EffortEstimateResult:
        complexity = str(kwargs.get("complexity", "medium")).lower()
        category = kwargs.get("category")
        if isinstance(category, ImprovementCategory):
            category_key = category.value
        else:
            category_key = str(category) if category is not None else ""

        if category_key and category_key in self.historical_data and self.historical_data[category_key]:
            base = sum(self.historical_data[category_key]) / len(self.historical_data[category_key])
        else:
            base = float(self.base_rates.get(complexity, self.base_rates["medium"]))

        # If an EffortEstimate enum is present, bias the base.
        effort = getattr(improvement, "effort", None)
        if isinstance(effort, EffortEstimate):
            scale = {
                EffortEstimate.TRIVIAL: 0.5,
                EffortEstimate.SMALL: 0.75,
                EffortEstimate.MEDIUM: 1.0,
                EffortEstimate.LARGE: 2.0,
                EffortEstimate.EPIC: 4.0,
            }.get(effort, 1.0)
            base *= scale

        return EffortEstimateResult(hours=float(base))
