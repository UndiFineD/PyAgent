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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_test_utils.py"""




from typing import Dict, Set

class CoverageTracker:
    """Lightweight coverage hit tracker used by tests."""

    def __init__(self) -> None:
        self._hits: Dict[str, int] = {}
        self._targets: Set[str] = set()

    def register_target(self, name: str) -> None:
        self._targets.add(name)

    def record_hit(self, name: str) -> None:
        self._hits[name] = self._hits.get(name, 0) + 1

    def get_hits(self) -> Dict[str, int]:
        return dict(self._hits)

    def get_percentage(self) -> float:
        if not self._targets:
            return 0.0
        covered = sum(1 for t in self._targets if self._hits.get(t, 0) > 0)
        return (covered / len(self._targets)) * 100.0
