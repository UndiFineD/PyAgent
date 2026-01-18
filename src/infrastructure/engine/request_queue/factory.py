# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from typing import Any
from .enums import SchedulingPolicy
from .base import RequestQueue
from .models import QueuedRequest
from .queues.fcfs import FCFSQueue
from .queues.priority import PriorityQueue, DeadlineQueue
from .queues.fair import FairQueue
from .queues.mlfq import MLFQueue

def create_request_queue(
    policy: SchedulingPolicy,
    **kwargs: Any,
) -> RequestQueue:
    """
    Factory function to create request queue.
    
    Args:
        policy: Scheduling policy
        **kwargs: Policy-specific arguments
    
    Returns:
        RequestQueue instance
    """
    if policy == SchedulingPolicy.FCFS:
        return FCFSQueue()
    elif policy == SchedulingPolicy.PRIORITY:
        return PriorityQueue()
    elif policy == SchedulingPolicy.DEADLINE:
        return DeadlineQueue()
    elif policy == SchedulingPolicy.FAIR:
        return FairQueue(
            default_weight=kwargs.get('default_weight', 1.0)
        )
    elif policy == SchedulingPolicy.MLFQ:
        return MLFQueue(
            num_levels=kwargs.get('num_levels', 4),
            quantum_ms=kwargs.get('quantum_ms', 100.0),
            aging_interval_ms=kwargs.get('aging_interval_ms', 1000.0),
        )
    else:
        return FCFSQueue()
