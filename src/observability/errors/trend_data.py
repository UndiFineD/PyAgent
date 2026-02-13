#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
TrendData - Hold trend analysis payload

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate TrendData for a tracked metric, append values/timestamps, read direction and optional prediction
- Example: td = TrendData("cpu.load"); td.values.append(0.75); td.timestamps.append("2026-02-12T21:00:00Z"); inspect td.direction

WHAT IT DOES:
- Simple dataclass container for metric name, historical numeric values, timestamps, current trend direction, and an optional next-value prediction
- Exposes typed fields and defaults suitable for lightweight error/trend reporting across the agent

WHAT IT SHOULD DO BETTER:
- Validate timestamps and enforce consistent length between values and timestamps
- Provide methods for incremental updates, windowed aggregation, statistical summaries, and serialization (to/from dict or JSON)
- Optionally compute direction/prediction lazily from values or accept pluggable predictors

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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .trend_direction import TrendDirection

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
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .trend_direction import TrendDirection

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
