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

from src.core.base.lifecycle.version import VERSION

from .scheduled_improvement import ScheduledImprovement

__version__ = VERSION


class _ScheduleStore:
    """Mapping wrapper that compares equal to {} and [] when empty."""

    def __init__(self) -> None:
        self._data: dict[str, ScheduledImprovement] = {}

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict):
            return self._data == other
        if isinstance(other, list):
            return not other and not self._data
        return False

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> ScheduledImprovement:
        return self._data[key]

    def __setitem__(self, key: str, value: ScheduledImprovement) -> None:
        self._data[key] = value

    def get(self, key: str, default: ScheduledImprovement | None = None) -> ScheduledImprovement | None:
        return self._data.get(key, default)

    def values(self) -> list[ScheduledImprovement]:
        return list(self._data.values())
