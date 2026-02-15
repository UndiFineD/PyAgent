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
improvement_exporter.py - Export improvements to JSON/CSV

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.tools.improvement_exporter import ImprovementExporter
exporter = ImprovementExporter()
json_text = exporter.export(improvements_list, output_format="json")
csv_text = exporter.export(improvements_list, output_format="csv")

WHAT IT DOES:
- Provides a small utility class ImprovementExporter that serializes a list of Improvement objects to JSON or CSV text
- Supports two formats: "json" and "csv"
- Returns the serialized data as a string for downstream writing or transmission

WHAT IT SHOULD DO BETTER:
- Properly escape CSV fields (commas, quotes, newlines) and use the csv module rather than naive string joins
- Provide optional file I/O helpers to write directly to a file path or stream large exports incrementally
- Validate input types and surface richer error messages, include schema/version metadata in exports
- Add tests for edge cases (empty lists, Unicode, large payloads) and support additional formats (ndjson, parquet) in future
- Ensure logging and instrumentation for large exports and implement configurable field selection and ordering

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

import json
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class ImprovementExporter:
    """Exports improvements to json/csv."""

    def __init__(self) -> None:
        self.formats: list[str] = ["json", "csv"]

    def export(self, improvements: list[Improvement], output_format: str = "json") -> str:
        fmt = output_format.lower()
        if fmt == "json":
            rows: list[dict[str, Any]] = []
            for imp in improvements:
                rows.append(
                    {
                        "id": imp.id,
                        "title": imp.title,
                        "description": imp.description,
                    }
                )
            return json.dumps(rows)
        if fmt == "csv":
            lines = ["id,title,description"]
            for imp in improvements:
                lines.append(f"{imp.id},{imp.title},{imp.description}")
            return "\n".join(lines)
        raise ValueError("Unsupported format")
