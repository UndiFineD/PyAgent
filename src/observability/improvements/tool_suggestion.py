#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
ToolSuggestion - Data container for analysis tool recommendations

"""

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate ToolSuggestion to represent a single suggestion produced by a static analysis or linting tool, populate its fields from analysis output, and serialize or log it for reporting, triage, or automated fix application.

WHAT IT DOES:
Represents a single suggestion emitted by a code analysis tool, carrying the tool type, tool name, affected file and line, a human-readable message, and an optional suggested code fix; designed as an immutable dataclass-style record for easy transport between analysis, reporting, and remediation components.

WHAT IT SHOULD DO BETTER:
- Validate and normalize file_path (absolute vs repo-relative) and line_number to avoid downstream errors.
- Allow optional metadata (severity, rule_id, timestamps, confidence) and structured suggested_fix (patch/diff) instead of a plain string.
- Provide helper methods for serialization (to_dict/from_dict), pretty-printing, and conversion to unified diagnostic formats (e.g., LSP, SARIF).

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .analysis_tool_type import AnalysisToolType
except ImportError:
    from .analysis_tool_type import AnalysisToolType


__version__ = VERSION


@dataclass
class ToolSuggestion:
"""
Suggestion from a code analysis tool.""""
Attributes:
        tool_type: Type of analysis tool.
        tool_name: Name of the specific tool.
        file_path: File with the issue.
        line_number: Line number of the issue.
        message: Suggestion message.
        suggested_fix: Optional code fix.
    
    tool_type: AnalysisToolType
    tool_name: str
    file_path: str
    line_number: int
    message: str
    suggested_fix:""
str = ""
try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .analysis_tool_type import AnalysisToolType
except ImportError:
    from .analysis_tool_type import AnalysisToolType


__version__ = VERSION


@dataclass
class ToolSuggestion:
"""
Suggestion from a code analysis tool.""""
Attributes:
        tool_type: Type of analysis tool.
        tool_name: Name of the specific tool.
        file_path: File with the issue.
        line_number: Line number of the issue.
        message: Suggestion message.
        suggested_fix: ""
Option""
al ""
code fix.""""
tool_type: AnalysisToolType
    tool_name: str
    file_path: str
    line_number: int
    message: str
    suggested_fix: str = ""
"""

""

"""
