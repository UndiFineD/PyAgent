"""
DataParallelCoordinator: DP coordination with step/wave synchronization.

vLLM Pattern: DPEngineCoreProc from v1/engine/dp_engine_core_proc.py
- step_counter / step_request_count for sync tracking
- wave_id for execution wave management
- DPLBAsyncMPClient for load-balanced request distribution
- P2C (Power of Two Choices) worker selection

Beyond vLLM:
- Hierarchical DP with locality awareness
- Adaptive load balancing based on worker latency
- Fault tolerance with worker recovery
"""

from __future__ import annotations
import asyncio
import logging
import threading
import time
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar, Dict, List
from collections import deque

logger = logging.getLogger(__name__)

T = TypeVar("T")


class DPRole(Enum):
    """Data parallel role."""
    MASTER = auto()    # Coordinates workers
    WORKER = auto()    # Executes work
    HYBRID = auto()    # Both roles


class WorkerHealth(Enum):
    """Worker health status."""
    HEALTHY = auto()
    DEGRADED = auto()
    RECOVERING = auto()
    FAILED = auto()


class LoadBalanceStrategy(Enum):
    """Load balancing strategy."""
    ROUND_ROBIN = auto()
    LEAST_LOADED = auto()
    P2C = auto()               # Power of Two Choices
    LOCALITY_AWARE = auto()    # Prefer local workers


@dataclass
class DPConfig:
    """Configuration for data parallel coordinator."""
    num_workers: int = 1
    dp_rank: int = 0
    dp_size: int = 1
    role: DPRole = DPRole.WORKER
    lb_strategy: LoadBalanceStrategy = LoadBalanceStrategy.P2C
    p2c_sample_size: int = 2
    health_check_interval_s: float = 5.0
    max_consecutive_failures: int = 3
    enable_locality: bool = True
    locality_groups: list[list[int]] = field(default_factory=list)  # Groups of local workers


@dataclass
class WorkerState:
    """State of a DP worker."""
    worker_id: int
    dp_rank: int
    health: WorkerHealth = WorkerHealth.HEALTHY
    pending_requests: int = 0
    total_processed: int = 0
    avg_latency_ms: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    consecutive_failures: int = 0
    locality_group: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def update_latency(self, latency_ms: float) -> None:
        """Update average latency with EMA."""
        self.avg_latency_ms = 0.9 * self.avg_latency_ms + 0.1 * latency_ms


@dataclass
class StepState:
    """State for a single step."""
    step_id: int
    wave_id: int
    request_count: int = 0
    completed_count: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    @property
    def is_complete(self) -> bool:
        return self.completed_count >= self.request_count
    
    @property
    def duration_ms(self) -> float:
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000


@dataclass
class WaveState:
    """State for an execution wave."""
    wave_id: int
    num_steps: int = 0
    completed_steps: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    @property
    def is_complete(self) -> bool:
        return self.completed_steps >= self.num_steps


class P2CLoadBalancer:
    """
    Power of Two Choices load balancer.
    
    vLLM Pattern: DPLBAsyncMPClient worker selection
    
    Algorithm:
    1. Randomly sample 2 workers
    2. Select the one with fewer pending requests
    3. Tie-break by latency
    """
    
    def __init__(
        self,
        workers: list[WorkerState],
        sample_size: int = 2,
        enable_locality: bool = True
    ):
        self._workers = workers
        self._sample_size = min(sample_size, len(workers))
        self._enable_locality = enable_locality
        self._lock = threading.Lock()
    
    def select_worker(self, locality_group: Optional[int] = None) -> WorkerState:
        """Select best worker using P2C algorithm."""
        with self._lock:
            # Filter healthy workers
            healthy = [
                w for w in self._workers
                if w.health in (WorkerHealth.HEALTHY, WorkerHealth.DEGRADED)
            ]
            
            if not healthy:
                # Fallback to any worker
                healthy = self._workers
            
            # Apply locality preference
            if self._enable_locality and locality_group is not None:
                local_workers = [w for w in healthy if w.locality_group == locality_group]
                if local_workers:
                    healthy = local_workers
            
            if len(healthy) == 1:
                return healthy[0]
            
            # Sample workers
            candidates = random.sample(healthy, min(self._sample_size, len(healthy)))
            
            # Select by pending requests, then latency
            best = min(candidates, key=lambda w: (w.pending_requests, w.avg_latency_ms))
            
            return best
    
    def update_workers(self, workers: list[WorkerState]) -> None:
        """Update worker list."""
        with self._lock:
            self._workers = workers


