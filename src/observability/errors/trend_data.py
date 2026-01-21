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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from .trend_direction import TrendDirection
from dataclasses import dataclass, field

__version__ = VERSION


@dataclass
class TrendData:
    """Error trend analysis data.

    Attributes:
        metric_name: Name of the metric being tracked.
        values: Historical values.
        timestamps: Timestamps for each value.
        direction: Current trend direction.
        prediction: Predicted next value.
    """

    metric_name: str
    values: list[float] = field(default_factory=lambda: [])
    timestamps: list[str] = field(default_factory=lambda: [])
    direction: TrendDirection = TrendDirection.STABLE
    prediction: float | None = None
