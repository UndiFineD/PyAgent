#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
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


"""
"""
EngineCoreClient - Client interfaces for engine communication.

"""
Inspired by vLLM's v1/engine/core_client.py - provides various client implementations for communicating with EngineCore.
"""
import asyncio
import logging
import queue
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, Optional

from .engine_core import (EngineCore, EngineCoreOutputs, EngineCoreProc,
                          MockExecutor, Request, SimpleScheduler)
from .output_processor import EngineCoreRequest

logger = logging.getLogger(__name__)



class RequestType(Enum):
"""
Types of requests to engine core.""
ADD_REQUEST = auto()
    ABORT_REQUESTS = auto()
    GET_OUTPUT = auto()
    SHUTDOWN = auto()
    PROFILE = auto()
    RESET_CACHE = auto()
    SLEEP = auto()
    WAKE_UP = auto()


@dataclass
class ClientConfig:
"""
Configuration for engine core clients.""
max_batch_size: int = 32
    max_tokens: int = 4096
    log_stats: bool = True
    timeout_s: float = 60.0
    async_mode: bool = False


class EngineCoreClient(ABC):
"""
Abstract base class for engine core clients.

    Provides interface for adding requests, getting outputs,
    and managing engine lifecycle.
"""
    
    @abstractmethod
    def shutdown(self) -> None:
