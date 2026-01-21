"""
Phase 45: Multiprocess Executor
vLLM-inspired multiprocess executor with advanced coordination.

Refactored to modular package structure for Phase 317.
Decomposed into types, future, base, and specific implementation modules.
"""

from src.infrastructure.services.executor.multiproc.types import (
    ExecutorBackend, WorkerState, WorkerInfo, TaskMessage, ResultMessage
)
from src.infrastructure.services.executor.multiproc.future import FutureWrapper
from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.uniproc import UniprocExecutor
from src.infrastructure.services.executor.multiproc.multiproc_logic import MultiprocExecutor
from src.infrastructure.services.executor.multiproc.distributed import DistributedExecutor
from src.infrastructure.services.executor.multiproc.factory import ExecutorFactory

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
