# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
DistributedCoordinator - Data-parallel and distributed engine coordination.

Inspired by vLLM's v1/engine/coordinator.py and v1/executor patterns.
Provides multi-process worker management, load balancing, and engine lifecycle.
"""

from __future__ import annotations

import asyncio
import logging
import multiprocessing as mp
import os
import queue
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

import numpy as np

logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Configuration
# =============================================================================


class EngineState(Enum):
    """State of a distributed engine instance."""
    
    INITIALIZING = auto()   # Engine is starting up
    READY = auto()          # Engine is ready to process
    BUSY = auto()           # Engine is processing requests
    DRAINING = auto()       # Engine is draining requests
    STOPPED = auto()        # Engine has stopped
    ERROR = auto()          # Engine encountered an error


class WorkerState(Enum):
    """State of a worker process."""
    
    STARTING = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPING = auto()
    STOPPED = auto()
    ERROR = auto()


class LoadBalancingStrategy(Enum):
    """Load balancing strategies for data parallel."""
    
    ROUND_ROBIN = auto()
    LEAST_LOADED = auto()
    RANDOM = auto()
    CONSISTENT_HASH = auto()


@dataclass
class ParallelConfig:
    """Configuration for parallelism.
    
    Inspired by vLLM's ParallelConfig.
    
    Attributes:
        data_parallel_size: Number of data parallel replicas.
        tensor_parallel_size: Number of tensor parallel ranks.
        pipeline_parallel_size: Number of pipeline stages.
        world_size: Total number of distributed ranks.
        distributed_executor_backend: Backend type (mp, ray).
        worker_use_ray: Whether workers use Ray.
        max_parallel_loading: Max workers loading simultaneously.
    """
    
    data_parallel_size: int = 1
    tensor_parallel_size: int = 1
    pipeline_parallel_size: int = 1
    distributed_executor_backend: str = "mp"
    worker_use_ray: bool = False
    max_parallel_loading: int = 4
    
    @property
    def world_size(self) -> int:
        """Total number of distributed ranks."""
        return (
            self.data_parallel_size
            * self.tensor_parallel_size
            * self.pipeline_parallel_size
        )
    
    @property
    def is_distributed(self) -> bool:
        """Check if running in distributed mode."""
        return self.world_size > 1


@dataclass
class EngineIdentity:
    """Identity of a distributed engine instance.
    
    Inspired by vLLM's coordinator identity management.
    
    Attributes:
        dp_rank: Data parallel rank.
        dp_size: Data parallel world size.
        address: Network address.
        engine_id: Unique engine identifier.
    """
    
    dp_rank: int
    dp_size: int
    address: str = ""
    engine_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self) -> str:
        return f"Engine[{self.engine_id}:DP{self.dp_rank}/{self.dp_size}]"


@dataclass
class WorkerIdentity:
    """Identity of a worker process."""
    
    worker_id: int
    engine_id: str
    rank: int
    local_rank: int
    world_size: int
    tp_rank: int = 0
    pp_rank: int = 0


# =============================================================================
# Message Types
# =============================================================================


@dataclass
class CoordinatorMessage:
    """Base message type for coordinator communication."""
    
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)


@dataclass
class RequestMessage(CoordinatorMessage):
    """Request message sent to workers."""
    
    request_id: str = ""
    input_data: Any = None
    priority: int = 0


@dataclass
class ResponseMessage(CoordinatorMessage):
    """Response message from workers."""
    
    request_id: str = ""
    output_data: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class ControlMessage(CoordinatorMessage):
    """Control message for worker management."""
    
    command: str = ""  # "start", "stop", "pause", "resume", "health"
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricsMessage(CoordinatorMessage):
    """Metrics message from workers."""
    
    worker_id: int = 0
    queue_depth: int = 0
    active_requests: int = 0
    total_processed: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0


# =============================================================================
# Worker Abstract Base Class
# =============================================================================


class BaseWorker(ABC):
    """Abstract base class for distributed workers.
    
    Workers receive requests, process them, and return results.
    """
    
    def __init__(self, identity: WorkerIdentity):
        self.identity = identity
        self.state = WorkerState.STARTING
        self._total_processed = 0
        self._error_count = 0
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the worker (load models, etc.)."""
        ...
    
    @abstractmethod
    def process(self, request: RequestMessage) -> ResponseMessage:
        """Process a single request.
        
        Args:
            request: Request to process.
        
        Returns:
            Response with output data.
        """
        ...
    
    @abstractmethod
    def shutdown(self) -> None:
        """Clean up worker resources."""
        ...
    
    def get_metrics(self) -> MetricsMessage:
        """Get worker metrics."""
        return MetricsMessage(
            worker_id=self.identity.worker_id,
            total_processed=self._total_processed,
            error_count=self._error_count,
        )


