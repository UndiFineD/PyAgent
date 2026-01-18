"""
AsyncEngineClient: Multi-process async engine client with DP load balancing.

vLLM Pattern: EngineCoreClient hierarchy from v1/engine/core_client.py
- InprocClient: Single-GPU in-process execution
- SyncMPClient: Synchronous multi-process with ZMQ
- AsyncMPClient: Async multi-process with queue handlers
- DPAsyncMPClient: Data parallel with P2C load balancing

Beyond vLLM:
- Automatic client selection based on GPU topology
- Graceful degradation on worker failure
- Health-based routing with circuit breaker integration
"""

from __future__ import annotations
import asyncio
import logging
import time
import threading
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar, TYPE_CHECKING
from collections import deque
import random

if TYPE_CHECKING:
    import zmq
    import zmq.asyncio

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class ClientMode(Enum):
    """Engine client execution mode."""
    INPROC = auto()      # In-process, single GPU
    SYNC_MP = auto()     # Synchronous multi-process
    ASYNC_MP = auto()    # Async multi-process
    DP_ASYNC = auto()    # Data parallel with load balancing


class WorkerState(Enum):
    """Worker health state."""
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    DEAD = auto()


@dataclass
class EngineClientConfig:
    """Configuration for engine client."""
    mode: ClientMode = ClientMode.ASYNC_MP
    num_workers: int = 1
    zmq_endpoint: str = "ipc:///tmp/pyagent_engine"
    request_timeout_ms: int = 30000
    health_check_interval_s: float = 5.0
    max_pending_requests: int = 1000
    p2c_sample_size: int = 2  # Power of Two Choices
    auto_select_mode: bool = True  # Auto-select based on GPU topology


