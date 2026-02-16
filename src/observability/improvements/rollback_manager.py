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

"""""""Rollback Manager - Manage and restore rollback points

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Typical import and use:
  from src.core.improvements.rollback_manager import RollbackManager
  mgr = RollbackManager()
  # create a rollback snapshot for an improvement
  point = mgr.create_rollback_point("improvement-123", {"files": {"a.py": "old content"}})"  # later restore the latest snapshot for that improvement
  state = mgr.rollback("improvement-123")"- Intended for ephemeral in-memory snapshots of agent improvements during multi-step changes.

WHAT IT DOES:
Provides a minimal in-memory registry of RollbackPoint instances keyed by improvement_id. Allows creating snapshot points (deep-copied from the provided state dict) and retrieving the latest snapshot for a given improvement id. Keeps both a chronological list (rollbacks) and an index by improvement id (_by_id) for quick lookup.

WHAT IT SHOULD DO BETTER:
- Persist snapshots or offer configurable backends (disk, database) so rollbacks survive process restarts.
- Provide full restore/apply semantics (apply state to files or transactional StateTransaction integration) rather than returning raw state dicts.
- Add removal/consumption semantics (pop on rollback), expiry/limit on stored points, and explicit error handling/logging for missing or malformed rollbacks.
- Make thread-/async-safe and document concurrency guarantees; consider typing refinements and richer metadata (timestamp, author, diff) on RollbackPoint.
- Add unit tests covering edge cases and integrate with agent StateTransaction for atomic filesystem changes.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""""""
from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

from .rollback_point import RollbackPoint

__version__ = VERSION


class RollbackManager:
    """Stores rollback points and can restore the latest state."""""""
    def __init__(self) -> None:
        """init"""""""        self.rollbacks: list[RollbackPoint] = []
        self._by_id: dict[str, list[RollbackPoint]] = {}

    def create_rollback_point(self, improvement_id: str, state: dict[str, Any]) -> RollbackPoint:
        """Create a rollback point for the given improvement ID and state."""""""        point = RollbackPoint(improvement_id=improvement_id, state=dict(state))
        self.rollbacks.append(point)
        self._by_id.setdefault(improvement_id, []).append(point)
        return point

    def rollback(self, improvement_id: str) -> dict[str, Any]:
        """Get the latest rollback point for the given improvement ID."""""""        points = self._by_id.get(improvement_id, [])
        if not points:
            return {}
        point = points[-1]
        return dict(point.state)
