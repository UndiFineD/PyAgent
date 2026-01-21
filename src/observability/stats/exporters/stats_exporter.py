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


"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from typing import Any
import json

__version__ = VERSION


class StatsExporter:
    """Exports stats in various formats."""

    def __init__(self, format: str = "json") -> None:
        self.format = format

    def export(self, metrics: dict[str, Any], format: str | None = None) -> str:
        """Export metrics in specified format."""
        export_format = format or self.format
        if export_format == "json":
            return json.dumps(metrics)
        elif export_format == "prometheus":
            lines: list[str] = []
            for name, value in metrics.items():
                lines.append(f"{name} {value}")
            return "\n".join(lines)
        return ""
