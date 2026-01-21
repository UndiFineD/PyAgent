# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from enum import Enum, auto

class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 0    # Immediate execution
    HIGH = 1        # Low latency
    NORMAL = 2      # Default
    LOW = 3         # Background
    IDLE = 4        # When nothing else to do


class TaskState(Enum):
    """Task execution state."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    TIMEOUT = auto()
