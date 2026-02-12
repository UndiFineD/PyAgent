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
FilterCriteria - Report filtering core

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Construct a FilterCriteria instance to restrict report queries by date range, minimum severity, categories and file glob patterns.
- Example:
  from src.reports.filter_criteria import FilterCriteria
  criteria = FilterCriteria(date_from=datetime(2026,1,1), min_severity=SeverityLevel.MEDIUM, categories=[IssueCategory.BUG], file_patterns=["**/*.py"])

WHAT IT DOES:
Defines a small, immutable-friendly dataclass that encapsulates common filtering options used when assembling or applying report queries (date_from, date_to, min_severity, categories, file_patterns).

WHAT IT SHOULD DO BETTER:
- Validate and normalize inputs (e.g., ensure date_from <= date_to, enforce unique categories).
- Provide convenience constructors (from dict, from query params) and serialization helpers (to_dict, to_json).
- Support timezone-aware datetimes and richer file-matching semantics (exclude patterns, regex support).

FILE CONTENT SUMMARY:
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

from dataclasses import dataclass
from datetime import datetime

from src.core.base.lifecycle.version import VERSION

from .issue_category import IssueCategory
from .severity_level import SeverityLevel

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
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.core.base.lifecycle.version import VERSION

from .issue_category import IssueCategory
from .severity_level import SeverityLevel

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
