from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from src.infrastructure.services.executor.multiproc.types import ExecutorBackend
from src.infrastructure.services.executor.multiproc.future import FutureWrapper

class Executor(ABC):
    """
    Abstract executor base.
    """

    uses_ray: bool = False
    supports_pp: bool = False
    supports_tp: bool = False

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
        from src.infrastructure.services.executor.multiproc.uniproc import UniprocExecutor
        from src.infrastructure.services.executor.multiproc.multiproc_logic import MultiprocExecutor
        from src.infrastructure.services.executor.multiproc.distributed import DistributedExecutor

        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor
        else:
            raise ValueError(f"Unknown backend: {backend}")
