# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Engine Core sub-package."""

from .config import (
    RequestStatus,
    FinishReason,
    Request,
    SchedulerOutput,
    ModelRunnerOutput,
    EngineCoreOutput,
    EngineCoreOutputs,
)
from .base import Scheduler, Executor
from .scheduler import SimpleScheduler
from .executor import MockExecutor
from .engine import EngineCore
from .messaging import EngineCoreProc

def create_engine_core(
    max_batch_size: int = 32,
    max_tokens: int = 4096,
    log_stats: bool = True,
) -> EngineCore:
    """Create an EngineCore with default settings."""
    scheduler = SimpleScheduler(max_batch_size=max_batch_size, max_tokens=max_tokens)
    executor = MockExecutor()
    return EngineCore(scheduler=scheduler, executor=executor, log_stats=log_stats)

__all__ = [
    "RequestStatus",
    "FinishReason",
    "Request",
    "SchedulerOutput",
    "ModelRunnerOutput",
    "EngineCoreOutput",
    "EngineCoreOutputs",
    "Scheduler",
    "SimpleScheduler",
    "Executor",
    "MockExecutor",
    "EngineCore",
    "EngineCoreProc",
    "create_engine_core",
]
