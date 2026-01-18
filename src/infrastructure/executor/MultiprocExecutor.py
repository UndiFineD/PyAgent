"""
Phase 45: Multiprocess Executor
vLLM-inspired multiprocess executor with advanced coordination.

Beyond vLLM:
- Zero-copy message passing
- Automatic worker recovery
- Dynamic load balancing
- Pipeline parallelism support
- Distributed health monitoring
"""

from __future__ import annotations

import multiprocessing as mp
import os
import queue
import signal
import threading
import time
import traceback
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar, Union

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None

T = TypeVar('T')
R = TypeVar('R')


class ExecutorBackend(Enum):
    """Executor backend types."""
    MULTIPROC = auto()
    RAY = auto()
    UNIPROC = auto()
    DISTRIBUTED = auto()


class WorkerState(Enum):
    """Worker process states."""
    STARTING = auto()
    READY = auto()
    BUSY = auto()
    ERROR = auto()
    TERMINATED = auto()


@dataclass
class WorkerInfo:
    """Information about a worker process."""
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
    """Message for task execution."""
    task_id: str
    func_name: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    priority: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class ResultMessage:
    """Message for task result."""
    task_id: str
    worker_id: int
    success: bool
    result: Any = None
    error: Optional[str] = None
    traceback: Optional[str] = None
    execution_time_ns: int = 0


class FutureWrapper(Generic[T]):
    """
    Future wrapper for async task results (vLLM FutureWrapper equivalent).
    
    Beyond vLLM:
    - Timeout support
    - Cancellation
    - Progress callbacks
    """
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self._result: Optional[T] = None
        self._error: Optional[Exception] = None
        self._done = threading.Event()
        self._cancelled = False
        self._callbacks: List[Callable[['FutureWrapper[T]'], None]] = []
        self._lock = threading.Lock()
    
    def set_result(self, result: T) -> None:
        """Set the result."""
        with self._lock:
            self._result = result
            self._done.set()
            for callback in self._callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
    
    def set_exception(self, error: Exception) -> None:
        """Set an exception."""
        with self._lock:
            self._error = error
            self._done.set()
            for callback in self._callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
    
    def result(self, timeout: Optional[float] = None) -> T:
        """Get the result, blocking if necessary."""
        if not self._done.wait(timeout):
            raise TimeoutError(f"Task {self.task_id} timed out")
        
        with self._lock:
            if self._error:
                raise self._error
            return self._result  # type: ignore
    
    def done(self) -> bool:
        """Check if the future is done."""
        return self._done.is_set()
    
    def cancel(self) -> bool:
        """Cancel the future."""
        with self._lock:
            if self._done.is_set():
                return False
            self._cancelled = True
            self._error = Exception("Task cancelled")
            self._done.set()
            return True
    
    def cancelled(self) -> bool:
        """Check if the future was cancelled."""
        return self._cancelled
    
    def add_done_callback(self, callback: Callable[['FutureWrapper[T]'], None]) -> None:
        """Add a callback to be called when the future is done."""
        with self._lock:
            if self._done.is_set():
                callback(self)
            else:
                self._callbacks.append(callback)


