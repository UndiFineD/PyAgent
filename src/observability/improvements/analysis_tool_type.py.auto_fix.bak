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
AnalysisToolType - Enumeration of analysis tool categories

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import AnalysisToolType from src.core.base.analysis_tool_type to classify or switch behavior by tool category
- Compare values with AnalysisToolType.LINTER, AnalysisToolType.TYPE_CHECKER, etc
- Use value attribute for storage or display, e.g., tool.type.value

WHAT IT DOES:
Defines a small, explicit Enum representing common static analysis tool categories used across the codebase so callers can rely on a single canonical set of identifiers

WHAT IT SHOULD DO BETTER:
- Add docstrings per member to clarify intended scope and examples for each category
- Provide utility helpers such as from_string, is_security_related, or grouping sets for composite checks
- Consider attaching metadata like default CLI names or common file extensions to support tooling integrations

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

try:
    from enum import Enum
except ImportError:
    from enum import Enum


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


class AnalysisToolType(Enum):
    """Types of code analysis tools.
    LINTER = "linter""    TYPE_CHECKER = "type_checker""    SECURITY_SCANNER = "security_scanner""    COVERAGE = "coverage""    COMPLEXITY = "complexity""