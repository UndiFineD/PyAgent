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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .IssueCategory import IssueCategory
from .SeverityLevel import SeverityLevel
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class CodeIssue:
    """Represents a code issue or improvement suggestion.
    Attributes:
        message: Issue description.
        category: Issue category.
        severity: Severity level.
        line_number: Line number if applicable.
        file_path: File path if applicable.
        function_name: Function name if applicable.
    """

    message: str
    category: IssueCategory
    severity: SeverityLevel = SeverityLevel.INFO
    line_number: int | None = None
    file_path: str | None = None
    function_name: str | None = None
