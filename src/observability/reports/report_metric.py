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
ReportMetric - Custom report metric dataclass

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Create and use a simple metric for agent reports:
  report = ReportMetric(name="latency_ms", value=123.4, unit="ms", threshold=200.0, trend="-")
- Serialize or include in report payloads (e.g., as dict/json after adding a to_dict method).
- Use for alerting when value crosses threshold and for display in generated reports.

WHAT IT DOES:
- Encapsulates a single metric for reports as a dataclass with fields: name, value, unit, threshold, and trend.
- Provides a lightweight, typed container suitable for inclusion in generated reports and basic downstream processing.

WHAT IT SHOULD DO BETTER:
- Add validation (e.g., ensure value is finite, threshold sensible, name non-empty) and explicit type coercion.
- Provide utility methods: to_dict/from_dict, JSON serialization, human-readable formatting, and comparison helpers for trend detection.
- Use stricter types/enums for unit and trend, include unit tests, and document expected units and trend semantics; optionally integrate with metrics registry or telemetry exporters.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION


@dataclass
class ReportMetric:
    """Custom metric for reports.
    Attributes:
        name: Metric name.
        value: Metric value.
        unit: Unit of measurement.
        threshold: Alert threshold.
        trend: Trend direction (+/-/=).
    """

    name: str
    value: float
    unit: str = ""
    threshold: float | None = None
    trend: str = "="
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION


@dataclass
class ReportMetric:
    """Custom metric for reports.
    Attributes:
        name: Metric name.
        value: Metric value.
        unit: Unit of measurement.
        threshold: Alert threshold.
        trend: Trend direction (+/-/=).
    """

    name: str
    value: float
    unit: str = ""
    threshold: float | None = None
    trend: str = "="
