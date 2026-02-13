#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Report Search Result - Dataclass representing a single report search hit

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.interface.reports.report_search_result import ReportSearchResult, ReportType
result = ReportSearchResult(
    file_path="reports/daily.md",
    report_type=ReportType.SUMMARY,
    match_text="error: connection refused",
    line_number=42,
    score=0.87,
)

WHAT IT DOES:
Provides a small, immutable container (dataclass) that models a single search hit within generated agent reports, holding the file path, report type enum, the matched snippet, the line number, and a relevance score.

WHAT IT SHOULD DO BETTER:
- Accept Path-like objects (pathlib.Path) instead of plain str for file_path and validate existence/get canonical path.
- Expose serialization helpers (to_dict/from_dict, JSON) and a concise display method for UIs.
- Normalize/validate score (0.0–1.0), add ordering by score, and include an optional context window around match_text.
- Add unit tests for equality, ordering, and serialization.

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

from src.core.base.lifecycle.version import VERSION

from .report_type import ReportType

__version__ = VERSION


@dataclass
class ReportSearchResult:
    """Result from report search.
    Attributes:
        file_path: Path to report file.
        report_type: Type of report.
        match_text: Matched text snippet.
        line_number: Line number of match.
        score: Relevance score.
    """

    file_path: str
    report_type: ReportType
    match_text: str
    line_number: int
    score: float = 1.0
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .report_type import ReportType

__version__ = VERSION


@dataclass
class ReportSearchResult:
    """Result from report search.
    Attributes:
        file_path: Path to report file.
        report_type: Type of report.
        match_text: Matched text snippet.
        line_number: Line number of match.
        score: Relevance score.
    """

    file_path: str
    report_type: ReportType
    match_text: str
    line_number: int
    score: float = 1.0
