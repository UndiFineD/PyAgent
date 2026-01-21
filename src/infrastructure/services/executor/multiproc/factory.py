from __future__ import annotations
from typing import Any, Callable, Dict
from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.types import ExecutorBackend
from src.infrastructure.services.executor.multiproc.uniproc import UniprocExecutor
from src.infrastructure.services.executor.multiproc.multiproc_logic import MultiprocExecutor
from src.infrastructure.services.executor.multiproc.distributed import DistributedExecutor

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
        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor(num_workers=num_workers, functions=functions, **kwargs)
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor(functions=functions)
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor(local_size=num_workers, functions=functions, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")
