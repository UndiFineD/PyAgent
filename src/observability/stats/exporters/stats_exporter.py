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
Stats Exporter - Export metrics in JSON and Prometheus text

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate and call:
  from stats_exporter import StatsExporter
  exporter = StatsExporter(export_format="json")  # or "prometheus"
  text = exporter.export({"requests_total": 42, "latency_seconds": 0.123})
- Or override per-call: exporter.export(metrics, export_format="prometheus")

WHAT IT DOES:
- Provides a small utility class StatsExporter that serializes
  a metrics dict to either JSON (json.dumps) or a simple
  Prometheus-style plaintext (one "name value" per line).
- Defaults to JSON; returns an empty string for unsupported
  formats.

WHAT IT SHOULD DO BETTER:
- Validate metric names and values and handle non-primitive
  values (lists, dicts) robustly instead of dumping or
  producing invalid Prometheus lines.
- Implement proper Prometheus exposition formatting: support
  HELP and TYPE lines, label support, sanitization of metric
  names, and float formatting; optionally expose timestamps.
- Add error handling/logging, unit tests for edge cases,
  deterministic ordering for stable outputs, streaming/
  large-payload support, and an extensible plugin-based
  exporter registry for additional formats.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_stats.py
"""

from __future__ import annotations

import json
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class StatsExporter:
    """Exports stats in various formats."""

    def __init__(self, export_format: str = "json") -> None:
        self.export_format = export_format

    def export(self, metrics: dict[str, Any], export_format: str | None = None) -> str:
        """Export metrics in specified format."""
        effective_format = export_format or self.export_format
        if effective_format == "json":
            return json.dumps(metrics)
        elif effective_format == "prometheus":
            lines: list[str] = []
            for name, value in metrics.items():
                lines.append(f"{name} {value}")
            return "\n".join(lines)
        return ""
