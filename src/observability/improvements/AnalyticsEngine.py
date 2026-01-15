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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .CompletionTrend import CompletionTrend
from .Improvement import Improvement

__version__ = VERSION




class AnalyticsEngine:
    """Very small analytics engine used by tests."""

    def __init__(self) -> None:
        self._completed: list[Improvement] = []

    def record_completion(self, improvement: Improvement) -> None:
        self._completed.append(improvement)

    def get_completion_trend(self, period_days: int = 30) -> CompletionTrend:
        return CompletionTrend(total_completed=len(self._completed))

    def calculate_velocity(self, sprint_days: int = 14) -> float:
        total_points = 0.0
        for imp in self._completed:
            total_points += float(getattr(imp, "story_points", 0) or 0)
        return total_points / (float(sprint_days) / 7.0) if sprint_days else 0.0
