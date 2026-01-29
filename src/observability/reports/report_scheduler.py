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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

import logging
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION


class ReportScheduler:
    """Scheduler for report generation.
    Handles scheduling report generation with cron - like expressions.
    Attributes:
        schedules: Scheduled tasks.
    Example:
        scheduler=ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])
        due=scheduler.get_due_tasks()
    """

    def __init__(self) -> None:
        """Initialize scheduler."""

        self.schedules: dict[str, dict[str, Any]] = {}
        logging.debug("ReportScheduler initialized")

    def add_schedule(self, name: str, cron_expr: str, file_patterns: list[str]) -> None:
        """Add a schedule.
        Args:
            name: Schedule name.
            cron_expr: Cron expression.
            file_patterns: Files to process.
        """

        self.schedules[name] = {
            "cron": cron_expr,
            "patterns": file_patterns,
            "last_run": 0.0,
        }

    def remove_schedule(self, name: str) -> bool:
        """Remove a schedule.
        Args:
            name: Schedule name.
        Returns:
            True if removed.
        """

        if name in self.schedules:
            del self.schedules[name]
            return True
        return False

    def get_due_tasks(self) -> list[str]:
        """Get tasks due to run.
        Returns:
            List of due schedule names.
        """

        # Simple implementation - in production would parse cron
        return list(self.schedules.keys())

    def mark_completed(self, name: str) -> None:
        """Mark a task as completed.
        Args:
            name: Schedule name.
        """

        if name in self.schedules:
            self.schedules[name]["last_run"] = time.time()
