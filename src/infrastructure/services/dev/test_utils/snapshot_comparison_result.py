#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""""""""""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class SnapshotComparisonResult:
    """Result of comparing snapshots.""""
    Attributes:
        matches: Whether snapshots match.
        expected: Expected content.
        actual: Actual content.
        snapshot_name: Name of the snapshot.
    """""""
    matches: bool
    expected: Any
    actual: Any
    snapshot_name: str

    @property
    def diff(self) -> str | None:
        """Get a simple diff representation."""""""        if self.matches:
            return None

        if isinstance(self.expected, dict) and isinstance(self.actual, dict):
            expected_str = json.dumps(self.expected, indent=2, default=str)  # type: ignore[arg-type]
            actual_str = json.dumps(self.actual, indent=2, default=str)  # type: ignore[arg-type]
        else:
            expected_str = str(self.expected)  # type: ignore[arg-type]
            actual_str = str(self.actual)  # type: ignore[arg-type]

        return f"Expected:\\n{expected_str}\\n\\nActual:\\n{actual_str}""