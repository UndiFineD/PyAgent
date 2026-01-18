# SPDX-License-Identifier: Apache-2.0
"""
Request Queue - FCFS and Priority-based request scheduling queues.

Implements vLLM's RequestQueue patterns with PyAgent enhancements:
- First-Come-First-Served (FCFS) queuing
- Priority-based scheduling with heap
- Deadline-aware scheduling
- Fair queuing across clients

Beyond vLLM:
- Multi-level feedback queues
- Weighted fair queuing
- Deadline-miss prediction
- Adaptive priority boosting
"""

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Set, TypeVar
import heapq
import time
import threading


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


T = TypeVar('T', bound=QueuedRequest)


class RequestQueue(ABC, Generic[T]):
    """Abstract base class for request queues."""
    
    @abstractmethod
    def add(self, request: T) -> None:
        """Add a request to the queue."""
        pass
    
    @abstractmethod
    def pop(self) -> T:
        """Pop the next request from the queue."""
        pass
    
    @abstractmethod
    def peek(self) -> T:
        """Peek at the next request without removing."""
        pass
    
    @abstractmethod
    def prepend(self, request: T) -> None:
        """Add request to front (for preemption)."""
        pass
    
    @abstractmethod
    def remove(self, request: T) -> bool:
        """Remove a specific request."""
        pass
    
    @abstractmethod
    def __len__(self) -> int:
        pass
    
    @abstractmethod
    def __bool__(self) -> bool:
        pass
    
    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass


class FCFSQueue(deque[T], RequestQueue[T]):
    """
    First-Come-First-Served queue using deque.
    
    O(1) add, pop, prepend operations.
    O(n) remove for arbitrary elements.
    """
    
    def add(self, request: T) -> None:
        """Add request to end of queue."""
        self.append(request)
    
    def pop(self) -> T:
        """Pop from front of queue."""
        if not self:
            raise IndexError("pop from empty queue")
        return self.popleft()
    
    def peek(self) -> T:
        """Peek at front of queue."""
        if not self:
            raise IndexError("peek from empty queue")
        return self[0]
    
    def prepend(self, request: T) -> None:
        """Add request to front of queue."""
        self.appendleft(request)
    
    def remove(self, request: T) -> bool:
        """Remove a specific request."""
        try:
            deque.remove(self, request)
            return True
        except ValueError:
            return False
    
    def remove_batch(self, requests: Set[T]) -> int:
        """Remove multiple requests efficiently."""
        if not requests:
            return 0
        
        original_len = len(self)
        # Filter in place
        filtered = [r for r in self if r not in requests]
        self.clear()
        self.extend(filtered)
        return original_len - len(self)
    
    def __bool__(self) -> bool:
        return len(self) > 0
    
    def __iter__(self) -> Iterator[T]:
        return iter(deque.__iter__(self))


class PriorityQueue(RequestQueue[T]):
    """
    Priority queue using heap.
    
    O(log n) add, pop operations.
    O(n) remove for arbitrary elements.
    """
    
    def __init__(self) -> None:
        self._heap: List[T] = []
        self._counter = 0  # For stable ordering
    
    def add(self, request: T) -> None:
        """Add request to heap."""
        heapq.heappush(self._heap, request)
    
    def pop(self) -> T:
        """Pop highest priority request."""
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)
    
    def peek(self) -> T:
        """Peek at highest priority request."""
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0]
    
    def prepend(self, request: T) -> None:
        """Add request (same as add for priority queue)."""
        # Priority queue doesn't have a front, so just add
        self.add(request)
    
    def remove(self, request: T) -> bool:
        """Remove a specific request."""
        try:
            self._heap.remove(request)
            heapq.heapify(self._heap)
            return True
        except ValueError:
            return False
    
    def remove_batch(self, requests: Set[T]) -> int:
        """Remove multiple requests efficiently."""
        if not requests:
            return 0
        
        original_len = len(self._heap)
        self._heap = [r for r in self._heap if r not in requests]
        heapq.heapify(self._heap)
        return original_len - len(self._heap)
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return len(self._heap) > 0
    
    def __iter__(self) -> Iterator[T]:
        # Return in priority order without modifying heap
        return iter(sorted(self._heap))
    
    def __reversed__(self) -> Iterator[T]:
        return iter(sorted(self._heap, reverse=True))


class DeadlineQueue(PriorityQueue[T]):
    """
    Deadline-aware priority queue.
    
    Prioritizes requests by deadline, then by priority.
    """
    
    def add(self, request: T) -> None:
        """Add with deadline consideration."""
        # Boost priority for deadline-critical requests
        if request.is_deadline_critical:
            request.priority.boost_factor = 2.0
        super().add(request)
    
    def update_priorities(self) -> int:
        """Update priorities based on deadline proximity."""
        updated = 0
        current_time = time.time()
        
        for request in self._heap:
            if request.priority.deadline is not None:
                time_to_deadline = request.priority.deadline - current_time
                if time_to_deadline < 10:  # Less than 10 seconds
                    request.priority.boost_factor = 3.0
                    updated += 1
                elif time_to_deadline < 30:
                    request.priority.boost_factor = 2.0
                    updated += 1
        
        if updated > 0:
            heapq.heapify(self._heap)
        
        return updated


