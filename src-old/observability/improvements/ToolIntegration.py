#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/observability/improvements/ToolIntegration.description.md

# ToolIntegration

**File**: `src\observability\improvements\ToolIntegration.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 115  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `ToolIntegration`

Integrates with code analysis tools for suggestions.

Parses output from linters, type checkers, and other tools.

Attributes:
    tool_configs: Configuration for each tool.
    suggestions: List of tool suggestions.

**Methods** (6):
- `__init__(self)`
- `configure_tool(self, tool_name, tool_type, command)`
- `parse_pylint_output(self, output)`
- `parse_mypy_output(self, output)`
- `get_suggestions(self, tool_type)`
- `convert_to_improvements(self, suggestions)`

## Dependencies

**Imports** (10):
- `AnalysisToolType.AnalysisToolType`
- `ImprovementCategory.ImprovementCategory`
- `ToolSuggestion.ToolSuggestion`
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/improvements/ToolIntegration.improvements.md

# Improvements for ToolIntegration

**File**: `src\observability\improvements\ToolIntegration.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 115 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ToolIntegration_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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


"""Auto-extracted class from agent_improvements.py"""

import re
from typing import Any

from src.core.base.version import VERSION

from .AnalysisToolType import AnalysisToolType
from .ImprovementCategory import ImprovementCategory
from .ToolSuggestion import ToolSuggestion

__version__ = VERSION


class ToolIntegration:
    """Integrates with code analysis tools for suggestions.

    Parses output from linters, type checkers, and other tools.

    Attributes:
        tool_configs: Configuration for each tool.
        suggestions: List of tool suggestions.

    """

    def __init__(self) -> None:
        """Initialize tool integration."""
        self.tool_configs: dict[str, dict[str, Any]] = {}
        self.suggestions: list[ToolSuggestion] = []

    def configure_tool(
        self, tool_name: str, tool_type: AnalysisToolType, command: str = ""
    ) -> None:
        """Configure a tool.

        Args:
            tool_name: Name of the tool (e.g., "pylint").
            tool_type: Type of the tool.
            command: Command to run the tool.

        """
        self.tool_configs[tool_name] = {"type": tool_type, "command": command}

    def parse_pylint_output(self, output: str) -> list[ToolSuggestion]:
        """Parse pylint output into suggestions."""
        suggestions: list[ToolSuggestion] = []
        for line in output.split("\n"):
            match = re.match(r"(.+):(\d+):\d+: (\w+): (.+)", line)
            if match:
                suggestions.append(
                    ToolSuggestion(
                        tool_type=AnalysisToolType.LINTER,
                        tool_name="pylint",
                        file_path=match.group(1),
                        line_number=int(match.group(2)),
                        message=match.group(4),
                    )
                )
        self.suggestions.extend(suggestions)
        return suggestions

    def parse_mypy_output(self, output: str) -> list[ToolSuggestion]:
        """Parse mypy output into suggestions."""
        suggestions: list[ToolSuggestion] = []
        for line in output.split("\n"):
            match = re.match(r"(.+):(\d+): error: (.+)", line)
            if match:
                suggestions.append(
                    ToolSuggestion(
                        tool_type=AnalysisToolType.TYPE_CHECKER,
                        tool_name="mypy",
                        file_path=match.group(1),
                        line_number=int(match.group(2)),
                        message=match.group(3),
                    )
                )
        self.suggestions.extend(suggestions)
        return suggestions

    def get_suggestions(
        self, tool_type: AnalysisToolType | None = None
    ) -> list[ToolSuggestion]:
        """Get all tool suggestions."""
        if tool_type:
            return [s for s in self.suggestions if s.tool_type == tool_type]
        return self.suggestions

    def convert_to_improvements(
        self, suggestions: list[ToolSuggestion]
    ) -> list[dict[str, Any]]:
        """Convert tool suggestions to improvement data."""
        return [
            {
                "title": f"Fix {s.tool_name} issue in {s.file_path}",
                "description": s.message,
                "file_path": s.file_path,
                "line_number": s.line_number,
                "category": ImprovementCategory.MAINTAINABILITY.value,
            }
            for s in suggestions
        ]