class DPEngineCoreProc:
    """
    Data Parallel engine core processor.
    
    vLLM Pattern: DPEngineCoreProc from dp_engine_core_proc.py
    
    Manages step/wave synchronization across DP workers.
    """
    
    def __init__(self, config: DPConfig):
        self.config = config
        
        # Step tracking
        self._step_counter = 0
        self._step_request_count = 0
        self._current_step: Optional[StepState] = None
        
        # Wave tracking
        self._wave_id = 0
        self._current_wave: Optional[WaveState] = None
        self._wave_history: deque[WaveState] = deque(maxlen=100)
        
        # Workers
        self._workers: dict[int, WorkerState] = {}
        self._init_workers()
        
        # Load balancer
        self._load_balancer = P2CLoadBalancer(
            list(self._workers.values()),
            self.config.p2c_sample_size,
            self.config.enable_locality
        )
        
        # Barriers for synchronization
        self._step_barrier: Optional[threading.Barrier] = None
        self._wave_barrier: Optional[threading.Barrier] = None
        
        if self.config.dp_size > 1:
            self._step_barrier = threading.Barrier(self.config.dp_size)
            self._wave_barrier = threading.Barrier(self.config.dp_size)
        
        self._lock = threading.RLock()
        
        logger.info(f"DPEngineCoreProc initialized: rank={config.dp_rank}, size={config.dp_size}")
    
    def _init_workers(self) -> None:
        """Initialize worker states."""
        for i in range(self.config.num_workers):
            # Assign locality groups
            locality_group = 0
            for group_idx, group in enumerate(self.config.locality_groups):
                if i in group:
                    locality_group = group_idx
                    break
            
            self._workers[i] = WorkerState(
                worker_id=i,
                dp_rank=i % self.config.dp_size,
                locality_group=locality_group
            )
    
    def begin_step(self, num_requests: int = 0) -> StepState:
        """
        Begin a new step.
        
        vLLM Pattern: step_counter tracking
        """
        with self._lock:
            self._step_counter += 1
            self._step_request_count = num_requests
            
            step = StepState(
                step_id=self._step_counter,
                wave_id=self._wave_id,
                request_count=num_requests
            )
            self._current_step = step
            
            logger.debug(f"Begin step {step.step_id} (wave {step.wave_id}, {num_requests} requests)")
            
            return step
    
    def end_step(self) -> Optional[StepState]:
        """End current step."""
        with self._lock:
            if self._current_step is None:
                return None
            
            step = self._current_step
            step.end_time = time.time()
            
            # Update wave
            if self._current_wave:
                self._current_wave.completed_steps += 1
            
            self._current_step = None
            
            logger.debug(f"End step {step.step_id} ({step.duration_ms:.2f}ms)")
            
            return step
    
    def step_sync(self) -> None:
        """Synchronize all DP ranks at step boundary."""
        if self._step_barrier:
            self._step_barrier.wait()
    
    def begin_wave(self, num_steps: int = 0) -> WaveState:
        """
        Begin a new execution wave.
        
        vLLM Pattern: wave_id tracking
        """
        with self._lock:
            self._wave_id += 1
            
            wave = WaveState(
                wave_id=self._wave_id,
                num_steps=num_steps
            )
            self._current_wave = wave
            
            logger.debug(f"Begin wave {wave.wave_id} ({num_steps} steps)")
            
            return wave
    
    def wave_complete(self) -> bool:
        """
        Check if current wave is complete.
        
        vLLM Pattern: wave completion check
        """
        with self._lock:
            if self._current_wave is None:
                return True
            return self._current_wave.is_complete
    
    def end_wave(self) -> Optional[WaveState]:
        """End current wave."""
        with self._lock:
            if self._current_wave is None:
                return None
            
            wave = self._current_wave
            wave.end_time = time.time()
            
            self._wave_history.append(wave)
            self._current_wave = None
            
            logger.debug(f"End wave {wave.wave_id}")
            
            return wave
    
    def wave_sync(self) -> None:
        """Synchronize all DP ranks at wave boundary."""
        if self._wave_barrier:
            self._wave_barrier.wait()
    
    def select_worker(self, locality_group: Optional[int] = None) -> WorkerState:
        """
        Select worker for request assignment.
        
        vLLM Pattern: P2C worker selection
        """
        return self._load_balancer.select_worker(locality_group)
    
    def assign_request(self, request_id: str) -> int:
        """Assign request to a worker. Returns worker ID."""
        worker = self.select_worker()
        worker.pending_requests += 1
        return worker.worker_id
    
    def complete_request(
        self,
        worker_id: int,
        latency_ms: float,
        success: bool = True
    ) -> None:
        """Mark request as complete on worker."""
        with self._lock:
            if worker_id not in self._workers:
                return
            
            worker = self._workers[worker_id]
            worker.pending_requests = max(0, worker.pending_requests - 1)
            worker.total_processed += 1
            worker.update_latency(latency_ms)
            
            if success:
                worker.consecutive_failures = 0
                if worker.health == WorkerHealth.RECOVERING:
                    worker.health = WorkerHealth.HEALTHY
            else:
                worker.consecutive_failures += 1
                if worker.consecutive_failures >= self.config.max_consecutive_failures:
                    worker.health = WorkerHealth.FAILED
                    logger.warning(f"Worker {worker_id} marked as FAILED")
            
            # Update current step
            if self._current_step:
                self._current_step.completed_count += 1
    
    def update_worker_health(self, worker_id: int, health: WorkerHealth) -> None:
        """Update worker health status."""
        with self._lock:
            if worker_id in self._workers:
                self._workers[worker_id].health = health
                self._workers[worker_id].last_heartbeat = time.time()
    
    def get_step_counter(self) -> int:
        """Get current step counter."""
        return self._step_counter
    
    def get_wave_id(self) -> int:
        """Get current wave ID."""
        return self._wave_id
    
    def get_worker_states(self) -> list[WorkerState]:
        """Get all worker states."""
        with self._lock:
            return list(self._workers.values())
    
    def get_healthy_workers(self) -> list[WorkerState]:
        """Get only healthy workers."""
        with self._lock:
            return [
                w for w in self._workers.values()
                if w.health in (WorkerHealth.HEALTHY, WorkerHealth.DEGRADED)
            ]
    
    def get_metrics(self) -> dict[str, Any]:
        """Get coordinator metrics."""
        with self._lock:
            total_pending = sum(w.pending_requests for w in self._workers.values())
            total_processed = sum(w.total_processed for w in self._workers.values())
            healthy_count = len(self.get_healthy_workers())
            
            return {
                "dp_rank": self.config.dp_rank,
                "dp_size": self.config.dp_size,
                "step_counter": self._step_counter,
                "wave_id": self._wave_id,
                "num_workers": len(self._workers),
                "healthy_workers": healthy_count,
                "total_pending": total_pending,
                "total_processed": total_processed,
                "waves_completed": len(self._wave_history),
            }


