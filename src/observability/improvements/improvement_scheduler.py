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

from datetime import datetime, timedelta
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .resource_allocation import ResourceAllocation
from .schedule_status import ScheduleStatus
from .schedule_store import _ScheduleStore
from .scheduled_entry import ScheduledEntry
from .scheduled_improvement import ScheduledImprovement

__version__ = VERSION


class ImprovementScheduler:
    """Manages improvement scheduling with resource allocation.

    Schedules improvements into sprints and tracks resource availability.

    Attributes:
        schedule: Map of improvement IDs to scheduled items.
        resources: Map of resource names to availability.
    """

    def __init__(self) -> None:
        self.schedule: _ScheduleStore = _ScheduleStore()
        self.sprints: dict[str, list[str]] = {}
        self.resources: dict[str, list[str]] = {}

        self._entries_by_id: dict[str, ScheduledEntry] = {}
        self._entries: list[ScheduledEntry] = []
        self._allocations: dict[str, ResourceAllocation] = {}

    def schedule_improvement(
        self,
        improvement: Any,
        start_date: Any,
        resources: list[str] | None = None,
        sprint_id: str = "",
        **_: Any,
    ) -> Any:
        # Legacy convention: Improvement object + ISO date string
        if isinstance(improvement, Improvement):
            start_dt = datetime.fromisoformat(str(start_date))
            end_dt = start_dt + timedelta(days=1)
            scheduled = ScheduledImprovement(
                improvement_id=improvement.id,
                scheduled_start=str(start_date),
                scheduled_end=end_dt.date().isoformat(),
                assigned_resources=list(resources or []),
                status=ScheduleStatus.SCHEDULED,
                sprint_id=sprint_id,
            )
            self.schedule[improvement.id] = scheduled
            if sprint_id:
                self.sprints.setdefault(sprint_id, []).append(improvement.id)
            return scheduled

        # Newer convention: id + datetime (or parseable string)
        improvement_id = str(improvement)
        if isinstance(start_date, datetime):
            start_dt2 = start_date
        else:
            start_dt2 = datetime.fromisoformat(str(start_date))

        entry = ScheduledEntry(
            improvement_id=improvement_id,
            start_date=start_dt2,
            resources=list(resources or []),
        )
        self._entries_by_id[improvement_id] = entry
        self._entries = [e for e in self._entries if e.improvement_id != improvement_id]
        self._entries.append(entry)
        return entry

    def get_schedule(self, improvement_id: str) -> ScheduledImprovement | None:
        return self.schedule.get(improvement_id)

    def update_status(self, improvement_id: str, status: ScheduleStatus) -> bool:
        item = self.schedule.get(improvement_id)
        if item is None:
            return False
        item.status = status
        return True

    def get_sprint_items(self, sprint_id: str) -> list[str]:
        return self.sprints.get(sprint_id, [])

    def allocate_resources(self, improvement_id: str, resources: list[str]) -> None:
        self._allocations[improvement_id] = ResourceAllocation(
            improvement_id=improvement_id,
            resources=list(resources),
        )

    def get_allocation(self, improvement_id: str) -> ResourceAllocation:
        return self._allocations.get(
            improvement_id,
            ResourceAllocation(improvement_id=improvement_id, resources=[]),
        )