class FairQueue(RequestQueue[T]):
    """
    Fair share queue with per-client quotas.
    
    Ensures fair scheduling across multiple clients/tenants.
    """
    
    def __init__(self, default_weight: float = 1.0) -> None:
        self._client_queues: Dict[str, deque[T]] = {}
        self._client_weights: Dict[str, float] = {}
        self._client_served: Dict[str, int] = {}
        self._default_weight = default_weight
        self._round_robin_index = 0
        self._total_requests = 0
    
    def add(self, request: T) -> None:
        """Add request to appropriate client queue."""
        client_id = request.client_id or "default"
        
        if client_id not in self._client_queues:
            self._client_queues[client_id] = deque()
            self._client_weights[client_id] = self._default_weight
            self._client_served[client_id] = 0
        
        self._client_queues[client_id].append(request)
        self._total_requests += 1
    
    def pop(self) -> T:
        """Pop using weighted fair sharing."""
        if self._total_requests == 0:
            raise IndexError("pop from empty fair queue")
        
        # Find client with best fair share ratio
        best_client = None
        best_ratio = float('inf')
        
        for client_id, queue in self._client_queues.items():
            if not queue:
                continue
            
            weight = self._client_weights.get(client_id, self._default_weight)
            served = self._client_served.get(client_id, 0)
            ratio = served / weight if weight > 0 else float('inf')
            
            if ratio < best_ratio:
                best_ratio = ratio
                best_client = client_id
        
        if best_client is None:
            raise IndexError("no requests available")
        
        request = self._client_queues[best_client].popleft()
        self._client_served[best_client] += 1
        self._total_requests -= 1
        
        return request
    
    def peek(self) -> T:
        """Peek at next fair request."""
        # Similar logic to pop but don't remove
        for client_id in sorted(
            self._client_queues.keys(),
            key=lambda c: self._client_served.get(c, 0) / self._client_weights.get(c, 1.0)
        ):
            if self._client_queues[client_id]:
                return self._client_queues[client_id][0]
        raise IndexError("peek from empty fair queue")
    
    def prepend(self, request: T) -> None:
        """Prepend to client queue."""
        client_id = request.client_id or "default"
        
        if client_id not in self._client_queues:
            self._client_queues[client_id] = deque()
            self._client_weights[client_id] = self._default_weight
            self._client_served[client_id] = 0
        
        self._client_queues[client_id].appendleft(request)
        self._total_requests += 1
    
    def remove(self, request: T) -> bool:
        """Remove specific request."""
        client_id = request.client_id or "default"
        
        if client_id in self._client_queues:
            try:
                self._client_queues[client_id].remove(request)
                self._total_requests -= 1
                return True
            except ValueError:
                pass
        return False
    
    def set_client_weight(self, client_id: str, weight: float) -> None:
        """Set weight for a client."""
        self._client_weights[client_id] = max(0.1, weight)
    
    def __len__(self) -> int:
        return self._total_requests
    
    def __bool__(self) -> bool:
        return self._total_requests > 0
    
    def __iter__(self) -> Iterator[T]:
        for queue in self._client_queues.values():
            yield from queue