class HierarchicalDPCoordinator:
    """
    Hierarchical DP coordinator with locality awareness.
    
    Beyond vLLM: Two-level hierarchy for large-scale DP.
    
    Level 1: Local coordinators (within a node)
    Level 2: Global coordinator (across nodes)
    """
    
    def __init__(
        self,
        num_local_coordinators: int,
        workers_per_coordinator: int,
        locality_groups: Optional[list[list[int]]] = None
    ):
        self._num_local = num_local_coordinators
        self._workers_per = workers_per_coordinator
        
        # Create local coordinators
        self._local_coordinators: list[DPEngineCoreProc] = []
        
        for i in range(num_local_coordinators):
            config = DPConfig(
                num_workers=workers_per_coordinator,
                dp_rank=i,
                dp_size=num_local_coordinators,
                role=DPRole.HYBRID,
                enable_locality=True,
                locality_groups=locality_groups or []
            )
            self._local_coordinators.append(DPEngineCoreProc(config))
        
        # Global state
        self._global_step = 0
        self._global_wave = 0
        
        # Request routing
        self._next_coordinator = 0
        
        self._lock = threading.Lock()
        
        logger.info(
            f"HierarchicalDPCoordinator: {num_local_coordinators} coordinators, "
            f"{workers_per_coordinator} workers each"
        )
    
    def route_request(self, request_id: str, hint_locality: Optional[int] = None) -> tuple[int, int]:
        """
        Route request to coordinator and worker.
        
        Returns (coordinator_idx, worker_id).
        """
        with self._lock:
            if hint_locality is not None and 0 <= hint_locality < self._num_local:
                coord_idx = hint_locality
            else:
                # Round-robin across coordinators
                coord_idx = self._next_coordinator
                self._next_coordinator = (self._next_coordinator + 1) % self._num_local
            
            coordinator = self._local_coordinators[coord_idx]
            worker_id = coordinator.assign_request(request_id)
            
            return (coord_idx, worker_id)
    
    def complete_request(
        self,
        coordinator_idx: int,
        worker_id: int,
        latency_ms: float,
        success: bool = True
    ) -> None:
        """Mark request complete."""
        if 0 <= coordinator_idx < self._num_local:
            self._local_coordinators[coordinator_idx].complete_request(
                worker_id, latency_ms, success
            )
    
    def global_step_sync(self) -> int:
        """Synchronize all coordinators at step boundary."""
        with self._lock:
            self._global_step += 1
            
            for coord in self._local_coordinators:
                coord.step_sync()
            
            return self._global_step
    
    def global_wave_sync(self) -> int:
        """Synchronize all coordinators at wave boundary."""
        with self._lock:
            self._global_wave += 1
            
            for coord in self._local_coordinators:
                coord.wave_sync()
            
            return self._global_wave
    
    def get_global_metrics(self) -> dict[str, Any]:
        """Get aggregated metrics."""
        with self._lock:
            total_pending = 0
            total_processed = 0
            total_healthy = 0
            total_workers = 0
            
            for coord in self._local_coordinators:
                metrics = coord.get_metrics()
                total_pending += metrics["total_pending"]
                total_processed += metrics["total_processed"]
                total_healthy += metrics["healthy_workers"]
                total_workers += metrics["num_workers"]
            
            return {
                "num_coordinators": self._num_local,
                "total_workers": total_workers,
                "healthy_workers": total_healthy,
                "global_step": self._global_step,
                "global_wave": self._global_wave,
                "total_pending": total_pending,
                "total_processed": total_processed,
            }


async def dp_collective_all_reduce(
    values: list[float],
    coordinator: DPEngineCoreProc,
    operation: str = "sum"
) -> list[float]:
    """
    Async all-reduce across DP ranks.
    
    Beyond vLLM: Async collective operations.
    """
    # In a real implementation, this would use NCCL or similar
    # For now, simulate by returning the input (single rank)
    await asyncio.sleep(0.001)  # Simulate communication
    
    if operation == "sum":
        return values
    elif operation == "mean":
        return [v / coordinator.config.dp_size for v in values]
    elif operation == "max":
        return values
    elif operation == "min":
        return values
    else:
        return values


# Convenience exports
__all__ = [
    "DPRole",
    "WorkerHealth",
    "LoadBalanceStrategy",
    "DPConfig",
    "WorkerState",
    "StepState",
    "WaveState",
    "P2CLoadBalancer",
    "DPEngineCoreProc",
    "HierarchicalDPCoordinator",
    "dp_collective_all_reduce",
]
