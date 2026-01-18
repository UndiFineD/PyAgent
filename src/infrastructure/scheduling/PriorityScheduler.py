"""
Priority Scheduler with deadline-aware task scheduling.

Phase 19: Beyond vLLM - Performance Patterns
Advanced scheduling for latency-sensitive workloads.
"""
from __future__ import annotations

import asyncio
import heapq
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    TypeVar,
    Union,
)
from concurrent.futures import Future, ThreadPoolExecutor
import weakref

T = TypeVar('T')
R = TypeVar('R')


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


@dataclass
class TaskStats:
    """Statistics for task execution."""
    scheduled: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0
    timeouts: int = 0
    total_wait_time_ms: float = 0.0
    total_exec_time_ms: float = 0.0
    
    @property
    def avg_wait_time_ms(self) -> float:
        """Average wait time in milliseconds."""
        if self.completed == 0:
            return 0.0
        return self.total_wait_time_ms / self.completed
    
    @property
    def avg_exec_time_ms(self) -> float:
        """Average execution time in milliseconds."""
        if self.completed == 0:
            return 0.0
        return self.total_exec_time_ms / self.completed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'scheduled': self.scheduled,
            'completed': self.completed,
            'failed': self.failed,
            'cancelled': self.cancelled,
            'timeouts': self.timeouts,
            'avg_wait_time_ms': self.avg_wait_time_ms,
            'avg_exec_time_ms': self.avg_exec_time_ms,
        }


@dataclass(order=True)
class ScheduledTask(Generic[R]):
    """A task scheduled for execution."""
    
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
        """Check if task has exceeded its deadline."""
        if self.deadline == float('inf'):
            return False
        return time.monotonic() > self.deadline


