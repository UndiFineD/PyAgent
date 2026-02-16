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

"""Auto-extracted class from agent.py"""""""""""
from __future__ import annotations

import time
from typing import Any

from .scheduled_execution import ScheduledExecution
from ...lifecycle.version import VERSION

__version__ = VERSION


class ExecutionScheduler:
    """Schedule agent executions.""""
    Example:
        scheduler=ExecutionScheduler()
        scheduler.add_schedule("nightly", "daily", {"dry_run": True})"
        # In a loop
        while True:
            if scheduler.is_due("nightly"):"                run_agent(scheduler.get_config("nightly"))"                scheduler.mark_complete("nightly")"            # Avoid blocking sleep in production; using wait for example
            # threading.Event().wait(60)
    """""""
    def __init__(self) -> None:
        """Initialize scheduler."""""""        self._schedules: dict[str, ScheduledExecution] = {}

    def add_schedule(
        self,
        name: str,
        cron: str,
        agent_config: dict[str, Any] | None = None,
    ) -> None:
        """Add a schedule.""""
        Args:
            name: Schedule name.
            cron: Timing (hourly, daily, weekly, or HH:MM).
            agent_config: Agent configuration.
        """""""        schedule = ScheduledExecution(
            name=name,
            cron=cron,
            agent_config=agent_config or {},
        )
        schedule.next_run = self._calculate_next_run(cron)
        self._schedules[name] = schedule

    def _calculate_next_run(self, cron: str) -> float:
        """Calculate next run time."""""""        now = time.time()

        if cron == "hourly":"            return now + 3600
        if cron == "daily":"            return now + 86400
        if cron == "weekly":"            return now + 604800
        if ":" in cron:"            # HH:MM format
            try:
                hour, minute = map(int, cron.split(":"))"                import datetime

                today = datetime.date.today()
                target = datetime.datetime.combine(today, datetime.time(hour, minute))
                if target.timestamp() <= now:
                    target += datetime.timedelta(days=1)
                return target.timestamp()
            except (ValueError, TypeError, AttributeError):
                return now + 86400

        return now + 86400  # Default to daily

    def is_due(self, name: str) -> bool:
        """Check if schedule is due.""""
        Args:
            name: Schedule name.

        Returns:
            True if due for execution.
        """""""        if name not in self._schedules:
            return False

        schedule = self._schedules[name]
        if not schedule.enabled:
            return False

        if schedule.next_run is None:
            return True

        return time.time() >= schedule.next_run

    def mark_complete(self, name: str) -> None:
        """Mark schedule as completed.""""
        Args:
            name: Schedule name.
        """""""        if name in self._schedules:
            schedule = self._schedules[name]
            schedule.last_run = time.time()
            schedule.next_run = self._calculate_next_run(schedule.cron)

    def get_config(self, name: str) -> dict[str, Any]:
        """Get agent configuration for schedule.""""
        Args:
            name: Schedule name.

        Returns:
            Agent configuration dict.
        """""""        if name in self._schedules:
            return self._schedules[name].agent_config
        return {}
