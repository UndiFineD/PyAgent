#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_comparator.description.md

# Description: src/observability/reports/report_comparator.py

Module overview:
- `ReportComparator` compares two report contents and returns a `ReportComparison` with added/removed/unchanged counts.
- Uses simple line-item extraction for markdown lists to determine differences.

Behavioral notes:
- Default `reports_dir` uses project `src/` root.
- The `_extract_items` method looks for markdown list items starting with `- `.
## Source: src-old/observability/reports/report_comparator.improvements.md

# Improvements: src/observability/reports/report_comparator.py

Potential improvements:
- Add unit tests that compare real report snippets and verify reported diffs.
- Improve diff detection to handle markdown variations and ignore ordering when appropriate.
- Provide options to produce unified diffs or side-by-side comparisons as output.

LLM_CONTEXT_END
"""

from __future__ import annotations

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


from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .report_comparison import ReportComparison

__version__ = VERSION

# Define AGENT_DIR for default parameter

AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/


class ReportComparator:
    """Compares report versions to show differences.

    Attributes:
        reports_dir: Directory containing reports.

    """

    def __init__(self, reports_dir: Path = AGENT_DIR) -> None:
        """Initialize comparator.

        Args:
            reports_dir: Directory containing report files.

        """
        self.reports_dir = reports_dir

    def compare(self, old_path: str, new_path: str, old_content: str, new_content: str) -> ReportComparison:
        """Compare two report versions.

        Args:
            old_path: Path to old version.
            new_path: Path to new version.
            old_content: Previous report content.
            new_content: New report content.

        Returns:
            ReportComparison with differences.

        """
        old_items = self._extract_items(old_content)
        new_items = self._extract_items(new_content)
        old_set = set(old_items)
        new_set = set(new_items)
        added = list(new_set - old_set)
        removed = list(old_set - new_set)
        unchanged = len(old_set & new_set)
        return ReportComparison(
            old_path=old_path,
            new_path=new_path,
            added=added,
            removed=removed,
            changed=[],
            unchanged_count=unchanged,
        )

    def _extract_items(self, content: str) -> list[str]:
        """Extract list items from markdown content."""
        items: list[str] = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                items.append(line)
        return items
