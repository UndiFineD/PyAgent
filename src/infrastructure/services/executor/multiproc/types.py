#!/usr/bin/env python3

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


"""
Types.py module.

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Optional, Tuple


class ExecutorBackend(Enum):
    """Executor backend types.
    MULTIPROC = auto()
    RAY = auto()
    UNIPROC = auto()
    DISTRIBUTED = auto()


class WorkerState(Enum):
    """Worker process states.
    STARTING = auto()
    READY = auto()
    BUSY = auto()
    ERROR = auto()
    TERMINATED = auto()


@dataclass
class WorkerInfo:
    """Information about a worker process.
    worker_id: int
    pid: Optional[int] = None
    state: WorkerState = WorkerState.STARTING
    gpu_id: Optional[int] = None
    start_time: float = 0.0
    last_heartbeat: float = 0.0
    tasks_completed: int = 0
    error_count: int = 0
    current_task_id: Optional[str] = None


@dataclass
class TaskMessage:
    """Message for task execution.
    task_id: str
    func_name: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    priority: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class ResultMessage:
    """Message for task result.
    task_id: str
    worker_id: int
    success: bool
    result: Any = None
    error: Optional[str] = None
    traceback: Optional[str] = None
    execution_time_ns: int = 0
