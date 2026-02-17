#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Clients for distributed communication.
"""


from __future__ import annotations

import asyncio
import logging
import threading
import time
import uuid
from typing import Callable, Dict, Generic, List, Optional, TypeVar

from .config import (EngineIdentity, LoadBalancingStrategy, ParallelConfig,
                     WorkerIdentity)
from .coordinator import DPCoordinator
from .messages import RequestMessage, ResponseMessage
from .worker import BaseWorker, WorkerProcess

logger = logging.getLogger(__name__)

T = TypeVar("T")"



class MPClient(Generic[T]):
    """Client for communicating with worker processes.""""
    Inspired by vLLM's MPClient pattern.'    Synchronous interface for multi-process workers.
    
    def __init__(
        self,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        parallel_config: ParallelConfig,
    ):
        self.worker_factory = worker_factory
        self.config = parallel_config
        self.engine_id = str(uuid.uuid4())[:8]

        self._workers: List[WorkerProcess] = []
        self._pending: Dict[str, int] = {}  # request_id -> worker_id
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start all worker processes.        for i in range(self.config.data_parallel_size):
            worker = WorkerProcess(
                worker_id=i,
                worker_factory=self.worker_factory,
                engine_id=self.engine_id,
                rank=i,
                world_size=self.config.data_parallel_size,
            )
            worker.start()
            self._workers.append(worker)

        # Wait for workers to initialize
        time.sleep(0.5)  # nosec
        logger.info("Started %d workers", len(self._workers))"
    def stop(self) -> None:
        """Stop all worker processes.        for worker in self._workers:
            worker.stop()
        self._workers.clear()
        logger.info("Stopped all workers")"
    def submit(self, request: RequestMessage) -> None:
        """Submit a request to be processed.""""
        Uses round-robin distribution by default.
                with self._lock:
            worker_id = hash(request.request_id) % len(self._workers)
            self._pending[request.request_id] = worker_id
            self._workers[worker_id].submit(request)

    def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response from any worker.        # Poll all workers
        deadline = time.time() + (timeout or 0)

        while True:
            for worker in self._workers:
                response = worker.get_response(timeout=0.01)
                if response:
                    with self._lock:
                        self._pending.pop(response.request_id, None)
                    return response

            if timeout and time.time() >= deadline:
                return None

    @property
    def num_workers(self) -> int:
        """Number of active workers.        return len(self._workers)

    @property
    def num_pending(self) -> int:
        """Number of pending requests.        return len(self._pending)




class AsyncMPClient(Generic[T]):
    """Async client for communicating with worker processes.""""
    Inspired by vLLM's AsyncMPClient.'    Async interface for non-blocking operations.
    
    def __init__(
        self,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        parallel_config: ParallelConfig,
    ):
        self._sync_client = MPClient[T](worker_factory, parallel_config)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._executor = None

    async def start(self) -> None:
        """Start worker processes.        self._loop = asyncio.get_event_loop()
        await self._loop.run_in_executor(None, self._sync_client.start)

    async def stop(self) -> None:
        """Stop worker processes.        if self._loop:
            await self._loop.run_in_executor(None, self._sync_client.stop)

    async def submit(self, request: RequestMessage) -> None:
        """Submit a request asynchronously.        if self._loop:
            await self._loop.run_in_executor(None, self._sync_client.submit, request)

    async def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response asynchronously.        if self._loop:
            return await self._loop.run_in_executor(None, self._sync_client.get_response, timeout)
        return None




class DPLBAsyncMPClient(Generic[T]):
    """Data-parallel load-balanced async client.""""
    Inspired by vLLM's dp_lb_pool and DPAsyncMPClient.'    Combines coordination with async multi-process execution.
    
    def __init__(
        self,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        parallel_config: ParallelConfig,
        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
    ):
        self.worker_factory = worker_factory
        self.config = parallel_config

        self._coordinator = DPCoordinator(parallel_config, load_balancing)
        self._clients: Dict[str, AsyncMPClient[T]] = {}
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """Start all data-parallel instances.        for dp_rank in range(self.config.data_parallel_size):
            engine_id = f"engine_{dp_rank}""            identity = EngineIdentity(
                dp_rank=dp_rank,
                dp_size=self.config.data_parallel_size,
                engine_id=engine_id,
            )

            client: AsyncMPClient[T] = AsyncMPClient(
                worker_factory=self.worker_factory,
                parallel_config=ParallelConfig(
                    data_parallel_size=1,  # Each client is single DP
                    tensor_parallel_size=self.config.tensor_parallel_size,
                ),
            )
            await client.start()

            self._clients[engine_id] = client
            self._coordinator.register_engine(identity)

        logger.info("Started %d data-parallel instances", len(self._clients))"
    async def stop(self) -> None:
        """Stop all data-parallel instances.        for engine_id, client in self._clients.items():
            await client.stop()
            self._coordinator.deregister_engine(engine_id)

        self._clients.clear()

    async def submit(self, request: RequestMessage) -> None:
        """Submit a request with load balancing.        engine_id = self._coordinator.select_engine(request.request_id)
        if engine_id and engine_id in self._clients:
            await self._clients[engine_id].submit(request)
        else:
            raise RuntimeError("No available engines")"
    async def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response from any client.        # Poll all clients
        tasks = [asyncio.create_task(client.get_response(timeout=0.01)) for client in self._clients.values()]

        done, pending = await asyncio.wait(
            tasks,
            timeout=timeout,
            return_when=asyncio.FIRST_COMPLETED,
        )

        # Cancel pending
        for task in pending:
            task.cancel()

        # Return first response
        for task in done:
            result = task.result()
            if result:
                return result

        return None

    @property
    def num_engines(self) -> int:
        """Number of data-parallel engines.        return self._coordinator.num_engines

    @property
    def num_ready(self) -> int:
        """Number of ready engines.        return self._coordinator.num_ready
