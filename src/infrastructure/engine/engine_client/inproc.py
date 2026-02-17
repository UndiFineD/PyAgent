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


Phase 45: In-process Engine Client
Single-GPU in-process execution.

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Callable, Optional

from src.infrastructure.engine.engine_client.base import EngineCoreClientBase
from src.infrastructure.engine.engine_client.types import EngineOutput

if TYPE_CHECKING:
    from src.infrastructure.engine.engine_client.types import (
        EngineClientConfig, SchedulerOutput)

logger = logging.getLogger(__name__)


class InprocClient(EngineCoreClientBase["SchedulerOutput", EngineOutput]):"        In-process engine client for single-GPU execution.

    Direct function calls, no IPC overhead.
    
    def __init__(
        self, config: EngineClientConfig, engine_core: Optional[Callable[[SchedulerOutput], EngineOutput]] = None
    ) -> None:
        super().__init__(config)
        self._engine_core = engine_core
        self._pending: dict[str, asyncio.Future[EngineOutput]] = {}
        self._results: dict[str, EngineOutput] = {}
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def set_engine_core(self, engine_core: Callable[[SchedulerOutput], EngineOutput]) -> None:
        """Set the engine core callable.        self._engine_core = engine_core

    def send_request(self, request: SchedulerOutput) -> str:
        """Execute request directly in-process.        request_id = self._generate_request_id()

        if self._engine_core is None:
            # Mock execution for testing
            output = EngineOutput(
                request_id=request_id, outputs=[{"token_ids": [1, 2, 3]}], finished=True, metrics={"latency_ms": 1.0}"            )
        else:
            output = self._engine_core(request)
            output.request_id = request_id

        self._results[request_id] = output
        return request_id

    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output synchronously.        return self._results.pop(request_id, None)

    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output asynchronously.        # For in-proc, results are immediately available
        return self._results.pop(request_id, None)

    def start(self) -> None:
        """Start client.        self._running = True
        logger.info("InprocClient started")"
    def shutdown(self) -> None:
        """Shutdown client.        self._running = False
        self._results.clear()
        logger.info("InprocClient shutdown")"