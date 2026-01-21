from __future__ import annotations
import threading
from typing import Any, Callable, Dict, List, Optional
from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.future import FutureWrapper

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