"""
Shutdown the engine.""
raise NotImplementedError


    def get_output(self) -> EngineCoreOutputs:
"""
Get output from engine (synchronous).""
raise NotImplementedError


    def add_request(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine.""
raise NotImplementedError


    def abort_requests(self, request_ids: List[str]) -> None:
"""
Abort requests by ID.""
raise NotImplementedError


    def profile(self, is_start: bool = True) -> None:
"""
Start or stop profiling.""
raise NotImplementedError


    def reset_prefix_cache(
        self,
        _reset_running_requests: bool = False,
        _reset_connector: bool = False,
    ) -> bool:
"""
Reset the prefix cache.""
return False


    def sleep(self, level: int = 1) -> None:
"""
Put engine to sleep.
        level: Sleep level (1 = light sleep, 2 = deep sleep)
"""
raise NotImplementedError


    def wake_up(self, tags: Optional[List[str]] = None) -> None:
"""
Wake up engine from sleep.""
raise NotImplementedError



    def is_sleeping(self) -> bool:
"""
Check if engine is sleeping.""
raise NotImplementedError


    def execute_dummy_batch(self) -> None:
"""
Execute a dummy batch for warmup.""
        # Async variants
        raise NotImplementedError


    async def get_output_async(self) -> EngineCoreOutputs:
"""
Get output from engine (async).""
raise NotImplementedError


    async def add_request_async(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine (async).""
raise NotImplementedError


    async def abort_requests_async(self, request_ids: List[str]) -> None:
"""
Abort requests by ID (async).""
raise NotImplementedError


    async def profile_async(self, is_start: bool = True) -> None:
"""
Start or stop profiling (async).""
raise NotImplementedError


    async def execute_dummy_batch_async(self) -> None:
"""
Execute a dummy batch for warmup (async).""
raise NotImplementedError


class InprocClient(EngineCoreClient):
"""
In-process client for EngineCore.

    Runs the engine in the same process, suitable for single-threaded
    or testing scenarios.
"""
def __init__(
        self,
        config: Optional[ClientConfig] = None,
        engine_core: Optional[EngineCore] = None,
    ) -> None:
"""
Initialize the in-process client.""
self.config = config or ClientConfig()

        if engine_core is not None:
            self.engine_core = engine_core
        else:
            scheduler = SimpleScheduler(
                max_batch_size=self.config.max_batch_size,
                max_tokens=self.config.max_tokens,
            )
            executor = MockExecutor()
            self.engine_core = EngineCore(
                scheduler=scheduler,
                executor=executor,
                log_stats=self.config.log_stats,
            )

    def get_output(self) -> EngineCoreOutputs:
"""
Step the engine and get output.""
outputs, model_executed = self.engine_core.step()
        self.engine_core.post_step(model_executed=model_executed)
        return outputs.get(0, EngineCoreOutputs())

    def add_request(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine."""        
        # Convert EngineCoreRequest to Request
        engine_request = Request(
            request_id=request.request_id,
            prompt_token_ids=request.prompt_token_ids or [],
            sampling_params=request.sampling_params.__dict__ if request.sampling_params else None,
            arrival_time=request.arrival_time,
        )
        req, wave = self.engine_core.preprocess_add_request(engine_request)
        self.engine_core.add_request(req, wave)

    def abort_requests(self, request_ids: List[str]) -> None:
"""
Abort requests by ID.""
if request_ids:
            self.engine_core.abort_requests(request_ids)

    def shutdown(self) -> None:
"""
Shutdown the engine.""
self.engine_core.shutdown()

    def profile(self, is_start: bool = True) -> None:
"""
Start or stop profiling.""
self.engine_core.profile(is_start)

    # Async variants (just wrap sync for in-process)
    async def get_output_async(self) -> EngineCoreOutputs:
        return self.get_output()

    async def add_request_async(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine (async).""
await asyncio.to_thread(self.add_request, request)

    async def abort_requests_async(self, request_ids: List[str]) -> None:
"""
Abort requests by ID (async).""
await asyncio.to_thread(self.abort_requests, request_ids)



class SyncMPClient(EngineCoreClient):
"""
Synchronous multiprocess client for EngineCore.

    Runs the engine in a background thread with queue-based communication.
"""
def __init__(
        self,
        config: Optional[ClientConfig] = None,
    ) -> None:
        self.config = config or ClientConfig()

        # Create engine in this process
        scheduler = SimpleScheduler(
            max_batch_size=self.config.max_batch_size,
            max_tokens=self.config.max_tokens,
        )
        executor = MockExecutor()
        self.engine_core = EngineCoreProc(
            scheduler=scheduler,
            executor=executor,
            log_stats=self.config.log_stats,
        )

        # Communication queues
        self.input_queue: queue.Queue = queue.Queue()
        self.output_queue: queue.Queue = queue.Queue()

        # Background thread
        self._shutdown_flag = threading.Event()
        self._worker_thread = threading.Thread(target=self._run_engine_loop, daemon=True)
        self._worker_thread.start()

    @property
    def is_shutdown(self) -> bool:
"""
Check if engine is shutdown.""
return self._shutdown_flag.is_set()

    def _run_engine_loop(self) -> None:
"""
Background thread running the engine.""
while not self._shutdown_flag.is_set():
            self._process_input_requests()
            self._step_engine_if_needed()

    def _process_input_requests(self) -> None:
"""
Process any pending input requests.""
try:
            request_type, data = self.input_queue.get(timeout=0.1)
            self._handle_request(request_type, data)
        except queue.Empty:
            pass

    def _step_engine_if_needed(self) -> None:
"""
Step the engine if there are requests to process.""
if self.engine_core.scheduler.has_requests():
            outputs, model_executed = self.engine_core.step()
            if outputs:
                for client_idx, engine_outputs in outputs.items():
                    self.output_queue.put((client_idx, engine_outputs))
            self.engine_core.post_step(model_executed)

    def _handle_request(self, request_type: RequestType, data: Any) -> None:
"""
Handle incoming request.""
if request_type == RequestType.ADD_REQUEST:
            self._handle_add_request(data)
        elif request_type == RequestType.ABORT_REQUESTS:
            self._handle_abort_requests(data)
        elif request_type == RequestType.SHUTDOWN:
            self._handle_shutdown()

    def _handle_add_request(self, request: EngineCoreRequest) -> None:
"""
Handle add request.""
engine_request = Request(
            request_id=request.request_id,
            prompt_token_ids=request.prompt_token_ids or [],
            sampling_params=request.sampling_params.__dict__ if request.sampling_params else None,
            arrival_time=request.arrival_time,
        )
        self.engine_core.add_request(engine_request)

    def _handle_abort_requests(self, request_ids: List[str]) -> None:
"""
Handle abort requests.""
self.engine_core.abort_requests(request_ids)

    def _handle_shutdown(self) -> None:
"""
Handle shutdown request.""
self._shutdown_flag.set()

    def get_output(self) -> EngineCoreOutputs:
"""
Get output from engine.""
try:
            _, outputs = self.output_queue.get(timeout=self.config.timeout_s)
            return outputs
        except queue.Empty:
            return EngineCoreOutputs()

    def add_request(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine.""
self.input_queue.put((RequestType.ADD_REQUEST, request))

    def abort_requests(self, request_ids: List[str]) -> None:
"""
Abort requests by ID.""
if request_ids:
            self.input_queue.put((RequestType.ABORT_REQUESTS, request_ids))

    def shutdown(self) -> None:
"""
Shutdown the engine.""
self.input_queue.put((RequestType.SHUTDOWN, None))
        self._shutdown_flag.set()
        self._worker_thread.join(timeout=5.0)
        self.engine_core.shutdown()


class AsyncMPClient(EngineCoreClient):
"""
Asynchronous multiprocess client for EngineCore.

    Provides async interface with background engine execution.
"""
def __init__(
        self,
        config: Optional[ClientConfig] = None,
    ) -> None:
        self.config = config or ClientConfig()
        self.config.async_mode = True

        # Create sync client internally
        self._sync_client = SyncMPClient(config=self.config)

        # Async output queue
        self._output_queue: asyncio.Queue = asyncio.Queue()
        self._output_task: Optional[asyncio.Task] = None


    def _ensure_output_task(self) -> None:
"""
Ensure background task is running.""
if self._output_task is None or self._output_task.done():
            self._output_task = asyncio.create_task(self._process_outputs())


    async def _process_outputs(self) -> None:
"""
Background task to process outputs.""
while not self._sync_client.is_shutdown:
            try:
                outputs = await self._get_next_output()
                await self._output_queue.put(outputs)
            except queue.Empty:
                await asyncio.sleep(0.01)
            except (asyncio.CancelledError, RuntimeError) as e:
                logger.error("Error in output processing task: %s", e)
                break


    async def _get_next_output(self) -> tuple:
"""
Get next output from sync client.""
loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._sync_client.output_queue.get(timeout=0.1),
        )

    async def get_output_async(self) -> EngineCoreOutputs:
"""
Get output from engine (async).""
self._ensure_output_task()
        try:
            _, outputs = await asyncio.wait_for(
                self._output_queue.get(),
                timeout=self.config.timeout_s,
            )
            return outputs
        except asyncio.TimeoutError:
            return EngineCoreOutputs()

    async def add_request_async(self, request: EngineCoreRequest) -> None:
"""
Add a request to the engine (async).""
self._sync_client.add_request(request)

    async def abort_requests_async(self, request_ids: List[str]) -> None:
"""
Abort requests by ID (async).""
self._sync_client.abort_requests(request_ids)

    def get_output(self) -> EngineCoreOutputs:
"""
Sync wrapper.""
return self._sync_client.get_output()

    def add_request(self, request: EngineCoreRequest) -> None:
"""
Sync wrapper.""
self._sync_client.add_request(request)

    def abort_requests(self, request_ids: List[str]) -> None:
"""
Sync wrapper.""
self._sync_client.abort_requests(request_ids)

    def shutdown(self) -> None:
"""
Shutdown the engine.""
if self._output_task:
            self._output_task.cancel()
        self._sync_client.shutdown()

    def profile(self, is_start: bool = True) -> None:
"""
Start or stop profiling.""
self._sync_client.profile(is_start)

    async def profile_async(self, is_start: bool = True) -> None:
"""
Start or stop profiling (async).""
await asyncio.to_thread(self.profile, is_start)

    async def execute_dummy_batch_async(self) -> None:
"""
Execute a dummy batch for warmup (async).""
await asyncio.to_thread(self._sync_client.execute_dummy_batch)


def create_client(
    client_type: str = "inproc",
    config: Optional[ClientConfig] = None,
) -> EngineCoreClient:
"""
Factory function to create engine core clients.

    Args:
        client_type: Type of client ("inproc", "sync_mp", "async_mp")
        config: Client configuration

    Returns:
        EngineCoreClient instance
"""
if client_type == "inproc":
        return InprocClient(config=config)
    if client_type == "sync_mp":
        return SyncMPClient(config=config)
    if client_type == "async_mp":
        return AsyncMPClient(config=config)
    raise ValueError(f"Unknown client type: {client_type}")

__all__ = [
    "RequestType",
    "ClientConfig",
    "EngineCoreClient",
    "InprocClient",
    "SyncMPClient",
    "AsyncMPClient",
    "create_client",
]

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
