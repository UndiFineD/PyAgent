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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .snapshot_comparison_result import SnapshotComparisonResult
from .test_snapshot import TestSnapshot
from pathlib import Path
from typing import Any
import json

__version__ = VERSION


class SnapshotManager:
    """Manages snapshots for snapshot testing.

    Example:
        mgr=SnapshotManager(Path("snapshots"))
        mgr.assert_match("test1", actual_output)
    """

    def __init__(self, snapshot_dir: Path) -> None:
        """Initialize snapshot manager.

        Args:
            snapshot_dir: Directory to store snapshots.
        """
        self.snapshot_dir = snapshot_dir
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self._snapshots: dict[str, TestSnapshot] = {}

    def _get_snapshot_path(self, name: str) -> Path:
        """Get path for a snapshot."""
        return self.snapshot_dir / f"{name}.snap"

    def save_snapshot(self, name: str, content: Any) -> TestSnapshot:
        """Save a new snapshot.

        Args:
            name: Snapshot name.
            content: Snapshot content (str or dict/list).

        Returns:
            TestSnapshot: Created snapshot.
        """
        # Convert content to string for TestSnapshot
        if isinstance(content, str):
            content_str = content
            snapshot_content = content
        else:
            content_str = json.dumps(content, indent=2)
            snapshot_content = content_str

        path = self._get_snapshot_path(name)
        path.write_text(content_str, encoding="utf-8")
        snapshot = TestSnapshot(name=name, content=snapshot_content)
        self._snapshots[name] = snapshot
        return snapshot

    def load_snapshot(self, name: str) -> TestSnapshot | None:
        """Load an existing snapshot.

        Args:
            name: Snapshot name.

        Returns:
            The loaded TestSnapshot object or None.
        """
        path = self._get_snapshot_path(name)
        if not path.exists():
            return None

        content_str = path.read_text(encoding="utf-8")
        # Try to parse as JSON
        try:
            content = json.loads(content_str)
        except json.JSONDecodeError:
            content = content_str

        # Return TestSnapshot object with the loaded content
        snapshot = TestSnapshot(name=name, content=content)
        self._snapshots[name] = snapshot
        return snapshot

    def compare_snapshot(self, name: str, actual: Any) -> SnapshotComparisonResult:
        """Compare actual content with a saved snapshot.

        Args:
            name: Snapshot name.
            actual: Actual content to compare.

        Returns:
            SnapshotComparisonResult with comparison details.
        """
        expected_snapshot = self.load_snapshot(name)

        if expected_snapshot is None:
            return SnapshotComparisonResult(
                matches=False, expected=None, actual=actual, snapshot_name=name
            )

        # Compare the content
        matches = expected_snapshot.content == actual
        return SnapshotComparisonResult(
            matches=matches,
            expected=expected_snapshot.content,
            actual=actual,
            snapshot_name=name,
        )

    def assert_match(
        self,
        name: str,
        actual: str,
        update: bool = False,
    ) -> bool:
        """Assert that actual matches snapshot.

        Args:
            name: Snapshot name.
            actual: Actual content.
            update: Update snapshot if mismatch.

        Returns:
            bool: True if match, False otherwise.
        """
        expected = self.load_snapshot(name)

        if expected is None:
            # No snapshot exists, create it
            self.save_snapshot(name, actual)
            return True

        if expected.content == actual:
            return True

        if update:
            self.save_snapshot(name, actual)
            return True

        return False

    def get_diff(self, name: str, actual: str) -> list[str]:
        """Get diff between snapshot and actual.

        Args:
            name: Snapshot name.
            actual: Actual content.

        Returns:
            List[str]: Diff lines.
        """
        import difflib

        expected = self.load_snapshot(name)
        if expected is None:
            return ["No snapshot exists"]
        return list(
            difflib.unified_diff(
                expected.content.splitlines(),
                actual.splitlines(),
                fromfile=f"snapshot/{name}",
                tofile="actual",
                lineterm="",
            )
        )
