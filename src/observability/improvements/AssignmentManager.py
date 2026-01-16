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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from datetime import datetime
from typing import Any

__version__ = VERSION


class AssignmentManager:
    """Tracks assignees and ownership history."""

    def __init__(self) -> None:
        self.assignments: dict[str, str] = {}
        self._history: dict[str, list[dict[str, Any]]] = {}

    def assign(self, improvement_id: str, assignee: str) -> None:
        self.assignments[improvement_id] = assignee
        self._history.setdefault(improvement_id, []).append(
            {"assignee": assignee, "timestamp": datetime.now().isoformat()}
        )

    def get_assignee(self, improvement_id: str) -> str | None:
        return self.assignments.get(improvement_id)

    def get_ownership_history(self, improvement_id: str) -> list[dict[str, Any]]:
        return list(self._history.get(improvement_id, []))
