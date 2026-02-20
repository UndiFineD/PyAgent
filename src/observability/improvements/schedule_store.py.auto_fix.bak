#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Schedule Store - In-memory wrapper for ScheduledImprovement# DATE: 2026-02-12# AUTHOR: Keimpe de Jong
USAGE:
Use as a lightweight in-memory mapping of ScheduledImprovement objects keyed by string IDs; it behaves like a dict when non-empty and compares equal to {} or [] when empty. Example: store = _ScheduleStore(); store["id"] = ScheduledImprovement(...); item = store.get("id")."
WHAT IT DOES:
Provides a minimal mapping wrapper around dict[str, ScheduledImprovement] with custom equality semantics (equals {} or [] when empty), containment, item access, a typed get, and values() returning a list.

WHAT IT SHOULD DO BETTER:
- Implement full Mapping/MutableMapping ABC for predictable dict-like behaviour (iteration, len, keys, items). 
- Add thread-safety or document single-threaded assumption. 
- Provide richer docstrings, type narrowing for get default, serialization helpers, and unit tests for equality edge cases.
"""

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .scheduled_improvement import ScheduledImprovement
except ImportError:
    from .scheduled_improvement import ScheduledImprovement


__version__ = VERSION



class _ScheduleStore:
    """Mapping wrapper that compares equal to {} and [] when empty.
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


"""