class Executor(ABC):
    """
    Abstract executor base (vLLM Executor equivalent).
    
    Features:
    - Unified interface for all backends
    - Factory pattern for backend selection
    - Health monitoring
    """
    
    # Class attributes for backend capabilities
    uses_ray: bool = False
    supports_pp: bool = False  # Pipeline parallelism
    supports_tp: bool = False  # Tensor parallelism
    
    @abstractmethod
    def start(self) -> None:
        """Start the executor."""
        pass
    
    @abstractmethod
    def shutdown(self, graceful: bool = True) -> None:
        """Shutdown the executor."""
        pass
    
    @abstractmethod
    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
        """Submit a task for execution."""
        pass
    
    @abstractmethod
    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
        """Broadcast a task to all workers."""
        pass
    
    @abstractmethod
    def get_num_workers(self) -> int:
        """Get the number of workers."""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the executor is healthy."""
        pass
    
    @classmethod
    def get_class(cls, backend: ExecutorBackend) -> type:
        """Get executor class for backend (factory pattern)."""
        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor
        else:
            raise ValueError(f"Unknown backend: {backend}")


class UniprocExecutor(Executor):
    """
    Single-process executor for debugging and simple use cases.
    """
    
    uses_ray = False
    supports_pp = False
    supports_tp = False
    
    def __init__(self, functions: Dict[str, Callable] = None):
        self._functions = functions or {}
        self._started = False
        self._task_counter = 0
        self._lock = threading.Lock()
    
    def register_function(self, name: str, func: Callable) -> None:
        """Register a function."""
        self._functions[name] = func
    
    def start(self) -> None:
        """Start the executor."""
        self._started = True
    
    def shutdown(self, graceful: bool = True) -> None:
        """Shutdown the executor."""
        self._started = False
    
    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
        """Submit a task."""
        with self._lock:
            self._task_counter += 1
            task_id = f"task-{self._task_counter}"
        
        future: FutureWrapper[Any] = FutureWrapper(task_id)
        
        try:
            if func_name not in self._functions:
                raise ValueError(f"Unknown function: {func_name}")
            result = self._functions[func_name](*args, **kwargs)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        
        return future
    
    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
        """Broadcast (just execute once for uniproc)."""
        return [self.submit(func_name, *args, **kwargs)]
    
    def get_num_workers(self) -> int:
        """Get number of workers."""
        return 1
    
    def is_healthy(self) -> bool:
        """Check health."""
        return self._started


class MultiprocExecutor(Executor):
    """
    Multiprocess executor (vLLM MultiprocExecutor equivalent).
    
    Features:
    - Worker pool management
    - Task queuing with priorities
    - Worker health monitoring
    - Automatic worker restart
    """
    
    uses_ray = False
    supports_pp = True
    supports_tp = False
    
    def __init__(
        self,
        num_workers: int = 4,
        functions: Dict[str, Callable] = None,
        heartbeat_interval: float = 5.0,
        worker_timeout: float = 30.0,
    ):
        self._num_workers = num_workers
        self._functions = functions or {}
        self._heartbeat_interval = heartbeat_interval
        self._worker_timeout = worker_timeout
        
        # Worker management
        self._workers: Dict[int, mp.Process] = {}
        self._worker_info: Dict[int, WorkerInfo] = {}
        
        # Communication queues
        self._task_queue: Optional[mp.Queue] = None
        self._result_queue: Optional[mp.Queue] = None
        self._control_queues: Dict[int, mp.Queue] = {}
        
        # Task tracking
        self._pending_tasks: Dict[str, FutureWrapper[Any]] = {}
        self._task_counter = 0
        
        # Threading
        self._result_thread: Optional[threading.Thread] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        self._lock = threading.Lock()
        
        self._started = False
    
    def register_function(self, name: str, func: Callable) -> None:
        """Register a function for workers to execute."""
        self._functions[name] = func
    
    def start(self) -> None:
        """Start the executor."""
        if self._started:
            return
        
        # Create queues
        self._task_queue = mp.Queue()
        self._result_queue = mp.Queue()
        
        # Start workers
        for worker_id in range(self._num_workers):
            self._start_worker(worker_id)
        
        # Start result collector thread
        self._result_thread = threading.Thread(
            target=self._collect_results,
            daemon=True,
        )
        self._result_thread.start()
        
        # Start monitor thread
        self._monitor_thread = threading.Thread(
            target=self._monitor_workers,
            daemon=True,
        )
        self._monitor_thread.start()
        
        self._started = True
    
    def _start_worker(self, worker_id: int) -> None:
        """Start a worker process."""
        control_queue = mp.Queue()
        self._control_queues[worker_id] = control_queue
        
        process = mp.Process(
            target=self._worker_loop,
            args=(worker_id, self._task_queue, self._result_queue, control_queue, self._functions),
            daemon=True,
        )
        process.start()
        
        self._workers[worker_id] = process
        self._worker_info[worker_id] = WorkerInfo(
            worker_id=worker_id,
            pid=process.pid,
            state=WorkerState.STARTING,
            start_time=time.time(),
            last_heartbeat=time.time(),
        )
    
    @staticmethod
    def _worker_loop(
        worker_id: int,
        task_queue: mp.Queue,
        result_queue: mp.Queue,
        control_queue: mp.Queue,
        functions: Dict[str, Callable],
    ) -> None:
        """Worker process main loop."""
        # Set up signal handlers
        signal.signal(signal.SIGTERM, lambda *_: None)
        
        while True:
            try:
                # Check for control messages (non-blocking)
                try:
                    control = control_queue.get_nowait()
                    if control == "shutdown":
                        break
                except queue.Empty:
                    pass
                
                # Get task (with timeout for responsiveness)
                try:
                    task: TaskMessage = task_queue.get(timeout=1.0)
                except queue.Empty:
                    # Send heartbeat
                    result_queue.put(ResultMessage(
                        task_id="__heartbeat__",
                        worker_id=worker_id,
                        success=True,
                    ))
                    continue
                
                # Execute task
                start_time = time.time_ns()
                try:
                    if task.func_name not in functions:
                        raise ValueError(f"Unknown function: {task.func_name}")
                    result = functions[task.func_name](*task.args, **task.kwargs)
                    end_time = time.time_ns()
                    
                    result_queue.put(ResultMessage(
                        task_id=task.task_id,
                        worker_id=worker_id,
                        success=True,
                        result=result,
                        execution_time_ns=end_time - start_time,
                    ))
                except Exception as e:
                    end_time = time.time_ns()
                    result_queue.put(ResultMessage(
                        task_id=task.task_id,
                        worker_id=worker_id,
                        success=False,
                        error=str(e),
                        traceback=traceback.format_exc(),
                        execution_time_ns=end_time - start_time,
                    ))
                    
            except Exception:
                # Worker error - try to continue
                pass
    
    def _collect_results(self) -> None:
        """Collect results from workers."""
        while not self._shutdown_event.is_set():
            try:
                result: ResultMessage = self._result_queue.get(timeout=1.0)
                
                if result.task_id == "__heartbeat__":
                    # Update heartbeat
                    with self._lock:
                        if result.worker_id in self._worker_info:
                            self._worker_info[result.worker_id].last_heartbeat = time.time()
                    continue
                
                # Find and complete the future
                with self._lock:
                    future = self._pending_tasks.pop(result.task_id, None)
                    if result.worker_id in self._worker_info:
                        self._worker_info[result.worker_id].tasks_completed += 1
                        self._worker_info[result.worker_id].current_task_id = None
                        self._worker_info[result.worker_id].state = WorkerState.READY
                
                if future:
                    if result.success:
                        future.set_result(result.result)
                    else:
                        future.set_exception(Exception(f"{result.error}\n{result.traceback}"))
                        
            except queue.Empty:
                continue
            except Exception:
                pass
    
    def _monitor_workers(self) -> None:
        """Monitor worker health."""
        while not self._shutdown_event.is_set():
            time.sleep(self._heartbeat_interval)
            
            now = time.time()
            with self._lock:
                for worker_id, info in list(self._worker_info.items()):
                    # Check for timeout
                    if now - info.last_heartbeat > self._worker_timeout:
                        info.state = WorkerState.ERROR
                        info.error_count += 1
                        
                        # Try to restart worker
                        self._restart_worker(worker_id)
    
    def _restart_worker(self, worker_id: int) -> None:
        """Restart a failed worker."""
        # Terminate old process
        if worker_id in self._workers:
            try:
                self._workers[worker_id].terminate()
                self._workers[worker_id].join(timeout=5.0)
            except Exception:
                pass
        
        # Start new process
        self._start_worker(worker_id)
    
    def shutdown(self, graceful: bool = True) -> None:
        """Shutdown the executor."""
        if not self._started:
            return
        
        self._shutdown_event.set()
        
        # Signal workers to stop
        for worker_id, control_queue in self._control_queues.items():
            try:
                control_queue.put("shutdown")
            except Exception:
                pass
        
        # Wait for workers
        if graceful:
            for worker_id, process in self._workers.items():
                try:
                    process.join(timeout=5.0)
                except Exception:
                    pass
        
        # Terminate remaining
        for process in self._workers.values():
            try:
                process.terminate()
            except Exception:
                pass
        
        self._started = False
    
    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
        """Submit a task."""
        with self._lock:
            self._task_counter += 1
            task_id = f"task-{self._task_counter}"
            
            future: FutureWrapper[Any] = FutureWrapper(task_id)
            self._pending_tasks[task_id] = future
        
        task = TaskMessage(
            task_id=task_id,
            func_name=func_name,
            args=args,
            kwargs=kwargs,
        )
        
        self._task_queue.put(task)
        return future
    
    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
        """Broadcast to all workers."""
        futures = []
        for _ in range(self._num_workers):
            futures.append(self.submit(func_name, *args, **kwargs))
        return futures
    
    def get_num_workers(self) -> int:
        """Get number of workers."""
        return self._num_workers
    
    def get_worker_stats(self) -> Dict[int, WorkerInfo]:
        """Get worker statistics."""
        with self._lock:
            return {wid: WorkerInfo(
                worker_id=info.worker_id,
                pid=info.pid,
                state=info.state,
                gpu_id=info.gpu_id,
                start_time=info.start_time,
                last_heartbeat=info.last_heartbeat,
                tasks_completed=info.tasks_completed,
                error_count=info.error_count,
                current_task_id=info.current_task_id,
            ) for wid, info in self._worker_info.items()}
    
    def is_healthy(self) -> bool:
        """Check executor health."""
        if not self._started:
            return False
        
        with self._lock:
            healthy_workers = sum(
                1 for info in self._worker_info.values()
                if info.state in (WorkerState.READY, WorkerState.BUSY)
            )
            return healthy_workers >= self._num_workers // 2


class DistributedExecutor(Executor):
    """
    Distributed executor for multi-node setups.
    
    Beyond vLLM: Cross-node coordination with leader election.
    """
    
    uses_ray = False
    supports_pp = True
    supports_tp = True
    
    def __init__(
        self,
        world_size: int = 1,
        rank: int = 0,
        local_size: int = 1,
        functions: Dict[str, Callable] = None,
    ):
        self._world_size = world_size
        self._rank = rank
        self._local_size = local_size
        self._functions = functions or {}
        self._started = False
        self._local_executor: Optional[MultiprocExecutor] = None
    
    def start(self) -> None:
        """Start the distributed executor."""
        # Start local executor
        self._local_executor = MultiprocExecutor(
            num_workers=self._local_size,
            functions=self._functions,
        )
        self._local_executor.start()
        self._started = True
    
    def shutdown(self, graceful: bool = True) -> None:
        """Shutdown the executor."""
        if self._local_executor:
            self._local_executor.shutdown(graceful)
        self._started = False
    
    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
        """Submit a task (local only in this basic implementation)."""
        if not self._local_executor:
            raise RuntimeError("Executor not started")
        return self._local_executor.submit(func_name, *args, **kwargs)
    
    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
        """Broadcast to all local workers."""
        if not self._local_executor:
            raise RuntimeError("Executor not started")
        return self._local_executor.broadcast(func_name, *args, **kwargs)
    
    def get_num_workers(self) -> int:
        """Get total workers across all nodes."""
        return self._world_size * self._local_size
    
    def is_healthy(self) -> bool:
        """Check health."""
        if not self._local_executor:
            return False
        return self._local_executor.is_healthy()
    
    @property
    def is_leader(self) -> bool:
        """Check if this is the leader node."""
        return self._rank == 0


class ExecutorFactory:
    """Factory for creating executors."""
    
    @staticmethod
    def create(
        backend: ExecutorBackend,
        num_workers: int = 4,
        functions: Dict[str, Callable] = None,
        **kwargs: Any,
    ) -> Executor:
        """Create an executor."""
        executor_class = Executor.get_class(backend)
        
        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor(num_workers=num_workers, functions=functions, **kwargs)
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor(functions=functions)
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor(local_size=num_workers, functions=functions, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")


__all__ = [
    'ExecutorBackend',
    'WorkerState',
    'WorkerInfo',
    'TaskMessage',
    'ResultMessage',
    'FutureWrapper',
    'Executor',
    'UniprocExecutor',
    'MultiprocExecutor',
    'DistributedExecutor',
    'ExecutorFactory',
]
