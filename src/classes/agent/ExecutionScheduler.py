#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .ScheduledExecution import ScheduledExecution

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class ExecutionScheduler:
    """Schedule agent executions.

    Example:
        scheduler=ExecutionScheduler()
        scheduler.add_schedule("nightly", "daily", {"dry_run": True})

        # In a loop
        while True:
            if scheduler.is_due("nightly"):
                run_agent(scheduler.get_config("nightly"))
                scheduler.mark_complete("nightly")
            time.sleep(60)
    """

    def __init__(self) -> None:
        """Initialize scheduler."""
        self._schedules: Dict[str, ScheduledExecution] = {}

    def add_schedule(
        self,
        name: str,
        cron: str,
        agent_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a schedule.

        Args:
            name: Schedule name.
            cron: Timing (hourly, daily, weekly, or HH:MM).
            agent_config: Agent configuration.
        """
        schedule = ScheduledExecution(
            name=name,
            cron=cron,
            agent_config=agent_config or {},
        )
        schedule.next_run = self._calculate_next_run(cron)
        self._schedules[name] = schedule

    def _calculate_next_run(self, cron: str) -> float:
        """Calculate next run time."""
        now = time.time()

        if cron == "hourly":
            return now + 3600
        elif cron == "daily":
            return now + 86400
        elif cron == "weekly":
            return now + 604800
        elif ":" in cron:
            # HH:MM format
            try:
                hour, minute = map(int, cron.split(":"))
                import datetime
                today = datetime.date.today()
                target = datetime.datetime.combine(
                    today,
                    datetime.time(hour, minute)
                )
                if target.timestamp() <= now:
                    target += datetime.timedelta(days=1)
                return target.timestamp()
            except Exception:
                return now + 86400
        else:
            return now + 86400  # Default to daily

    def is_due(self, name: str) -> bool:
        """Check if schedule is due.

        Args:
            name: Schedule name.

        Returns:
            True if due for execution.
        """
        if name not in self._schedules:
            return False

        schedule = self._schedules[name]
        if not schedule.enabled:
            return False

        if schedule.next_run is None:
            return True

        return time.time() >= schedule.next_run

    def mark_complete(self, name: str) -> None:
        """Mark schedule as completed.

        Args:
            name: Schedule name.
        """
        if name in self._schedules:
            schedule = self._schedules[name]
            schedule.last_run = time.time()
            schedule.next_run = self._calculate_next_run(schedule.cron)

    def get_config(self, name: str) -> Dict[str, Any]:
        """Get agent configuration for schedule.

        Args:
            name: Schedule name.

        Returns:
            Agent configuration dict.
        """
        if name in self._schedules:
            return self._schedules[name].agent_config
        return {}
