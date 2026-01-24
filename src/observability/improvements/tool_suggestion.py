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

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .analysis_tool_type import AnalysisToolType

__version__ = VERSION


@dataclass
class ToolSuggestion:
    """Suggestion from a code analysis tool.

    Attributes:
        tool_type: Type of analysis tool.
        tool_name: Name of the specific tool.
        file_path: File with the issue.
        line_number: Line number of the issue.
        message: Suggestion message.
        suggested_fix: Optional code fix.
    """

    tool_type: AnalysisToolType
    tool_name: str
    file_path: str
    line_number: int
    message: str
    suggested_fix: str = ""
