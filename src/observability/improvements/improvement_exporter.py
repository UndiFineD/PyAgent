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
from src.core.base.version import VERSION
from .Improvement import Improvement
from typing import Any, Dict, List
import json

__version__ = VERSION

class ImprovementExporter:
    """Exports improvements to json/csv."""

    def __init__(self) -> None:
        self.formats: list[str] = ["json", "csv"]

    def export(self, improvements: list[Improvement], format: str = "json") -> str:
        fmt = format.lower()
        if fmt == "json":
            rows: list[dict[str, Any]] = []
            for imp in improvements:
                rows.append({
                    "id": imp.id,
                    "title": imp.title,
                    "description": imp.description,
                })
            return json.dumps(rows)
        if fmt == "csv":
            lines = ["id,title,description"]
            for imp in improvements:
                lines.append(f"{imp.id},{imp.title},{imp.description}")
            return "\n".join(lines)
        raise ValueError("Unsupported format")