# =============================================================================
# Worker Process Wrapper
# =============================================================================


class WorkerProcess:
    """Wrapper for a worker running in a subprocess.
    
    Inspired by vLLM's CoreEngineProc.
    """
    
    def __init__(
        self,
        worker_id: int,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        engine_id: str,
        rank: int,
        world_size: int,
    ):
        self.worker_id = worker_id
        self.worker_factory = worker_factory
        self.engine_id = engine_id
        self.rank = rank
        self.world_size = world_size
        
        self._process: Optional[mp.Process] = None
        self._request_queue: mp.Queue = mp.Queue()
        self._response_queue: mp.Queue = mp.Queue()
        self._control_queue: mp.Queue = mp.Queue()
        self._state = WorkerState.STOPPED
        self._metrics = MetricsMessage(worker_id=worker_id)
    
    def start(self) -> None:
        """Start the worker process."""
        self._state = WorkerState.STARTING
        self._process = mp.Process(
            target=self._worker_main,
            args=(
                self.worker_id,
                self.worker_factory,
                self.engine_id,
                self.rank,
                self.world_size,
                self._request_queue,
                self._response_queue,
                self._control_queue,
            ),
            daemon=True,
        )
        self._process.start()
        logger.info("Started worker process %d (pid=%d)", self.worker_id, self._process.pid)
    
    @staticmethod
    def _worker_main(
        worker_id: int,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        engine_id: str,
        rank: int,
        world_size: int,
        request_queue: mp.Queue,
        response_queue: mp.Queue,
        control_queue: mp.Queue,
    ) -> None:
        """Main function running in the worker process."""
        identity = WorkerIdentity(
            worker_id=worker_id,
            engine_id=engine_id,
            rank=rank,
            local_rank=rank,
            world_size=world_size,
        )
        
        worker = worker_factory(identity)
        
        try:
            worker.initialize()
            worker.state = WorkerState.RUNNING
            
            while worker.state == WorkerState.RUNNING:
                # Check for control messages
                try:
                    control = control_queue.get_nowait()
                    if control.command == "stop":
                        break
                    elif control.command == "pause":
                        worker.state = WorkerState.PAUSED
                    elif control.command == "resume":
                        worker.state = WorkerState.RUNNING
                    elif control.command == "health":
                        response_queue.put(worker.get_metrics())
                except queue.Empty:
                    pass
                
                # Process requests
                try:
                    request = request_queue.get(timeout=0.1)
                    start = time.time()
                    
                    try:
                        response = worker.process(request)
                        response.latency_ms = (time.time() - start) * 1000
                        worker._total_processed += 1
                    except Exception as e:
                        response = ResponseMessage(
                            request_id=request.request_id,
                            error=str(e),
                        )
                        worker._error_count += 1
                    
                    response_queue.put(response)
                    
                except queue.Empty:
                    continue
        
        finally:
            worker.shutdown()
    
    def stop(self, timeout: float = 5.0) -> None:
        """Stop the worker process."""
        if self._process is None:
            return
        
        self._control_queue.put(ControlMessage(command="stop"))
        self._process.join(timeout=timeout)
        
        if self._process.is_alive():
            logger.warning("Worker %d did not stop gracefully, terminating", self.worker_id)
            self._process.terminate()
            self._process.join(timeout=1.0)
        
        self._state = WorkerState.STOPPED
    
    def submit(self, request: RequestMessage) -> None:
        """Submit a request to the worker."""
        self._request_queue.put(request)
    
    def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response from the worker."""
        try:
            return self._response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    @property
    def is_alive(self) -> bool:
        """Check if the worker process is alive."""
        return self._process is not None and self._process.is_alive()


# =============================================================================
# Data Parallel Coordinator
# =============================================================================


class DPCoordinator:
    """Coordinator for data-parallel engine instances.
    
    Inspired by vLLM's DPCoordinator and dp_lb_pool patterns.
    Manages multiple engine instances and distributes requests.
    """
    
    def __init__(
        self,
        parallel_config: ParallelConfig,
        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
    ):
        self.config = parallel_config
        self.load_balancing = load_balancing
        
        self._engines: Dict[str, EngineIdentity] = {}
        self._engine_states: Dict[str, EngineState] = {}
        self._engine_metrics: Dict[str, MetricsMessage] = {}
        
        self._round_robin_idx = 0
        self._lock = threading.Lock()
        self._running = False
    
    def register_engine(self, identity: EngineIdentity) -> None:
        """Register a new engine instance.
        
        Args:
            identity: Engine identity.
        """
        with self._lock:
            self._engines[identity.engine_id] = identity
            self._engine_states[identity.engine_id] = EngineState.READY
            self._engine_metrics[identity.engine_id] = MetricsMessage()
            logger.info("Registered engine: %s", identity)
    
    def deregister_engine(self, engine_id: str) -> None:
        """Deregister an engine instance.
        
        Args:
            engine_id: Engine ID to deregister.
        """
        with self._lock:
            self._engines.pop(engine_id, None)
            self._engine_states.pop(engine_id, None)
            self._engine_metrics.pop(engine_id, None)
            logger.info("Deregistered engine: %s", engine_id)
    
    def select_engine(self, request_id: str = None) -> Optional[str]:
        """Select an engine for processing.
        
        Args:
            request_id: Request ID (for consistent hashing).
        
        Returns:
            Engine ID, or None if no engines available.
        """
        with self._lock:
            ready_engines = [
                eid for eid, state in self._engine_states.items()
                if state == EngineState.READY
            ]
            
            if not ready_engines:
                return None
            
            if self.load_balancing == LoadBalancingStrategy.ROUND_ROBIN:
                idx = self._round_robin_idx % len(ready_engines)
                self._round_robin_idx += 1
                return ready_engines[idx]
            
            elif self.load_balancing == LoadBalancingStrategy.LEAST_LOADED:
                # Select engine with lowest queue depth
                min_load = float('inf')
                selected = ready_engines[0]
                for eid in ready_engines:
                    metrics = self._engine_metrics.get(eid)
                    if metrics and metrics.queue_depth < min_load:
                        min_load = metrics.queue_depth
                        selected = eid
                return selected
            
            elif self.load_balancing == LoadBalancingStrategy.RANDOM:
                return ready_engines[np.random.randint(len(ready_engines))]
            
            elif self.load_balancing == LoadBalancingStrategy.CONSISTENT_HASH:
                if request_id:
                    idx = hash(request_id) % len(ready_engines)
                    return ready_engines[idx]
                return ready_engines[0]
            
            return ready_engines[0]
    
    def update_metrics(self, engine_id: str, metrics: MetricsMessage) -> None:
        """Update metrics for an engine.
        
        Args:
            engine_id: Engine ID.
            metrics: Updated metrics.
        """
        with self._lock:
            self._engine_metrics[engine_id] = metrics
    
    def set_engine_state(self, engine_id: str, state: EngineState) -> None:
        """Set engine state.
        
        Args:
            engine_id: Engine ID.
            state: New state.
        """
        with self._lock:
            if engine_id in self._engine_states:
                self._engine_states[engine_id] = state
    
    def get_engine_states(self) -> Dict[str, EngineState]:
        """Get all engine states."""
        with self._lock:
            return dict(self._engine_states)
    
    @property
    def num_engines(self) -> int:
        """Number of registered engines."""
        return len(self._engines)
    
    @property
    def num_ready(self) -> int:
        """Number of ready engines."""
        with self._lock:
            return sum(1 for s in self._engine_states.values() if s == EngineState.READY)


# =============================================================================
# Multi-Process Client
# =============================================================================


T = TypeVar("T")


class MPClient(Generic[T]):
    """Client for communicating with worker processes.
    
    Inspired by vLLM's MPClient pattern.
    Synchronous interface for multi-process workers.
    """
    
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
        """Start all worker processes."""
        for i in range(self.config.data_parallel_size):
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
        time.sleep(0.5)
        logger.info("Started %d workers", len(self._workers))
    
    def stop(self) -> None:
        """Stop all worker processes."""
        for worker in self._workers:
            worker.stop()
        self._workers.clear()
        logger.info("Stopped all workers")
    
    def submit(self, request: RequestMessage) -> None:
        """Submit a request to be processed.
        
        Uses round-robin distribution by default.
        """
        with self._lock:
            worker_id = hash(request.request_id) % len(self._workers)
            self._pending[request.request_id] = worker_id
            self._workers[worker_id].submit(request)
    
    def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response from any worker."""
        # Poll all workers
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
        """Number of active workers."""
        return len(self._workers)
    
    @property
    def num_pending(self) -> int:
        """Number of pending requests."""
        return len(self._pending)


