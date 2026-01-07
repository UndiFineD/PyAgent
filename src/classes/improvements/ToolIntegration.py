#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .AnalysisToolType import AnalysisToolType
from .ImprovementCategory import ImprovementCategory
from .ToolSuggestion import ToolSuggestion

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time

class ToolIntegration:
    """Integrates with code analysis tools for suggestions.

    Parses output from linters, type checkers, and other tools.

    Attributes:
        tool_configs: Configuration for each tool.
        suggestions: List of tool suggestions.
    """

    def __init__(self) -> None:
        """Initialize tool integration."""
        self.tool_configs: Dict[str, Dict[str, Any]] = {}
        self.suggestions: List[ToolSuggestion] = []

    def configure_tool(
        self,
        tool_name: str,
        tool_type: AnalysisToolType,
        command: str = ""
    ) -> None:
        """Configure a tool.

        Args:
            tool_name: Name of the tool (e.g., "pylint").
            tool_type: Type of the tool.
            command: Command to run the tool.
        """
        self.tool_configs[tool_name] = {
            "type": tool_type,
            "command": command
        }

    def parse_pylint_output(self, output: str) -> List[ToolSuggestion]:
        """Parse pylint output into suggestions."""
        suggestions: List[ToolSuggestion] = []
        for line in output.split('\n'):
            match = re.match(
                r'(.+):(\d+):\d+: (\w+): (.+)',
                line
            )
            if match:
                suggestions.append(ToolSuggestion(
                    tool_type=AnalysisToolType.LINTER,
                    tool_name="pylint",
                    file_path=match.group(1),
                    line_number=int(match.group(2)),
                    message=match.group(4)
                ))
        self.suggestions.extend(suggestions)
        return suggestions

    def parse_mypy_output(self, output: str) -> List[ToolSuggestion]:
        """Parse mypy output into suggestions."""
        suggestions: List[ToolSuggestion] = []
        for line in output.split('\n'):
            match = re.match(r'(.+):(\d+): error: (.+)', line)
            if match:
                suggestions.append(ToolSuggestion(
                    tool_type=AnalysisToolType.TYPE_CHECKER,
                    tool_name="mypy",
                    file_path=match.group(1),
                    line_number=int(match.group(2)),
                    message=match.group(3)
                ))
        self.suggestions.extend(suggestions)
        return suggestions

    def get_suggestions(
        self, tool_type: Optional[AnalysisToolType] = None
    ) -> List[ToolSuggestion]:
        """Get all tool suggestions."""
        if tool_type:
            return [s for s in self.suggestions
                    if s.tool_type == tool_type]
        return self.suggestions

    def convert_to_improvements(
        self, suggestions: List[ToolSuggestion]
    ) -> List[Dict[str, Any]]:
        """Convert tool suggestions to improvement data."""
        return [{
            "title": f"Fix {s.tool_name} issue in {s.file_path}",
            "description": s.message,
            "file_path": s.file_path,
            "line_number": s.line_number,
            "category": ImprovementCategory.MAINTAINABILITY.value
        } for s in suggestions]