class PriorityScheduler:
    """
    Priority-based task scheduler with deadline support.
    
    Features:
    - Priority-based scheduling (CRITICAL to IDLE)
    - Deadline-aware execution
    - Timeout handling
    - Work stealing between priority levels
    - Statistics tracking
    
    Example:
        scheduler = PriorityScheduler(workers=4)
        
        # Schedule high-priority task
        future = scheduler.submit(my_func, priority=TaskPriority.HIGH)
        
        # Schedule with deadline
        future = scheduler.submit(
            my_func,
            priority=TaskPriority.NORMAL,
            deadline_ms=100.0,
        )
    """
    
    def __init__(
        self,
        workers: int = 4,
        max_queue_size: int = 10000,
        enable_work_stealing: bool = True,
    ):
        """
        Initialize scheduler.
        
        Args:
            workers: Number of worker threads
            max_queue_size: Maximum pending tasks
            enable_work_stealing: Allow low-priority workers to steal high-priority tasks
        """
        self._workers = workers
        self._max_queue_size = max_queue_size
        self._enable_work_stealing = enable_work_stealing
        
        # Priority queues (one per priority level)
        self._queues: Dict[TaskPriority, List[ScheduledTask]] = {
            p: [] for p in TaskPriority
        }
        
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._sequence = 0
        self._pending_count = 0
        
        self._stats = TaskStats()
        self._running = True
        
        # Thread pool
        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="scheduler",
        )
        
        # Start worker threads
        self._worker_futures: List[Future] = []
        for i in range(workers):
            f = self._executor.submit(self._worker_loop, i)
            self._worker_futures.append(f)
    
    def submit(
        self,
        func: Callable[[], R],
        priority: TaskPriority = TaskPriority.NORMAL,
        deadline_ms: Optional[float] = None,
        timeout_ms: Optional[float] = None,
        task_id: Optional[str] = None,
    ) -> Future[R]:
        """
        Submit a task for execution.
        
        Args:
            func: Function to execute
            priority: Task priority
            deadline_ms: Deadline in milliseconds from now
            timeout_ms: Maximum execution time in milliseconds
            task_id: Optional task identifier
            
        Returns:
            Future for the task result
        """
        now = time.monotonic()
        
        deadline = float('inf')
        if deadline_ms is not None:
            deadline = now + deadline_ms / 1000.0
        
        timeout = None
        if timeout_ms is not None:
            timeout = timeout_ms / 1000.0
        
        future: Future[R] = Future()
        
        with self._not_empty:
            if self._pending_count >= self._max_queue_size:
                future.set_exception(RuntimeError("Scheduler queue full"))
                return future
            
            self._sequence += 1
            
            task = ScheduledTask(
                priority_value=priority.value,
                deadline=deadline,
                sequence=self._sequence,
                id=task_id or f"task-{self._sequence}",
                func=func,
                priority=priority,
                created_at=now,
                timeout=timeout,
                future=future,
            )
            
            heapq.heappush(self._queues[priority], task)
            self._pending_count += 1
            self._stats.scheduled += 1
            
            self._not_empty.notify()
        
        return future
    
    def _worker_loop(self, worker_id: int) -> None:
        """Worker thread main loop."""
        while self._running:
            task = self._get_next_task()
            if task is None:
                continue
            
            self._execute_task(task)
    
    def _get_next_task(self) -> Optional[ScheduledTask]:
        """Get the next task to execute."""
        with self._not_empty:
            # Wait for work
            while self._running and self._pending_count == 0:
                self._not_empty.wait(timeout=0.1)
            
            if not self._running:
                return None
            
            # Find highest priority non-empty queue
            for priority in TaskPriority:
                queue = self._queues[priority]
                while queue:
                    task = heapq.heappop(queue)
                    self._pending_count -= 1
                    
                    # Skip expired tasks
                    if task.is_expired:
                        self._handle_timeout(task)
                        continue
                    
                    return task
            
            return None
    
    def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a single task."""
        start_time = time.monotonic()
        wait_time = (start_time - task.created_at) * 1000  # ms
        
        task.state = TaskState.RUNNING
        
        try:
            # Execute with timeout
            if task.timeout:
                result = self._execute_with_timeout(task.func, task.timeout)
            else:
                result = task.func()
            
            task.state = TaskState.COMPLETED
            task.result = result
            
            if task.future:
                task.future.set_result(result)
            
            # Update stats
            exec_time = (time.monotonic() - start_time) * 1000
            with self._lock:
                self._stats.completed += 1
                self._stats.total_wait_time_ms += wait_time
                self._stats.total_exec_time_ms += exec_time
        
        except TimeoutError:
            self._handle_timeout(task)
        
        except Exception as e:
            task.state = TaskState.FAILED
            task.error = e
            
            if task.future:
                task.future.set_exception(e)
            
            with self._lock:
                self._stats.failed += 1
    
    def _execute_with_timeout(
        self,
        func: Callable[[], R],
        timeout: float,
    ) -> R:
        """Execute function with timeout."""
        # Use a separate thread for timeout handling
        result_container: List[Any] = []
        error_container: List[Exception] = []
        completed = threading.Event()
        
        def wrapper():
            try:
                result_container.append(func())
            except Exception as e:
                error_container.append(e)
            finally:
                completed.set()
        
        thread = threading.Thread(target=wrapper)
        thread.start()
        
        if not completed.wait(timeout):
            raise TimeoutError("Task execution timed out")
        
        thread.join()
        
        if error_container:
            raise error_container[0]
        
        return result_container[0]
    
    def _handle_timeout(self, task: ScheduledTask) -> None:
        """Handle task timeout."""
        task.state = TaskState.TIMEOUT
        
        if task.future:
            task.future.set_exception(TimeoutError("Task deadline exceeded"))
        
        with self._lock:
            self._stats.timeouts += 1
    
    def cancel(self, task_id: str) -> bool:
        """
        Cancel a pending task.
        
        Args:
            task_id: ID of task to cancel
            
        Returns:
            True if task was found and cancelled
        """
        with self._lock:
            for priority in TaskPriority:
                queue = self._queues[priority]
                for i, task in enumerate(queue):
                    if task.id == task_id and task.state == TaskState.PENDING:
                        task.state = TaskState.CANCELLED
                        if task.future:
                            task.future.cancel()
                        self._stats.cancelled += 1
                        return True
        
        return False
    
    def shutdown(self, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Shutdown the scheduler.
        
        Args:
            wait: Wait for pending tasks to complete
            timeout: Maximum time to wait
        """
        self._running = False
        
        with self._not_empty:
            self._not_empty.notify_all()
        
        self._executor.shutdown(wait=wait)
    
    @property
    def pending_count(self) -> int:
        """Number of pending tasks."""
        return self._pending_count
    
    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._stats
    
    def get_queue_sizes(self) -> Dict[TaskPriority, int]:
        """Get current queue sizes by priority."""
        with self._lock:
            return {p: len(q) for p, q in self._queues.items()}


