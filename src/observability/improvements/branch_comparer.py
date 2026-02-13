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
Branch Comparer - Compare improvements between Git branches

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate BranchComparer with an optional repo_path and optional recorder. Call compare(source_branch, target_branch, file_path) to obtain a BranchComparison with diffs and counts. Example: comparer = BranchComparer(repo_path="C:\repo"); result = comparer.compare("main", "feature/improvements", "improvements.yaml")

WHAT IT DOES:
Provides tooling to fetch a file from two git branches, parse improvement entries, and compute added/removed/modified ImprovementDiffs; records comparison history and optional recorder interactions; returns a BranchComparison with status and counts.

WHAT IT SHOULD DO BETTER:
- Improve error handling to surface useful exception details and partial results instead of swallowing broad exceptions.  
- Add unit tests and validation for parsing logic and git access to avoid silent empty-file fallbacks.  
- Support configurable git command timeouts, authentication contexts, binary/large-file handling, and richer diff heuristics (e.g., semantic diffing, rename detection).

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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

import hashlib
import logging
import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .branch_comparison import BranchComparison
from .branch_comparison_status import BranchComparisonStatus
from .improvement import Improvement
from .improvement_diff import ImprovementDiff
from .improvement_diff_type import ImprovementDiffType

__version__ = VERSION


class BranchComparer:
    """Comparer for improvements across git branches.

    Enables comparison of improvement files between branches
    to identify additions, removals, and modifications.

    Attributes:
        repo_path: Path to git repository.
        comparisons: History of comparisons.

    Example:
        comparer=BranchComparer("/path / to / repo")
        result=comparer.compare("main", "feature / improvements")
        for diff in result.diffs:
            print(f"{diff.diff_type.value}: {diff.improvement_id}")
    """

    def __init__(self, repo_path: str | None = None, recorder: Any = None) -> None:
        """Initialize branch comparer.

        Args:
            repo_path: Path to git repository. Defaults to current directory.
            recorder: Optional LocalContextRecorder.
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.recorder = recorder
        self.comparisons: list[BranchComparison] = []

    def _record(self, action: str, result: str) -> None:
        """Record branch comparison activities."""
        if self.recorder:
            self.recorder.record_interaction("Git", "BranchComparer", action, result)
        logging.debug(f"BranchComparer initialized for {self.repo_path}")

    def compare(self, source_branch: str, target_branch: str, file_path: str) -> BranchComparison:
        """Compare improvements between branches.

        Args:
            source_branch: Source branch name.
            target_branch: Target branch name.
            file_path: Path to improvements file.

        Returns:
            Comparison result with diffs.
        """
        comparison = BranchComparison(
            source_branch=source_branch,
            target_branch=target_branch,
            file_path=file_path,
            status=BranchComparisonStatus.IN_PROGRESS,
        )

        try:
            # Get file content from each branch
            source_content = self._get_file_from_branch(source_branch, file_path)
            target_content = self._get_file_from_branch(target_branch, file_path)

            # Parse improvements from each branch
            source_improvements = self._parse_improvements(source_content)
            target_improvements = self._parse_improvements(target_content)

            # Calculate differences
            comparison.diffs = self._calculate_diffs(source_improvements, target_improvements)

            # Count by type
            comparison.added_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.ADDED)
            comparison.removed_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.REMOVED)
            comparison.modified_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.MODIFIED)

            comparison.status = BranchComparisonStatus.COMPLETED

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Branch comparison failed: {e}")
            comparison.status = BranchComparisonStatus.FAILED

        self.comparisons.append(comparison)
        return comparison

    def _get_file_from_branch(self, branch: str, file_path: str) -> str:
        """Get file content from a specific branch.

        Args:
            branch: Branch name.
            file_path: Path to file.

        Returns:
            File content string.
        """
        try:
            result = subprocess.run(
                ["git", "show", f"{branch}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def _parse_improvements(self, content: str) -> dict[str, Improvement]:
"""

from __future__ import annotations

import hashlib
import logging
import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .branch_comparison import BranchComparison
from .branch_comparison_status import BranchComparisonStatus
from .improvement import Improvement
from .improvement_diff import ImprovementDiff
from .improvement_diff_type import ImprovementDiffType

__version__ = VERSION


