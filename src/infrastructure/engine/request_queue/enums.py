# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from enum import Enum, auto

class SchedulingPolicy(Enum):
    """Request scheduling policy."""
    FCFS = "fcfs"           # First come first served
    PRIORITY = "priority"   # Priority-based
    DEADLINE = "deadline"   # Deadline-aware
    FAIR = "fair"           # Fair share scheduling
    MLFQ = "mlfq"          # Multi-level feedback queue


class RequestStatus(Enum):
    """Status of a request in the queue."""
    WAITING = auto()
    SCHEDULED = auto()
    RUNNING = auto()
    PREEMPTED = auto()
    FINISHED = auto()
    ABORTED = auto()