# =============================================================================
# Async Multi-Process Client
# =============================================================================


class AsyncMPClient(Generic[T]):
    """Async client for communicating with worker processes.
    
    Inspired by vLLM's AsyncMPClient.
    Async interface for non-blocking operations.
    """
    
    def __init__(
        self,
        worker_factory: Callable[[WorkerIdentity], BaseWorker],
        parallel_config: ParallelConfig,
    ):
        self._sync_client = MPClient[T](worker_factory, parallel_config)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._executor = None
    
    async def start(self) -> None:
        """Start worker processes."""
        self._loop = asyncio.get_event_loop()
        await self._loop.run_in_executor(None, self._sync_client.start)
    
    async def stop(self) -> None:
        """Stop worker processes."""
        if self._loop:
            await self._loop.run_in_executor(None, self._sync_client.stop)
    
    async def submit(self, request: RequestMessage) -> None:
        """Submit a request asynchronously."""
        if self._loop:
            await self._loop.run_in_executor(None, self._sync_client.submit, request)
    
    async def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response asynchronously."""
        if self._loop:
            return await self._loop.run_in_executor(
                None, self._sync_client.get_response, timeout
            )
        return None


# =============================================================================
# Data Parallel Load Balanced Client
# =============================================================================


class DPLBAsyncMPClient(Generic[T]):
    """Data-parallel load-balanced async client.
    
    Inspired by vLLM's dp_lb_pool and DPAsyncMPClient.
    Combines coordination with async multi-process execution.
    """
    
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
        """Start all data-parallel instances."""
        for dp_rank in range(self.config.data_parallel_size):
            engine_id = f"engine_{dp_rank}"
            identity = EngineIdentity(
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
        
        logger.info("Started %d data-parallel instances", len(self._clients))
    
    async def stop(self) -> None:
        """Stop all data-parallel instances."""
        for engine_id, client in self._clients.items():
            await client.stop()
            self._coordinator.deregister_engine(engine_id)
        
        self._clients.clear()
    
    async def submit(self, request: RequestMessage) -> None:
        """Submit a request with load balancing."""
        engine_id = self._coordinator.select_engine(request.request_id)
        if engine_id and engine_id in self._clients:
            await self._clients[engine_id].submit(request)
        else:
            raise RuntimeError("No available engines")
    
    async def get_response(self, timeout: float = None) -> Optional[ResponseMessage]:
        """Get a response from any client."""
        # Poll all clients
        tasks = [
            asyncio.create_task(client.get_response(timeout=0.01))
            for client in self._clients.values()
        ]
        
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
        """Number of data-parallel engines."""
        return self._coordinator.num_engines
    
    @property
    def num_ready(self) -> int:
        """Number of ready engines."""
        return self._coordinator.num_ready


# =============================================================================
# Executor Interface
# =============================================================================


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


# =============================================================================
# Convenience Functions
# =============================================================================


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