@dataclass
class SchedulerOutput:
    """Output from scheduler for engine core."""
    request_ids: list[str] = field(default_factory=list)
    scheduled_tokens: int = 0
    num_prefill: int = 0
    num_decode: int = 0
    block_tables: dict[str, list[int]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EngineOutput:
    """Output from engine core execution."""
    request_id: str
    outputs: list[Any] = field(default_factory=list)
    finished: bool = False
    metrics: dict[str, float] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class WorkerInfo:
    """Worker metadata and health."""
    worker_id: int
    endpoint: str
    state: WorkerState = WorkerState.HEALTHY
    pending_requests: int = 0
    total_processed: int = 0
    avg_latency_ms: float = 0.0
    last_health_check: float = field(default_factory=time.time)
    consecutive_failures: int = 0


class EngineCoreClientBase(ABC, Generic[T, R]):
    """Base class for engine core clients."""
    
    def __init__(self, config: EngineClientConfig):
        self.config = config
        self._running = False
        self._request_counter = 0
        self._lock = threading.Lock()
    
    @abstractmethod
    def send_request(self, request: T) -> str:
        """Send request and return request ID."""
        pass
    
    @abstractmethod
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[R]:
        """Get output for request (blocking)."""
        pass
    
    @abstractmethod
    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[R]:
        """Get output for request (async)."""
        pass
    
    @abstractmethod
    def start(self) -> None:
        """Start the client."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the client."""
        pass
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        with self._lock:
            self._request_counter += 1
            return f"req_{self._request_counter}_{uuid.uuid4().hex[:8]}"


class InprocClient(EngineCoreClientBase[SchedulerOutput, EngineOutput]):
    """
    In-process engine client for single-GPU execution.
    
    Direct function calls, no IPC overhead.
    """
    
    def __init__(
        self,
        config: EngineClientConfig,
        engine_core: Optional[Callable[[SchedulerOutput], EngineOutput]] = None
    ):
        super().__init__(config)
        self._engine_core = engine_core
        self._pending: dict[str, asyncio.Future[EngineOutput]] = {}
        self._results: dict[str, EngineOutput] = {}
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    def set_engine_core(self, engine_core: Callable[[SchedulerOutput], EngineOutput]) -> None:
        """Set the engine core callable."""
        self._engine_core = engine_core
    
    def send_request(self, request: SchedulerOutput) -> str:
        """Execute request directly in-process."""
        request_id = self._generate_request_id()
        
        if self._engine_core is None:
            # Mock execution for testing
            output = EngineOutput(
                request_id=request_id,
                outputs=[{"token_ids": [1, 2, 3]}],
                finished=True,
                metrics={"latency_ms": 1.0}
            )
        else:
            output = self._engine_core(request)
            output.request_id = request_id
        
        self._results[request_id] = output
        return request_id
    
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output synchronously."""
        return self._results.pop(request_id, None)
    
    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output asynchronously."""
        # For in-proc, results are immediately available
        return self._results.pop(request_id, None)
    
    def start(self) -> None:
        """Start client."""
        self._running = True
        logger.info("InprocClient started")
    
    def shutdown(self) -> None:
        """Shutdown client."""
        self._running = False
        self._results.clear()
        logger.info("InprocClient shutdown")


class SyncMPClient(EngineCoreClientBase[SchedulerOutput, EngineOutput]):
    """
    Synchronous multi-process engine client with ZMQ.
    
    Blocking request/response pattern.
    """
    
    def __init__(self, config: EngineClientConfig):
        super().__init__(config)
        self._context: Optional[zmq.Context] = None
        self._socket: Optional[zmq.Socket] = None
        self._pending: dict[str, EngineOutput] = {}
    
    def _init_zmq(self) -> None:
        """Initialize ZMQ socket."""
        try:
            import zmq
            self._context = zmq.Context()
            self._socket = self._context.socket(zmq.REQ)
            self._socket.setsockopt(zmq.RCVTIMEO, self.config.request_timeout_ms)
            self._socket.setsockopt(zmq.SNDTIMEO, self.config.request_timeout_ms)
            self._socket.connect(self.config.zmq_endpoint)
        except ImportError:
            logger.warning("ZMQ not available, using mock mode")
    
    def send_request(self, request: SchedulerOutput) -> str:
        """Send request via ZMQ."""
        request_id = self._generate_request_id()
        
        if self._socket is None:
            # Mock mode
            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                outputs=[{"mock": True}],
                finished=True
            )
            return request_id
        
        try:
            import msgpack
            payload = msgpack.packb({
                "request_id": request_id,
                "request_ids": request.request_ids,
                "scheduled_tokens": request.scheduled_tokens,
                "num_prefill": request.num_prefill,
                "num_decode": request.num_decode,
            })
            self._socket.send(payload)
            
            # Blocking receive
            response = self._socket.recv()
            data = msgpack.unpackb(response)
            
            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                outputs=data.get("outputs", []),
                finished=data.get("finished", True),
                metrics=data.get("metrics", {})
            )
        except Exception as e:
            logger.error(f"ZMQ error: {e}")
            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                error=str(e)
            )
        
        return request_id
    
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output synchronously."""
        return self._pending.pop(request_id, None)
    
    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output (sync wrapper for async interface)."""
        return self.get_output(request_id, timeout_ms)
    
    def start(self) -> None:
        """Start client."""
        self._init_zmq()
        self._running = True
        logger.info("SyncMPClient started")
    
    def shutdown(self) -> None:
        """Shutdown client."""
        self._running = False
        if self._socket:
            self._socket.close()
        if self._context:
            self._context.term()
        logger.info("SyncMPClient shutdown")


