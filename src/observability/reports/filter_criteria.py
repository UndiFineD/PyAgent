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
from src.core.base.version import VERSION
from .IssueCategory import IssueCategory
from .SeverityLevel import SeverityLevel
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

__version__ = VERSION

@dataclass
class FilterCriteria:
    """Criteria for filtering reports.
    Attributes:
        date_from: Start date for filtering.
        date_to: End date for filtering.
        min_severity: Minimum severity level.
        categories: Categories to include.
        file_patterns: Glob patterns for files.
    """

    date_from: datetime | None = None
    date_to: datetime | None = None
    min_severity: SeverityLevel | None = None
    categories: list[IssueCategory] | None = None
    file_patterns: list[str] | None = None