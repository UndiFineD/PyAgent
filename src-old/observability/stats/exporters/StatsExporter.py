#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/StatsExporter.description.md

# StatsExporter

**File**: `src\observability\stats\exporters\StatsExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 40  
**Complexity**: 2 (simple)

## Overview

Auto-extracted class from agent_stats.py

## Classes (1)

### `StatsExporter`

Exports stats in various formats.

**Methods** (2):
- `__init__(self, format)`
- `export(self, metrics, format)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/StatsExporter.improvements.md

# Improvements for StatsExporter

**File**: `src\observability\stats\exporters\StatsExporter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StatsExporter_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

from src.core.base.version import VERSION
from typing import Any, Dict, List, Optional
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