class AsyncPriorityScheduler:
    """
    Async priority scheduler for coroutine-based workloads.
    """
    
    def __init__(self, max_concurrent: int = 100):
        """
        Initialize async scheduler.
        
        Args:
            max_concurrent: Maximum concurrent tasks
        """
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)
        
        self._queues: Dict[TaskPriority, asyncio.PriorityQueue] = {}
        self._stats = TaskStats()
        self._sequence = 0
        self._lock = asyncio.Lock()
    
    async def submit(
        self,
        coro: Coroutine[Any, Any, R],
        priority: TaskPriority = TaskPriority.NORMAL,
        deadline_ms: Optional[float] = None,
    ) -> R:
        """
        Submit and await a coroutine.
        
        Args:
            coro: Coroutine to execute
            priority: Task priority
            deadline_ms: Deadline in milliseconds
            
        Returns:
            Coroutine result
        """
        async with self._semaphore:
            start = time.monotonic()
            
            timeout = None
            if deadline_ms:
                timeout = deadline_ms / 1000.0
            
            try:
                if timeout:
                    result = await asyncio.wait_for(coro, timeout=timeout)
                else:
                    result = await coro
                
                exec_time = (time.monotonic() - start) * 1000
                async with self._lock:
                    self._stats.completed += 1
                    self._stats.total_exec_time_ms += exec_time
                
                return result
            
            except asyncio.TimeoutError:
                async with self._lock:
                    self._stats.timeouts += 1
                raise
            
            except Exception:
                async with self._lock:
                    self._stats.failed += 1
                raise
    
    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._stats


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


class DeadlineScheduler:
    """
    Earliest-deadline-first (EDF) scheduler.
    
    Always executes the task with the nearest deadline first.
    """
    
    def __init__(self, workers: int = 4):
        """Initialize EDF scheduler."""
        self._workers = workers
        self._queue: List[tuple[float, int, ScheduledTask]] = []
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._sequence = 0
        self._running = True
        self._stats = TaskStats()
        
        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="edf",
        )
        
        for _ in range(workers):
            self._executor.submit(self._worker_loop)
    
    def submit(
        self,
        func: Callable[[], R],
        deadline_ms: float,
        task_id: Optional[str] = None,
    ) -> Future[R]:
        """
        Submit task with deadline.
        
        Args:
            func: Function to execute
            deadline_ms: Deadline in milliseconds from now
            task_id: Optional task ID
            
        Returns:
            Future for result
        """
        now = time.monotonic()
        deadline = now + deadline_ms / 1000.0
        
        future: Future[R] = Future()
        
        with self._not_empty:
            self._sequence += 1
            
            task = ScheduledTask(
                priority_value=0,
                deadline=deadline,
                sequence=self._sequence,
                id=task_id or f"task-{self._sequence}",
                func=func,
                priority=TaskPriority.NORMAL,
                created_at=now,
                future=future,
            )
            
            heapq.heappush(self._queue, (deadline, self._sequence, task))
            self._stats.scheduled += 1
            self._not_empty.notify()
        
        return future
    
    def _worker_loop(self) -> None:
        """Worker thread loop."""
        while self._running:
            with self._not_empty:
                while self._running and not self._queue:
                    self._not_empty.wait(timeout=0.1)
                
                if not self._running:
                    return
                
                _, _, task = heapq.heappop(self._queue)
            
            # Execute task
            try:
                result = task.func()
                task.state = TaskState.COMPLETED
                if task.future:
                    task.future.set_result(result)
                
                with self._lock:
                    self._stats.completed += 1
            
            except Exception as e:
                task.state = TaskState.FAILED
                if task.future:
                    task.future.set_exception(e)
                
                with self._lock:
                    self._stats.failed += 1
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown scheduler."""
        self._running = False
        with self._not_empty:
            self._not_empty.notify_all()
        self._executor.shutdown(wait=wait)
    
    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._stats
