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


"""
Assignment Manager - Tracks assignees and ownership history

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.assignment_manager import AssignmentManager

mgr = AssignmentManager()
mgr.assign("impr-123", "alice")
current = mgr.get_assignee("impr-123")
history = mgr.get_ownership_history("impr-123")

WHAT IT DOES:
- Provides an in-memory registry mapping improvement IDs to current assignees.
- Records a timestamped ownership history for each improvement when assign() is called.
- Exposes simple query methods to retrieve the current assignee and the recorded history.

WHAT IT SHOULD DO BETTER:
- Persist assignments and history to durable storage (filesystem, database, or StateTransaction) so ownership survives process restarts.
- Be thread/process-safe (use locks or an async-safe design) and support async APIs to fit the project's asyncio convention.
- Use timezone-aware timestamps (e.g., datetime.now(tz=timezone.utc).isoformat()), stronger typing (TypedDict for history entries), and validation of improvement_id and assignee values.
- Add unassign/remove operations, ability to merge histories, pagination for long histories, and export/import (JSON) helpers.
- Integrate with CascadeContext/agent state manager and the project's Core/Agent separation: move domain logic into a core class and keep this class an orchestration shim.
- Add unit tests, docstrings on public methods, and consider replacing dict[str, str] with a small data class for clarity.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

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
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

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
