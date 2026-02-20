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


import time
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class _Schedule:
    name: str
    cron: str
    agent_config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_run: float | None = None
    next_run: float | None = None


class ExecutionScheduler:
    """A small scheduler for testing purposes.

    It supports simplified crons: 'hourly', 'daily', 'weekly', or 'HH:MM'.
    """

    def __init__(self) -> None:
        self._schedules: dict[str, _Schedule] = {}

    def add_schedule(self, name: str, cron: str, agent_config: dict | None = None) -> None:
        sched = _Schedule(name=name, cron=cron, agent_config=agent_config or {})
        sched.next_run = self._calculate_next_run(cron)
        self._schedules[name] = sched

    def _calculate_next_run(self, cron: str) -> float:
        now = time.time()
        if cron == "hourly":
            return now + 3600
        if cron == "daily":
            return now + 86400
        if cron == "weekly":
            return now + 604800
        if ":" in cron:
            try:
                hour, minute = map(int, cron.split(":"))
                import datetime

                today = datetime.date.today()
                target = datetime.datetime.combine(today, datetime.time(hour, minute))
                if target.timestamp() <= now:
                    target += datetime.timedelta(days=1)
                return target.timestamp()
            except Exception:
                return now + 86400
        return now + 86400

    def is_due(self, name: str) -> bool:
        if name not in self._schedules:
            return False
        sched = self._schedules[name]
        if not sched.enabled:
            return False
        if sched.next_run is None:
            return True
        return time.time() >= sched.next_run

    def mark_complete(self, name: str) -> None:
        if name in self._schedules:
            sched = self._schedules[name]
            sched.last_run = time.time()
            sched.next_run = self._calculate_next_run(sched.cron)

    def get_config(self, name: str) -> dict[str, Any]:
        if name in self._schedules:
            return self._schedules[name].agent_config
        return {}


__all__ = ["ExecutionScheduler"]
