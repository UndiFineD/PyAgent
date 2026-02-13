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
ReportComparator - Compare report versions

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- From code: 
    comparator = ReportComparator(reports_dir=Path("reports/"))
    result = comparator.compare("old.md", "new.md", old_content, new_content)
    # result is a ReportComparison dataclass containing added/removed/changed/unchanged_count

WHAT IT DOES:
- Provides a small utility class ReportComparator that extracts markdown list items (lines starting with "- ") from two report versions and computes added, removed and unchanged counts returning a ReportComparison object.

WHAT IT SHOULD DO BETTER:
- Detect and report changed items (not only added/removed) by performing item-level fuzzy or token diffs.
- Normalize and parse markdown more robustly (support numbered lists, nested lists, checkboxes, variations in whitespace and bullet characters).
- Preserve item order, handle duplicates deterministically, and surface contextual diffs (unified diff or line ranges) for better traceability.
- Add input validation, logging, and unit tests; expose a CLI or higher-level API for directory comparisons and report discovery.

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
"""

from __future__ import annotations

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
