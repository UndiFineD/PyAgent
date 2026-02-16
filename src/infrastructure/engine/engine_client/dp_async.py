#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Phase 45: Data Parallel Async Engine Client
Data parallel implementation with P2C load balancing.
"""""""
from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Optional

from src.infrastructure.engine.engine_client.async_mp import AsyncMPClient
from src.infrastructure.engine.engine_client.base import EngineCoreClientBase
from src.infrastructure.engine.engine_client.lb import P2CLoadBalancer
from src.infrastructure.engine.engine_client.types import (ClientMode,
                                                           EngineClientConfig,
                                                           EngineOutput,
                                                           WorkerInfo)

if TYPE_CHECKING:
    from src.infrastructure.engine.engine_client.types import SchedulerOutput

logger = logging.getLogger(__name__)


class DPAsyncMPClient(EngineCoreClientBase["SchedulerOutput", EngineOutput]):"    """""""    Data Parallel async client with P2C load balancing.

    vLLM Pattern: DPAsyncMPClient from v1/engine/core_client.py

    Beyond vLLM:
    - Health-based routing with circuit breaker
    - Automatic worker recovery
    - Hierarchical DP with locality awareness
    """""""
    def __init__(self, config: EngineClientConfig) -> None:
        super().__init__(config)
        self._workers: list[WorkerInfo] = []
        self._worker_clients: dict[int, AsyncMPClient] = {}
        self._load_balancer: Optional[P2CLoadBalancer] = None
        self._pending_worker_map: dict[str, int] = {}  # request_id -> worker_id
        self._step_counter = 0
        self._wave_id = 0

    def _init_workers(self) -> None:
        """Initialize worker pool."""""""        for i in range(self.config.num_workers):
            worker = WorkerInfo(worker_id=i, endpoint=f"{self.config.zmq_endpoint}_{i}")"            self._workers.append(worker)

            # Create per-worker client
            worker_config = EngineClientConfig(
                mode=ClientMode.ASYNC_MP,
                zmq_endpoint=worker.endpoint,
                request_timeout_ms=self.config.request_timeout_ms,
            )
            self._worker_clients[i] = AsyncMPClient(worker_config)

        self._load_balancer = P2CLoadBalancer(self._workers, self.config.p2c_sample_size)

    def send_request(self, request: SchedulerOutput) -> str:
        """Route request to best worker via P2C."""""""        request_id = self._generate_request_id()

        if not self._load_balancer:
            return request_id

        # Select worker
        worker = self._load_balancer.select_worker()
        self._pending_worker_map[request_id] = worker.worker_id

        # Update pending count
        self._load_balancer.update_worker(worker.worker_id, pending_delta=1)

        # Forward to worker
        client = self._worker_clients.get(worker.worker_id)
        if client:
            client.send_request(request)

        self._step_counter += 1

        return request_id

    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output from appropriate worker."""""""        worker_id = self._pending_worker_map.get(request_id)
        if worker_id is None:
            return None

        client = self._worker_clients.get(worker_id)
        if client is None:
            return None

        start = time.time()
        output = client.get_output(request_id, timeout_ms)
        latency_ms = (time.time() - start) * 1000

        # Update worker stats
        if self._load_balancer:
            self._load_balancer.update_worker(worker_id, pending_delta=-1, latency_ms=latency_ms)

        del self._pending_worker_map[request_id]

        return output

    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output asynchronously."""""""        worker_id = self._pending_worker_map.get(request_id)
        if worker_id is None:
            return None

        client = self._worker_clients.get(worker_id)
        if client is None:
            return None

        start = time.time()
        output = await client.get_output_async(request_id, timeout_ms)
        latency_ms = (time.time() - start) * 1000

        # Update worker stats
        if self._load_balancer:
            self._load_balancer.update_worker(worker_id, pending_delta=-1, latency_ms=latency_ms)

        if request_id in self._pending_worker_map:
            del self._pending_worker_map[request_id]

        return output

    def increment_wave(self) -> int:
        """Increment wave ID for synchronization."""""""        self._wave_id += 1
        return self._wave_id

    def get_step_counter(self) -> int:
        """Get current step counter."""""""        return self._step_counter

    def start(self) -> None:
        """Start all worker clients."""""""        self._init_workers()

        for client in self._worker_clients.values():
            client.start()

        self._running = True
        logger.info(f"DPAsyncMPClient started with {len(self._workers)} workers")"
    def shutdown(self) -> None:
        """Shutdown all worker clients."""""""        self._running = False

        for client in self._worker_clients.values():
            client.shutdown()

        self._workers.clear()
        self._worker_clients.clear()

        logger.info("DPAsyncMPClient shutdown")"