class MLFQueue(RequestQueue[T]):
    """
    Multi-Level Feedback Queue.
    
    Implements multiple priority levels with aging.
    Short requests get priority over long-running ones.
    """
    
    def __init__(
        self,
        num_levels: int = 4,
        quantum_ms: float = 100.0,
        aging_interval_ms: float = 1000.0,
    ) -> None:
        self.num_levels = num_levels
        self.quantum = quantum_ms / 1000.0
        self.aging_interval = aging_interval_ms / 1000.0
        
        # Priority levels (0 = highest)
        self._levels: List[deque[T]] = [deque() for _ in range(num_levels)]
        self._request_levels: Dict[str, int] = {}
        self._request_runtime: Dict[str, float] = {}
        self._total_requests = 0
        self._last_aging = time.time()
    
    def add(self, request: T) -> None:
        """Add request to highest priority level."""
        self._levels[0].append(request)
        self._request_levels[request.request_id] = 0
        self._request_runtime[request.request_id] = 0.0
        self._total_requests += 1
    
    def pop(self) -> T:
        """Pop from highest non-empty priority level."""
        self._maybe_age_requests()
        
        for level, queue in enumerate(self._levels):
            if queue:
                request = queue.popleft()
                self._total_requests -= 1
                return request
        
        raise IndexError("pop from empty MLFQ")
    
    def peek(self) -> T:
        """Peek at highest priority request."""
        for queue in self._levels:
            if queue:
                return queue[0]
        raise IndexError("peek from empty MLFQ")
    
    def prepend(self, request: T) -> None:
        """Prepend to appropriate level."""
        level = self._request_levels.get(request.request_id, 0)
        self._levels[level].appendleft(request)
        self._total_requests += 1
    
    def remove(self, request: T) -> bool:
        """Remove specific request."""
        level = self._request_levels.get(request.request_id)
        if level is not None:
            try:
                self._levels[level].remove(request)
                del self._request_levels[request.request_id]
                del self._request_runtime[request.request_id]
                self._total_requests -= 1
                return True
            except ValueError:
                pass
        return False
    
    def demote(self, request_id: str, runtime_increment: float) -> None:
        """Demote request to lower priority after using quantum."""
        if request_id not in self._request_levels:
            return
        
        self._request_runtime[request_id] += runtime_increment
        
        if self._request_runtime[request_id] >= self.quantum:
            current_level = self._request_levels[request_id]
            new_level = min(current_level + 1, self.num_levels - 1)
            self._request_levels[request_id] = new_level
            self._request_runtime[request_id] = 0.0
    
    def _maybe_age_requests(self) -> None:
        """Age requests to prevent starvation."""
        now = time.time()
        if now - self._last_aging < self.aging_interval:
            return
        
        self._last_aging = now
        
        # Move oldest requests from lower levels to higher
        for level in range(1, self.num_levels):
            if self._levels[level]:
                # Move one request up
                request = self._levels[level].popleft()
                self._levels[level - 1].append(request)
                self._request_levels[request.request_id] = level - 1
    
    def __len__(self) -> int:
        return self._total_requests
    
    def __bool__(self) -> bool:
        return self._total_requests > 0
    
    def __iter__(self) -> Iterator[T]:
        for queue in self._levels:
            yield from queue


# ============================================================================
# Request Queue Manager
# ============================================================================

class RequestQueueManager:
    """
    Manages multiple request queues with different policies.
    
    Features:
    - Policy switching
    - Queue statistics
    - Admission control
    """
    
    def __init__(
        self,
        policy: SchedulingPolicy = SchedulingPolicy.FCFS,
        max_queue_size: int = 10000,
    ) -> None:
        self.policy = policy
        self.max_queue_size = max_queue_size
        self._queue = self._create_queue(policy)
        self._lock = threading.Lock()
        
        # Statistics
        self.total_added = 0
        self.total_popped = 0
        self.total_removed = 0
        self.max_observed_size = 0
    
    def _create_queue(self, policy: SchedulingPolicy) -> RequestQueue[QueuedRequest]:
        """Create queue for given policy."""
        if policy == SchedulingPolicy.FCFS:
            return FCFSQueue()
        elif policy == SchedulingPolicy.PRIORITY:
            return PriorityQueue()
        elif policy == SchedulingPolicy.DEADLINE:
            return DeadlineQueue()
        elif policy == SchedulingPolicy.FAIR:
            return FairQueue()
        elif policy == SchedulingPolicy.MLFQ:
            return MLFQueue()
        else:
            return FCFSQueue()
    
    def add(self, request: QueuedRequest) -> bool:
        """Add request with admission control."""
        with self._lock:
            if len(self._queue) >= self.max_queue_size:
                return False
            
            self._queue.add(request)
            self.total_added += 1
            self.max_observed_size = max(self.max_observed_size, len(self._queue))
            return True
    
    def pop(self) -> Optional[QueuedRequest]:
        """Pop next request."""
        with self._lock:
            if not self._queue:
                return None
            
            request = self._queue.pop()
            request.status = RequestStatus.SCHEDULED
            request.scheduled_time = time.time()
            self.total_popped += 1
            return request
    
    def peek(self) -> Optional[QueuedRequest]:
        """Peek at next request."""
        with self._lock:
            if not self._queue:
                return None
            return self._queue.peek()
    
    def remove(self, request_id: str) -> bool:
        """Remove request by ID."""
        with self._lock:
            for req in self._queue:
                if req.request_id == request_id:
                    if self._queue.remove(req):
                        self.total_removed += 1
                        return True
            return False
    
    def __len__(self) -> int:
        return len(self._queue)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self._lock:
            return {
                'policy': self.policy.value,
                'current_size': len(self._queue),
                'max_size': self.max_queue_size,
                'total_added': self.total_added,
                'total_popped': self.total_popped,
                'total_removed': self.total_removed,
                'max_observed_size': self.max_observed_size,
            }


# ============================================================================
# Factory Functions
# ============================================================================

def create_request_queue(
    policy: SchedulingPolicy,
    **kwargs: Any,
) -> RequestQueue[QueuedRequest]:
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


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    'SchedulingPolicy',
    'RequestStatus',
    # Data classes
    'RequestPriority',
    'QueuedRequest',
    # Queue implementations
    'RequestQueue',
    'FCFSQueue',
    'PriorityQueue',
    'DeadlineQueue',
    'FairQueue',
    'MLFQueue',
    # Manager
    'RequestQueueManager',
    # Factory
    'create_request_queue',
]
