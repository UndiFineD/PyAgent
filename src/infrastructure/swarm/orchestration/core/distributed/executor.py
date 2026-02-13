#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Executor interface and implementations for distributed execution.
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from .client import DPLBAsyncMPClient
from .config import LoadBalancingStrategy, ParallelConfig, WorkerIdentity
from .messages import RequestMessage, ResponseMessage
from .worker import BaseWorker

logger = logging.getLogger(__name__)


class DistributedExecutor(ABC):
    """Abstract interface for distributed execution.

    Inspired by vLLM's ExecutorBase.
    """

    @abstractmethod
    async def start(self) -> None:
        """Start the executor."""
        ...

    @abstractmethod
    async def stop(self) -> None:
        """Stop the executor."""
        ...

    @abstractmethod
    async def execute(self, request: RequestMessage) -> ResponseMessage:
        """Execute a request.

        Args:
            request: Request to execute.

        Returns:
            Response with results.
        """
        ...

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if executor is ready."""
        ...


class MultiProcessExecutor(DistributedExecutor):
    """Multi-process distributed executor.

    Implements distributed execution using multiprocessing.
    """

    def __init__(
        self,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        parallel_config: ParallelConfig,
        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
    ):
        self._client = DPLBAsyncMPClient[Any](
            worker_factory=worker_factory,
            parallel_config=parallel_config,
            load_balancing=load_balancing,
        )
        self._ready = False

    async def start(self) -> None:
        """Start the multi-process executor."""
        await self._client.start()
        self._ready = True
        logger.info("MultiProcessExecutor started")

    async def stop(self) -> None:
        """Stop the multi-process executor."""
        self._ready = False
        await self._client.stop()
        logger.info("MultiProcessExecutor stopped")

    async def execute(self, request: RequestMessage) -> ResponseMessage:
        """Execute a request across workers."""
        await self._client.submit(request)

        response = await self._client.get_response(timeout=30.0)
        if response is None:
            return ResponseMessage(
                request_id=request.request_id,
                error="Timeout waiting for response",
            )

        return response

    def is_ready(self) -> bool:
        """Check if executor is ready."""
        return self._ready and self._client.num_ready > 0


def create_distributed_executor(
    worker_factory: Callable[[WorkerIdentity], BaseWorker],
    parallel_config: Optional[ParallelConfig] = None,
    load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
) -> DistributedExecutor:
    """Create a distributed executor.

    Args:
        worker_factory: Factory function for creating workers.
        parallel_config: Parallel configuration.
        load_balancing: Load balancing strategy.

    Returns:
        Configured distributed executor.
    """
    config = parallel_config or ParallelConfig()

    return MultiProcessExecutor(
        worker_factory=worker_factory,
        parallel_config=config,
        load_balancing=load_balancing,
    )


def get_dp_rank() -> int:
    """Get current data parallel rank from environment."""
    return int(os.environ.get("DP_RANK", "0"))


def get_dp_size() -> int:
    """Get data parallel world size from environment."""
    return int(os.environ.get("DP_SIZE", "1"))


def get_tp_rank() -> int:
    """Get current tensor parallel rank from environment."""
    return int(os.environ.get("TP_RANK", "0"))


def get_tp_size() -> int:
    """Get tensor parallel world size from environment."""
    return int(os.environ.get("TP_SIZE", "1"))