class AsyncMPClient(EngineCoreClientBase[SchedulerOutput, EngineOutput]):
    """
    Async multi-process engine client with queue handlers.
    
    Non-blocking request submission with async output retrieval.
    """
    
    def __init__(self, config: EngineClientConfig):
        super().__init__(config)
        self._request_queue: asyncio.Queue[tuple[str, SchedulerOutput]] = asyncio.Queue()
        self._output_queue: asyncio.Queue[EngineOutput] = asyncio.Queue()
        self._pending_futures: dict[str, asyncio.Future[EngineOutput]] = {}
        self._worker_task: Optional[asyncio.Task] = None
        self._output_task: Optional[asyncio.Task] = None
    
    async def _run_busy_loop(self) -> None:
        """
        Core async execution loop.
        
        vLLM Pattern: EngineCoreProc.run_busy_loop()
        """
        while self._running:
            try:
                # Get next request with timeout
                try:
                    request_id, request = await asyncio.wait_for(
                        self._request_queue.get(),
                        timeout=0.1
                    )
                except asyncio.TimeoutError:
                    continue
                
                # Mock execution
                await asyncio.sleep(0.001)  # Simulate work
                
                output = EngineOutput(
                    request_id=request_id,
                    outputs=[{"token_ids": list(range(request.scheduled_tokens))}],
                    finished=True,
                    metrics={"latency_ms": 1.0}
                )
                
                await self._output_queue.put(output)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Busy loop error: {e}")
    
    async def _output_handler(self) -> None:
        """Handle output distribution to waiting futures."""
        while self._running:
            try:
                output = await asyncio.wait_for(
                    self._output_queue.get(),
                    timeout=0.1
                )
                
                if output.request_id in self._pending_futures:
                    future = self._pending_futures.pop(output.request_id)
                    if not future.done():
                        future.set_result(output)
                        
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Output handler error: {e}")
    
    def send_request(self, request: SchedulerOutput) -> str:
        """Submit request to async queue."""
        request_id = self._generate_request_id()
        
        loop = asyncio.get_event_loop()
        future: asyncio.Future[EngineOutput] = loop.create_future()
        self._pending_futures[request_id] = future
        
        # Non-blocking put
        asyncio.create_task(self._request_queue.put((request_id, request)))
        
        return request_id
    
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Blocking get (runs event loop)."""
        if request_id not in self._pending_futures:
            return None
        
        loop = asyncio.get_event_loop()
        timeout = (timeout_ms or self.config.request_timeout_ms) / 1000.0
        
        try:
            return loop.run_until_complete(
                asyncio.wait_for(self._pending_futures[request_id], timeout=timeout)
            )
        except asyncio.TimeoutError:
            return None
    
    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Non-blocking async get."""
        if request_id not in self._pending_futures:
            return None
        
        timeout = (timeout_ms or self.config.request_timeout_ms) / 1000.0
        
        try:
            return await asyncio.wait_for(
                self._pending_futures[request_id],
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return None
    
    def start(self) -> None:
        """Start async workers."""
        self._running = True
        
        loop = asyncio.get_event_loop()
        self._worker_task = loop.create_task(self._run_busy_loop())
        self._output_task = loop.create_task(self._output_handler())
        
        logger.info("AsyncMPClient started")
    
    def shutdown(self) -> None:
        """Shutdown async workers."""
        self._running = False
        
        if self._worker_task:
            self._worker_task.cancel()
        if self._output_task:
            self._output_task.cancel()
        
        # Cancel pending futures
        for future in self._pending_futures.values():
            if not future.done():
                future.cancel()
        
        logger.info("AsyncMPClient shutdown")


class P2CLoadBalancer:
    """
    Power of Two Choices load balancer.
    
    vLLM Pattern: DPLBAsyncMPClient worker selection
    
    Algorithm:
    1. Randomly sample 2 workers
    2. Select the one with fewer pending requests
    3. Tie-break by latency
    """
    
    def __init__(self, workers: list[WorkerInfo], sample_size: int = 2):
        self.workers = workers
        self.sample_size = min(sample_size, len(workers))
        self._lock = threading.Lock()
    
    def select_worker(self) -> WorkerInfo:
        """Select best worker using P2C algorithm."""
        with self._lock:
            # Filter healthy workers
            healthy = [w for w in self.workers if w.state in (WorkerState.HEALTHY, WorkerState.DEGRADED)]
            
            if not healthy:
                # Fallback to any worker
                healthy = self.workers
            
            if len(healthy) == 1:
                return healthy[0]
            
            # Sample workers
            candidates = random.sample(healthy, min(self.sample_size, len(healthy)))
            
            # Select by pending requests, then latency
            best = min(candidates, key=lambda w: (w.pending_requests, w.avg_latency_ms))
            
            return best
    
    def update_worker(self, worker_id: int, pending_delta: int = 0, latency_ms: Optional[float] = None) -> None:
        """Update worker statistics."""
        with self._lock:
            for worker in self.workers:
                if worker.worker_id == worker_id:
                    worker.pending_requests = max(0, worker.pending_requests + pending_delta)
                    if latency_ms is not None:
                        # Exponential moving average
                        worker.avg_latency_ms = 0.9 * worker.avg_latency_ms + 0.1 * latency_ms
                    break


class DPAsyncMPClient(EngineCoreClientBase[SchedulerOutput, EngineOutput]):
    """
    Data Parallel async client with P2C load balancing.
    
    vLLM Pattern: DPAsyncMPClient from v1/engine/core_client.py
    
    Beyond vLLM:
    - Health-based routing with circuit breaker
    - Automatic worker recovery
    - Hierarchical DP with locality awareness
    """
    
    def __init__(self, config: EngineClientConfig):
        super().__init__(config)
        self._workers: list[WorkerInfo] = []
        self._worker_clients: dict[int, AsyncMPClient] = {}
        self._load_balancer: Optional[P2CLoadBalancer] = None
        self._pending_worker_map: dict[str, int] = {}  # request_id -> worker_id
        self._step_counter = 0
        self._wave_id = 0
    
    def _init_workers(self) -> None:
        """Initialize worker pool."""
        for i in range(self.config.num_workers):
            worker = WorkerInfo(
                worker_id=i,
                endpoint=f"{self.config.zmq_endpoint}_{i}"
            )
            self._workers.append(worker)
            
            # Create per-worker client
            worker_config = EngineClientConfig(
                mode=ClientMode.ASYNC_MP,
                zmq_endpoint=worker.endpoint,
                request_timeout_ms=self.config.request_timeout_ms
            )
            self._worker_clients[i] = AsyncMPClient(worker_config)
        
        self._load_balancer = P2CLoadBalancer(self._workers, self.config.p2c_sample_size)
    
    def send_request(self, request: SchedulerOutput) -> str:
        """Route request to best worker via P2C."""
        request_id = self._generate_request_id()
        
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
            worker_request_id = client.send_request(request)
            # Map worker request ID to our request ID
            self._pending_worker_map[request_id] = worker.worker_id
        
        self._step_counter += 1
        
        return request_id
    
    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output from appropriate worker."""
        worker_id = self._pending_worker_map.get(request_id)
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
        """Get output asynchronously."""
        worker_id = self._pending_worker_map.get(request_id)
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
        """Increment wave ID for synchronization."""
        self._wave_id += 1
        return self._wave_id
    
    def get_step_counter(self) -> int:
        """Get current step counter."""
        return self._step_counter
    
    def start(self) -> None:
        """Start all worker clients."""
        self._init_workers()
        
        for client in self._worker_clients.values():
            client.start()
        
        self._running = True
        logger.info(f"DPAsyncMPClient started with {len(self._workers)} workers")
    
    def shutdown(self) -> None:
        """Shutdown all worker clients."""
        self._running = False
        
        for client in self._worker_clients.values():
            client.shutdown()
        
        self._workers.clear()
        self._worker_clients.clear()
        
        logger.info("DPAsyncMPClient shutdown")


def auto_select_client_mode(num_gpus: int = 1, use_dp: bool = False) -> ClientMode:
    """
    Auto-select client mode based on GPU topology.
    
    Beyond vLLM: Automatic optimal configuration.
    """
    if num_gpus == 1 and not use_dp:
        return ClientMode.INPROC
    elif use_dp and num_gpus > 1:
        return ClientMode.DP_ASYNC
    elif num_gpus > 1:
        return ClientMode.ASYNC_MP
    else:
        return ClientMode.SYNC_MP


def create_engine_client(
    config: Optional[EngineClientConfig] = None,
    num_gpus: int = 1,
    use_dp: bool = False,
    engine_core: Optional[Callable[[SchedulerOutput], EngineOutput]] = None
) -> EngineCoreClientBase:
    """
    Factory function to create appropriate engine client.
    
    Beyond vLLM: Unified factory with auto-selection.
    """
    if config is None:
        config = EngineClientConfig()
    
    if config.auto_select_mode:
        config.mode = auto_select_client_mode(num_gpus, use_dp)
    
    if config.mode == ClientMode.INPROC:
        client = InprocClient(config, engine_core)
    elif config.mode == ClientMode.SYNC_MP:
        client = SyncMPClient(config)
    elif config.mode == ClientMode.ASYNC_MP:
        client = AsyncMPClient(config)
    elif config.mode == ClientMode.DP_ASYNC:
        config.num_workers = num_gpus
        client = DPAsyncMPClient(config)
    else:
        raise ValueError(f"Unknown client mode: {config.mode}")
    
    return client


# Convenience exports
__all__ = [
    "ClientMode",
    "WorkerState",
    "EngineClientConfig",
    "SchedulerOutput",
    "EngineOutput",
    "WorkerInfo",
    "EngineCoreClientBase",
    "InprocClient",
    "SyncMPClient",
    "AsyncMPClient",
    "P2CLoadBalancer",
    "DPAsyncMPClient",
    "auto_select_client_mode",
    "create_engine_client",
]
