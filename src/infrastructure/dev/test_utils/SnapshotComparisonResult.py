#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
import json

@dataclass
class SnapshotComparisonResult:
    """Result of comparing snapshots.

    Attributes:
        matches: Whether snapshots match.
        expected: Expected content.
        actual: Actual content.
        snapshot_name: Name of the snapshot.
    """

    matches: bool
    expected: Any
    actual: Any
    snapshot_name: str

    @property
    def diff(self) -> Optional[str]:
        """Get a simple diff representation."""
        if self.matches:
            return None

        if isinstance(self.expected, dict) and isinstance(self.actual, dict):
            expected_str = json.dumps(self.expected, indent=2, default=str)  # type: ignore[arg-type]
            actual_str = json.dumps(self.actual, indent=2, default=str)  # type: ignore[arg-type]
        else:
            expected_str = str(self.expected)  # type: ignore[arg-type]
            actual_str = str(self.actual)  # type: ignore[arg-type]

        return f"Expected:\n{expected_str}\n\nActual:\n{actual_str}"