class BranchComparer:
    """Comparer for improvements across git branches.

    Enables comparison of improvement files between branches
    to identify additions, removals, and modifications.

    Attributes:
        repo_path: Path to git repository.
        comparisons: History of comparisons.

    Example:
        comparer=BranchComparer("/path / to / repo")
        result=comparer.compare("main", "feature / improvements")
        for diff in result.diffs:
            print(f"{diff.diff_type.value}: {diff.improvement_id}")
    """

    def __init__(self, repo_path: str | None = None, recorder: Any = None) -> None:
        """Initialize branch comparer.

        Args:
            repo_path: Path to git repository. Defaults to current directory.
            recorder: Optional LocalContextRecorder.
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.recorder = recorder
        self.comparisons: list[BranchComparison] = []

    def _record(self, action: str, result: str) -> None:
        """Record branch comparison activities."""
        if self.recorder:
            self.recorder.record_interaction("Git", "BranchComparer", action, result)
        logging.debug(f"BranchComparer initialized for {self.repo_path}")

    def compare(self, source_branch: str, target_branch: str, file_path: str) -> BranchComparison:
        """Compare improvements between branches.

        Args:
            source_branch: Source branch name.
            target_branch: Target branch name.
            file_path: Path to improvements file.

        Returns:
            Comparison result with diffs.
        """
        comparison = BranchComparison(
            source_branch=source_branch,
            target_branch=target_branch,
            file_path=file_path,
            status=BranchComparisonStatus.IN_PROGRESS,
        )

        try:
            # Get file content from each branch
            source_content = self._get_file_from_branch(source_branch, file_path)
            target_content = self._get_file_from_branch(target_branch, file_path)

            # Parse improvements from each branch
            source_improvements = self._parse_improvements(source_content)
            target_improvements = self._parse_improvements(target_content)

            # Calculate differences
            comparison.diffs = self._calculate_diffs(source_improvements, target_improvements)

            # Count by type
            comparison.added_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.ADDED)
            comparison.removed_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.REMOVED)
            comparison.modified_count = sum(1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.MODIFIED)

            comparison.status = BranchComparisonStatus.COMPLETED

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Branch comparison failed: {e}")
            comparison.status = BranchComparisonStatus.FAILED

        self.comparisons.append(comparison)
        return comparison

    def _get_file_from_branch(self, branch: str, file_path: str) -> str:
        """Get file content from a specific branch.

        Args:
            branch: Branch name.
            file_path: Path to file.

        Returns:
            File content string.
        """
        try:
            result = subprocess.run(
                ["git", "show", f"{branch}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def _parse_improvements(self, content: str) -> dict[str, Improvement]:
        """Parse improvements from markdown content.

        Args:
            content: Markdown content with improvements.

        Returns:
            Dictionary mapping improvement IDs to Improvement objects.
        """
        improvements: dict[str, Improvement] = {}

        # Parse improvement items from markdown
        pattern = r"- \[[ x]\] (.+?)(?=\n- \[|\n##|\Z)"
        matches = re.findall(pattern, content, re.DOTALL)

        for i, match in enumerate(matches):
            title = match.strip().split("\n")[0]
            improvement_id = f"imp_{i}_{hashlib.md5(title.encode()).hexdigest()[:8]}"

            improvements[improvement_id] = Improvement(
                id=improvement_id, title=title, description=match.strip(), file_path=""
            )

        return improvements

    def _calculate_diffs(
        self, source: dict[str, Improvement], target: dict[str, Improvement]
    ) -> list[ImprovementDiff]:
        """Calculate differences between two improvement sets.

        Args:
            source: Source branch improvements.
            target: Target branch improvements.

        Returns:
            List of improvement differences.
        """
        diffs: list[ImprovementDiff] = []
        all_ids = set(source.keys()) | set(target.keys())

        for imp_id in all_ids:
            in_source = imp_id in source
            in_target = imp_id in target

            if in_source and not in_target:
                diffs.append(
                    ImprovementDiff(
                        improvement_id=imp_id,
                        diff_type=ImprovementDiffType.REMOVED,
                        source_version=source[imp_id],
                        change_summary="Improvement removed in target branch",
                    )
                )
            elif in_target and not in_source:
                diffs.append(
                    ImprovementDiff(
                        improvement_id=imp_id,
                        diff_type=ImprovementDiffType.ADDED,
                        target_version=target[imp_id],
                        change_summary="New improvement in target branch",
                    )
                )
            elif source[imp_id].title != target[imp_id].title:
                diffs.append(
                    ImprovementDiff(
                        improvement_id=imp_id,
                        diff_type=ImprovementDiffType.MODIFIED,
                        source_version=source[imp_id],
                        target_version=target[imp_id],
                        change_summary="Improvement title or content changed",
                    )
                )
            else:
                diffs.append(
                    ImprovementDiff(
                        improvement_id=imp_id,
                        diff_type=ImprovementDiffType.UNCHANGED,
                        source_version=source[imp_id],
                        target_version=target[imp_id],
                        change_summary="No changes",
                    )
                )

        return diffs

    def get_added_improvements(self, comparison: BranchComparison) -> list[Improvement]:
        """Get improvements added in target branch.

        Args:
            comparison: Comparison result.

        Returns:
            List of added improvements.
        """
        return [
            d.target_version for d in comparison.diffs if d.diff_type == ImprovementDiffType.ADDED and d.target_version
        ]

    def get_removed_improvements(self, comparison: BranchComparison) -> list[Improvement]:
        """Get improvements removed in target branch.

        Args:
            comparison: Comparison result.

        Returns:
            List of removed improvements.
        """
        return [
            d.source_version
            for d in comparison.diffs
            if d.diff_type == ImprovementDiffType.REMOVED and d.source_version
        ]

    def get_modified_improvements(self, comparison: BranchComparison) -> list[tuple[Improvement, Improvement]]:
        """Get improvements modified between branches.

        Args:
            comparison: Comparison result.

        Returns:
            List of (source, target) improvement tuples.
        """
        return [
            (d.source_version, d.target_version)
            for d in comparison.diffs
            if d.diff_type == ImprovementDiffType.MODIFIED and d.source_version and d.target_version
        ]

    def detect_conflicts(self, base_branch: str, branch1: str, branch2: str, file_path: str) -> list[ImprovementDiff]:
        """Detect conflicting changes in a three-way comparison.

        Args:
            base_branch: Common ancestor branch.
            branch1: First branch.
            branch2: Second branch.
            file_path: Path to improvements file.

        Returns:
            List of conflicting improvement diffs.
        """
        comp1 = self.compare(base_branch, branch1, file_path)
        comp2 = self.compare(base_branch, branch2, file_path)

        # Find improvements modified in both branches
        modified1 = {d.improvement_id for d in comp1.diffs if d.diff_type == ImprovementDiffType.MODIFIED}
        modified2 = {d.improvement_id for d in comp2.diffs if d.diff_type == ImprovementDiffType.MODIFIED}

        conflicts = modified1 & modified2
        return [d for d in comp1.diffs if d.improvement_id in conflicts]

    def generate_merge_report(self, comparison: BranchComparison) -> str:
        """Generate a markdown merge report.

        Args:
            comparison: Comparison result.

        Returns:
            Markdown formatted report.
        """
        lines = [
            "# Branch Comparison Report",
            "",
            f"**Source Branch:** {comparison.source_branch}",
            f"**Target Branch:** {comparison.target_branch}",
            f"**File:** {comparison.file_path}",
            "",
            "## Summary",
            f"- Added: {comparison.added_count}",
            f"- Removed: {comparison.removed_count}",
            f"- Modified: {comparison.modified_count}",
            "",
            "## Changes",
        ]

        for diff in comparison.diffs:
            if diff.diff_type == ImprovementDiffType.UNCHANGED:
                continue

            emoji = {
                ImprovementDiffType.ADDED: "➕",
                ImprovementDiffType.REMOVED: "➖",
                ImprovementDiffType.MODIFIED: "📝",
            }.get(diff.diff_type, "•")

            title = (
                diff.target_version.title
                if diff.target_version
                else diff.source_version.title
                if diff.source_version
                else diff.improvement_id
            )
            lines.append(f"- {emoji} {title}")

        return "\n".join(lines)

    def get_comparison_history(self) -> list[BranchComparison]:
        """Get history of comparisons.

        Returns:
            List of past comparisons.
        """
        return list(self.comparisons)

    def clear_history(self) -> None:
        """Clear comparison history."""
        self.comparisons.clear()
