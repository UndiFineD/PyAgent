# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import threading
import time
from typing import (
    Dict,
    Optional,
    TypeVar,
    Callable,
)
from concurrent.futures import Future
from .enums import TaskPriority
from .models import TaskStats
from .base import PriorityScheduler

R = TypeVar('R')

class RateLimitedScheduler:
    """
    Scheduler with rate limiting per priority level.
    """
    
    def __init__(
        self,
        rates: Optional[Dict[TaskPriority, float]] = None,
        workers: int = 4,
    ):
        """
        Initialize rate-limited scheduler.
        
        Args:
            rates: Tasks per second per priority level
            workers: Number of worker threads
        """
        self._rates = rates or {
            TaskPriority.CRITICAL: float('inf'),
            TaskPriority.HIGH: 100.0,
            TaskPriority.NORMAL: 50.0,
            TaskPriority.LOW: 20.0,
            TaskPriority.IDLE: 5.0,
        }
        
        self._last_execution: Dict[TaskPriority, float] = {
            p: 0.0 for p in TaskPriority
        }
        
        self._scheduler = PriorityScheduler(workers=workers)
        self._lock = threading.Lock()
    
    def submit(
        self,
        func: Callable[[], R],
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> Future[R]:
        """Submit a rate-limited task."""
        rate = self._rates.get(priority, 10.0)
        min_interval = 1.0 / rate if rate < float('inf') else 0.0
        
        with self._lock:
            now = time.monotonic()
            last = self._last_execution[priority]
            wait_time = max(0, last + min_interval - now)
            
            if wait_time > 0:
                time.sleep(wait_time)
            
            self._last_execution[priority] = time.monotonic()
        
        return self._scheduler.submit(func, priority=priority)
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the scheduler."""
        self._scheduler.shutdown(wait=wait)
    
    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._scheduler.stats
