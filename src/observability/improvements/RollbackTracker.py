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
from src.core.base.Version import VERSION
from .Improvement import Improvement
from .RollbackRecord import RollbackRecord
from datetime import datetime
import json

__version__ = VERSION


class RollbackTracker:
    """Tracks improvement rollbacks.

    Records when and why improvements are rolled back.

    Attributes:
        rollbacks: List of rollback records.
    """

    def __init__(self) -> None:
        """Initialize the rollback tracker."""
        self.rollbacks: list[RollbackRecord] = []
        self.states: dict[str, str] = {}  # improvement_id -> previous state

    def save_state(self, improvement: Improvement) -> None:
        """Save the current state before an improvement.

        Args:
            improvement: The improvement being applied.
        """
        self.states[improvement.id] = json.dumps(
            {
                "status": improvement.status.value,
                "updated_at": improvement.updated_at,
                "votes": improvement.votes,
            }
        )

    def record_rollback(
        self, improvement: Improvement, reason: str, commit_hash: str = ""
    ) -> RollbackRecord:
        """Record a rollback.

        Args:
            improvement: The rolled back improvement.
            reason: Why the rollback occurred.
            commit_hash: Git commit of the rollback.

        Returns:
            The rollback record.
        """
        record = RollbackRecord(
            improvement_id=improvement.id,
            rollback_date=datetime.now().isoformat(),
            reason=reason,
            previous_state=self.states.get(improvement.id, ""),
            rollback_commit=commit_hash,
        )
        self.rollbacks.append(record)
        return record

    def get_rollbacks(self, improvement_id: str | None = None) -> list[RollbackRecord]:
        """Get rollback records."""
        if improvement_id:
            return [r for r in self.rollbacks if r.improvement_id == improvement_id]
        return self.rollbacks

    def get_rollback_rate(self, total_completed: int) -> float:
        """Calculate rollback rate."""
        if total_completed == 0:
            return 0.0
        return (len(self.rollbacks) / total_completed) * 100
