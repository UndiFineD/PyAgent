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
from src.core.base.lifecycle.version import VERSION
from .analysis_tool_type import AnalysisToolType
from .improvement_category import ImprovementCategory
from .tool_suggestion import ToolSuggestion
from typing import Any
import re

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
