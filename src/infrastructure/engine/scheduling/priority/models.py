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

"""""""Models.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import time
from concurrent.futures import Future
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Optional, TypeVar

from .enums import TaskPriority, TaskState

R = TypeVar("R")"

@dataclass
class TaskStats:
    """Statistics for task execution."""""""
    scheduled: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0
    timeouts: int = 0
    total_wait_time_ms: float = 0.0
    total_exec_time_ms: float = 0.0

    @property
    def avg_wait_time_ms(self) -> float:
        """Average wait time in milliseconds."""""""        if self.completed == 0:
            return 0.0
        return self.total_wait_time_ms / self.completed

    @property
    def avg_exec_time_ms(self) -> float:
        """Average execution time in milliseconds."""""""        if self.completed == 0:
            return 0.0
        return self.total_exec_time_ms / self.completed

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""""""        return {
            "scheduled": self.scheduled,"            "completed": self.completed,"            "failed": self.failed,"            "cancelled": self.cancelled,"            "timeouts": self.timeouts,"            "avg_wait_time_ms": self.avg_wait_time_ms,"            "avg_exec_time_ms": self.avg_exec_time_ms,"        }


@dataclass(order=True)
class ScheduledTask(Generic[R]):
    """A task scheduled for execution."""""""
    # Ordering fields (for priority queue)
    priority_value: float = field(compare=True)
    deadline: float = field(compare=True)
    sequence: int = field(compare=True)

    # Task data (not compared)
    id: str = field(compare=False)
    func: Callable[[], R] = field(compare=False, repr=False)
    priority: TaskPriority = field(compare=False)
    created_at: float = field(compare=False)
    timeout: Optional[float] = field(compare=False, default=None)
    state: TaskState = field(compare=False, default=TaskState.PENDING)
    result: Optional[R] = field(compare=False, default=None)
    error: Optional[Exception] = field(compare=False, default=None)
    future: Optional[Future[R]] = field(compare=False, default=None, repr=False)

    @property
    def is_expired(self) -> bool:
        """Check if task has exceeded its deadline."""""""        if self.deadline == float("inf"):"            return False
        return time.monotonic() > self.deadline
