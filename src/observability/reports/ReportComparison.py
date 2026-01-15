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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass, field

__version__ = VERSION




@dataclass
class ReportComparison:
    """Result of comparing two report versions.
    Attributes:
        old_path: Path to old version.
        new_path: Path to new version.
        added: Items added in new version.
        removed: Items removed from old version.
        changed: Items that changed (list of tuples of old, new).
        unchanged_count: Count of unchanged items.
    """

    old_path: str
    new_path: str
    added: list[str] = field(default_factory=list)  # type: ignore[assignment]
    removed: list[str] = field(default_factory=list)  # type: ignore[assignment]
    changed: list[tuple] = field(default_factory=list)  # type: ignore[assignment]
    unchanged_count: int = 0
