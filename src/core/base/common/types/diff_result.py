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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass, field

__version__ = VERSION


@dataclass
class DiffResult:
    """Result of a changelog diff comparison.

    Attributes:
        additions: Lines added.
        deletions: Lines removed.
        modifications: Lines changed.
        unchanged: Lines unchanged.
        similarity_score: Percentage of similarity (0 - 100).
    """

    additions: list[str] = field(default_factory=lambda: [])
    deletions: list[str] = field(default_factory=lambda: [])
    modifications: list[tuple[str, str]] = field(default_factory=lambda: [])
    unchanged: int = 0
    similarity_score: float = 0.0
