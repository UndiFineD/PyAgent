#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .Improvement import Improvement
from .ResourceAllocation import ResourceAllocation
from .ScheduleStatus import ScheduleStatus
from .ScheduledEntry import ScheduledEntry
from .ScheduledImprovement import ScheduledImprovement
from ._ScheduleStore import _ScheduleStore

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
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
        self.sprints: Dict[str, List[str]] = {}
        self.resources: Dict[str, List[str]] = {}

        self._entries_by_id: Dict[str, ScheduledEntry] = {}
        self._entries: List[ScheduledEntry] = []
        self._allocations: Dict[str, ResourceAllocation] = {}

    def schedule_improvement(
        self,
        improvement: Any,
        start_date: Any,
        resources: Optional[List[str]] = None,
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

    def get_schedule(self, improvement_id: str) -> Optional[ScheduledImprovement]:
        return self.schedule.get(improvement_id)

    def update_status(self, improvement_id: str, status: ScheduleStatus) -> bool:
        item = self.schedule.get(improvement_id)
        if item is None:
            return False
        item.status = status
        return True

    def get_sprint_items(self, sprint_id: str) -> List[str]:
        return self.sprints.get(sprint_id, [])

    def allocate_resources(self, improvement_id: str, resources: List[str]) -> None:
        self._allocations[improvement_id] = ResourceAllocation(
            improvement_id=improvement_id,
            resources=list(resources),
        )

    def get_allocation(self, improvement_id: str) -> ResourceAllocation:
        return self._allocations.get(
            improvement_id,
            ResourceAllocation(improvement_id=improvement_id, resources=[]),
        )
