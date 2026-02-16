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
Tool Integration - Parse and convert static-analysis outputs into structured improvement suggestions

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ToolIntegration, call configure_tool(...) to register tools and their run commands, then parse tool outputs with parse_pylint_output(...) or parse_mypy_output(...).
- Retrieve accumulated suggestions with get_suggestions() and convert them to improvement records with convert_to_improvements(...) for downstream workflows (automated fixes, issue creation, reporting).

WHAT IT DOES:
- Provides a thin adapter around static-analysis outputs (pylint, mypy) that extracts file, line and message information into ToolSuggestion objects and stores them.
- Stores simple tool configuration metadata and exposes filtering by AnalysisToolType.
- Converts accumulated suggestions into a minimal improvement dict structure categorized as MAINTAINABILITY for integration with the rest of the PyAgent pipeline.

WHAT IT SHOULD DO BETTER:
- Robustness: current parsers use brittle regexes and simple line-splitting; add multi-line message support, stderr capture, and tolerant parsing for other output formats (JSON, XML) or tool versions.
- Extensibility: implement a pluggable parser registry rather than hard-coded parse_* methods, and support asynchronous execution and collection of tool runs.
- Context and severity: enrich suggestions with severity, rule id, and contextual code snippets; map tool rule IDs to human-friendly remediation steps and to precise ImprovementCategory values.
- Error handling & testing: validate and surface malformed lines, add unit tests for varied tool outputs, and log parsing failures with actionable diagnostics.
- Configuration: persist and validate tool configurations, support command templates and environment isolation when invoking tools.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

import re
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .analysis_tool_type import AnalysisToolType
from .improvement_category import ImprovementCategory
from .tool_suggestion import ToolSuggestion

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

    def configure_tool(self, tool_name: str, tool_type: AnalysisToolType, command: str = "") -> None:
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
            match = re.match(r"(.+):(\\\\d+):\\\\d+: (\w+): (.+)", line)
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
            match = re.match(r"(.+):(\\\\d+): error: (.+)", line)
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

    def get_suggestions(self, tool_type: AnalysisToolType | None = None) -> list[ToolSuggestion]:
        """Get all tool suggestions."""
        if tool_type:
            return [s for s in self.suggestions if s.tool_type == tool_type]
        return self.suggestions

    def convert_to_improvements(self, suggestions: list[ToolSuggestion]) -> list[dict[str, Any]]:
        """Convert tool suggestions to improvement data."""
        return [
            {
                "title": f"Fix {s.tool_name} issue in {s.file_path}",
                "description": s.message,
                "file_path": s.file_path,
                "line_number": s.line_number,
                "category": ImprovementCategory.MAINTAINABILITY.value,
            }
  """          for s in suggestions
        ]
"""

from __future__ import annotations

import re
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .analysis_tool_type import AnalysisToolType
from .improvement_category import ImprovementCategory
from .tool_suggestion import ToolSuggestion

__version__ = VERSION


class ToolIntegration:
    """Integrates with code analysis tools for suggestions.

    Parses output from linters, type checkers, and other tools.

    Attributes:
        tool_configs: Configuration for each tool.
       """ sugge"""sti"""ons: List of tool suggestions.
    """

    def __init__(self) -> None:
        """Initialize tool integration."""
        self""".to"""ol_configs: dict[str, dict[str, Any]] = {}
        self.suggestions: list[ToolSuggestion] = []

    def configure_tool(self, tool_name: str, tool_typ"""e: AnalysisToolType, comma"""nd: st"""r = "") -> None:
        """Configure a tool.

        Args:
            tool_name: Name of the tool (e.g., "pylint").
            tool_type: Type of the tool.
            command: Command to run the tool.
        """
        self.tool_config"""s[tool"""_name] = {"type": tool_type, "command": command}

    def parse_pylint_output(self, output: str) -> list[ToolSuggestion]:
        """Parse pylint output into sugge"""stions"""."""
        suggestions: list[ToolSuggestion] = []
        for line in output.split("\n"):
            match = re.match(r"(.+):(\\\\d+):\\\\d+: (\w+): (.+)", line)
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
        """Parse mypy output into su"""ggesti"""ons."""
        suggestions: list[ToolSuggestion] = []
        for line in output.split("\n"):
            match = re.match(r"(.+):(\\\\d+): error: (.+)", line)
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

    def get_suggestions(self, tool_type: AnalysisToolType | None = None) -> list[ToolSuggestion]""":
    """    """Get all tool suggestions."""
        if tool_type:
            return [s for s in self.suggestions if s.tool_type == tool_type]
        return self.suggestions

    def convert_to_improvements(self, suggestions: list[ToolSuggestion]) -> list[dict[str, Any]]:
        Conve"""rt tool suggestions to improvement data."""
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
