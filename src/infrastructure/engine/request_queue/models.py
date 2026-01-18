# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import time
from dataclasses import dataclass, field
from typing import Any, Optional
from .enums import RequestStatus

@dataclass
class RequestPriority:
    """
    Composite priority for request scheduling.
    
    Lower values = higher priority (processed first).
    """
    priority: int = 0           # User-specified priority (lower = higher)
    arrival_time: float = field(default_factory=time.time)
    deadline: Optional[float] = None
    boost_factor: float = 1.0   # Dynamic priority boost
    
    def __lt__(self, other: 'RequestPriority') -> bool:
        """Compare for heap ordering."""
        # Priority first (lower is better)
        if self.priority != other.priority:
            return self.priority < other.priority
        # Then arrival time (earlier is better)
        return self.arrival_time < other.arrival_time
    
    def effective_priority(self) -> float:
        """Get effective priority with boost applied."""
        return self.priority / self.boost_factor


@dataclass
class QueuedRequest:
    """
    Request wrapper for queue management.
    
    Contains request data and queue metadata.
    """
    request_id: str
    data: Any
    priority: RequestPriority = field(default_factory=RequestPriority)
    status: RequestStatus = RequestStatus.WAITING
    
    # Queue tracking
    queue_time: float = field(default_factory=time.time)
    scheduled_time: Optional[float] = None
    
    # Client/tenant for fair scheduling
    client_id: Optional[str] = None
    
    # Token counts for scheduling decisions
    num_prompt_tokens: int = 0
    max_tokens: int = 256
    
    def __lt__(self, other: 'QueuedRequest') -> bool:
        """Compare for heap ordering."""
        return self.priority < other.priority
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QueuedRequest):
            return False
        return self.request_id == other.request_id
    
    def __hash__(self) -> int:
        return hash(self.request_id)
    
    @property
    def wait_time(self) -> float:
        """Time spent waiting in queue."""
        return time.time() - self.queue_time
    
    @property
    def is_deadline_critical(self) -> bool:
        """Check if deadline is approaching."""
        if self.priority.deadline is None:
            return False
        return time.time() > self.priority.deadline * 0.9
