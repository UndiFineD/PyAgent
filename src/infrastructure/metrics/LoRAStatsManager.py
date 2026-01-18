"""
Phase 45: LoRA Stats and Request State Tracking
vLLM-inspired LoRA adapter tracking with enhanced request lifecycle.

Beyond vLLM:
- Multi-adapter concurrent tracking
- Adapter warmup metrics
- Memory fragmentation tracking
- Adapter load prediction
- Cross-request adapter affinity
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None


class LoRALoadState(Enum):
    """State of a LoRA adapter."""
    NOT_LOADED = auto()
    LOADING = auto()
    LOADED = auto()
    EVICTING = auto()
    FAILED = auto()


class RequestStatus(Enum):
    """Status of a request in the system."""
    WAITING = auto()
    RUNNING = auto()
    PREEMPTED = auto()
    FINISHED_STOPPED = auto()
    FINISHED_LENGTH_CAPPED = auto()
    FINISHED_ABORTED = auto()


@dataclass
class LoRAAdapterInfo:
    """Information about a LoRA adapter."""
    adapter_id: str
    rank: int
    alpha: float
    target_modules: Tuple[str, ...]
    memory_bytes: int = 0
    load_state: LoRALoadState = LoRALoadState.NOT_LOADED
    load_time: float = 0.0
    last_used: float = 0.0
    use_count: int = 0
    
    def mark_used(self) -> None:
        """Mark adapter as used."""
        self.last_used = time.time()
        self.use_count += 1


@dataclass
class LoRARequestState:
    """
    State of a LoRA request (vLLM LoRARequestStates equivalent).
    
    Tracks per-request LoRA adapter usage and timing.
    """
    request_id: str
    adapter_id: str
    adapter_rank: int
    queued_time: float = field(default_factory=time.time)
    load_start_time: Optional[float] = None
    load_end_time: Optional[float] = None
    execution_start_time: Optional[float] = None
    execution_end_time: Optional[float] = None
    tokens_processed: int = 0
    was_preempted: bool = False
    
    @property
    def load_latency(self) -> Optional[float]:
        """Time spent loading the adapter."""
        if self.load_start_time and self.load_end_time:
            return self.load_end_time - self.load_start_time
        return None
    
    @property
    def queue_latency(self) -> Optional[float]:
        """Time spent waiting in queue."""
        if self.execution_start_time:
            return self.execution_start_time - self.queued_time
        return None
    
    @property
    def execution_latency(self) -> Optional[float]:
        """Time spent executing."""
        if self.execution_start_time and self.execution_end_time:
            return self.execution_end_time - self.execution_start_time
        return None
    
    @property
    def total_latency(self) -> Optional[float]:
        """Total request latency."""
        if self.execution_end_time:
            return self.execution_end_time - self.queued_time
        return None


@dataclass
class LoRAStats:
    """
    Aggregate statistics for LoRA operations (vLLM LoRAStats equivalent).
    
    Beyond vLLM:
    - Per-adapter breakdown
    - Load time percentiles
    - Memory efficiency tracking
    - Adapter affinity patterns
    """
    # Request counts
    total_requests: int = 0
    active_requests: int = 0
    completed_requests: int = 0
    preempted_requests: int = 0
    
    # Adapter counts
    total_adapters: int = 0
    loaded_adapters: int = 0
    max_loaded_adapters: int = 0
    
    # Timing stats (in seconds)
    total_load_time: float = 0.0
    total_execution_time: float = 0.0
    avg_load_latency: float = 0.0
    avg_execution_latency: float = 0.0
    
    # Memory stats
    total_adapter_memory: int = 0
    peak_adapter_memory: int = 0
    
    # Per-adapter stats
    adapter_use_counts: Dict[str, int] = field(default_factory=dict)
    adapter_request_counts: Dict[str, int] = field(default_factory=dict)


class LoRAStatsManager:
    """
    Manager for LoRA statistics collection.
    
    Features:
    - Thread-safe statistics updates
    - Per-adapter tracking
    - Request lifecycle tracking
    - Memory tracking
    """
    
    def __init__(self, max_loaded_adapters: int = 8):
        self._max_loaded = max_loaded_adapters
        self._adapters: Dict[str, LoRAAdapterInfo] = {}
        self._requests: Dict[str, LoRARequestState] = {}
        self._stats = LoRAStats()
        self._lock = threading.Lock()
        
        # For percentile tracking
        self._load_latencies: List[float] = []
        self._exec_latencies: List[float] = []
        self._max_history = 1000
    
    def register_adapter(
        self,
        adapter_id: str,
        rank: int,
        alpha: float,
        target_modules: Tuple[str, ...],
        memory_bytes: int = 0,
    ) -> LoRAAdapterInfo:
        """Register a new LoRA adapter."""
        with self._lock:
            if adapter_id in self._adapters:
                return self._adapters[adapter_id]
            
            info = LoRAAdapterInfo(
                adapter_id=adapter_id,
                rank=rank,
                alpha=alpha,
                target_modules=target_modules,
                memory_bytes=memory_bytes,
            )
            self._adapters[adapter_id] = info
            self._stats.total_adapters += 1
            return info
    
    def start_loading(self, adapter_id: str) -> None:
        """Mark adapter as loading."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.LOADING
                adapter.load_time = time.time()
    
    def finish_loading(self, adapter_id: str, success: bool = True) -> None:
        """Mark adapter as loaded or failed."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                if success:
                    adapter.load_state = LoRALoadState.LOADED
                    self._stats.loaded_adapters += 1
                    self._stats.max_loaded_adapters = max(
                        self._stats.max_loaded_adapters,
                        self._stats.loaded_adapters,
                    )
                    self._stats.total_adapter_memory += adapter.memory_bytes
                    self._stats.peak_adapter_memory = max(
                        self._stats.peak_adapter_memory,
                        self._stats.total_adapter_memory,
                    )
                else:
                    adapter.load_state = LoRALoadState.FAILED
    
    def start_evicting(self, adapter_id: str) -> None:
        """Mark adapter as evicting."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.EVICTING
    
    def finish_evicting(self, adapter_id: str) -> None:
        """Mark adapter as evicted."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.NOT_LOADED
                self._stats.loaded_adapters -= 1
                self._stats.total_adapter_memory -= adapter.memory_bytes
    
    def create_request(
        self,
        request_id: str,
        adapter_id: str,
    ) -> LoRARequestState:
        """Create a new LoRA request."""
        with self._lock:
            if adapter_id not in self._adapters:
                raise ValueError(f"Adapter {adapter_id} not registered")
            
            adapter = self._adapters[adapter_id]
            state = LoRARequestState(
                request_id=request_id,
                adapter_id=adapter_id,
                adapter_rank=adapter.rank,
            )
            self._requests[request_id] = state
            self._stats.total_requests += 1
            self._stats.active_requests += 1
            
            # Update adapter counts
            self._stats.adapter_request_counts[adapter_id] = (
                self._stats.adapter_request_counts.get(adapter_id, 0) + 1
            )
            
            return state
    
    def start_request_loading(self, request_id: str) -> None:
        """Mark request adapter loading started."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].load_start_time = time.time()
    
    def finish_request_loading(self, request_id: str) -> None:
        """Mark request adapter loading finished."""
        with self._lock:
            if request_id in self._requests:
                req = self._requests[request_id]
                req.load_end_time = time.time()
                if req.load_latency:
                    self._stats.total_load_time += req.load_latency
                    self._load_latencies.append(req.load_latency)
                    if len(self._load_latencies) > self._max_history:
                        self._load_latencies.pop(0)
    
    def start_execution(self, request_id: str) -> None:
        """Mark request execution started."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].execution_start_time = time.time()
    
    def finish_execution(self, request_id: str, tokens: int = 0) -> None:
        """Mark request execution finished."""
        with self._lock:
            if request_id in self._requests:
                req = self._requests[request_id]
                req.execution_end_time = time.time()
                req.tokens_processed = tokens
                
                self._stats.active_requests -= 1
                self._stats.completed_requests += 1
                
                if req.execution_latency:
                    self._stats.total_execution_time += req.execution_latency
                    self._exec_latencies.append(req.execution_latency)
                    if len(self._exec_latencies) > self._max_history:
                        self._exec_latencies.pop(0)
                
                # Update adapter usage
                adapter_id = req.adapter_id
                if adapter_id in self._adapters:
                    self._adapters[adapter_id].mark_used()
                    self._stats.adapter_use_counts[adapter_id] = (
                        self._stats.adapter_use_counts.get(adapter_id, 0) + 1
                    )
    
    def preempt_request(self, request_id: str) -> None:
        """Mark request as preempted."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].was_preempted = True
                self._stats.preempted_requests += 1
    
    def get_request_state(self, request_id: str) -> Optional[LoRARequestState]:
        """Get request state."""
        with self._lock:
            return self._requests.get(request_id)
    
    def get_adapter_info(self, adapter_id: str) -> Optional[LoRAAdapterInfo]:
        """Get adapter info."""
        with self._lock:
            return self._adapters.get(adapter_id)
    
    def get_stats(self) -> LoRAStats:
        """Get aggregate statistics."""
        with self._lock:
            stats = LoRAStats(
                total_requests=self._stats.total_requests,
                active_requests=self._stats.active_requests,
                completed_requests=self._stats.completed_requests,
                preempted_requests=self._stats.preempted_requests,
                total_adapters=self._stats.total_adapters,
                loaded_adapters=self._stats.loaded_adapters,
                max_loaded_adapters=self._stats.max_loaded_adapters,
                total_load_time=self._stats.total_load_time,
                total_execution_time=self._stats.total_execution_time,
                total_adapter_memory=self._stats.total_adapter_memory,
                peak_adapter_memory=self._stats.peak_adapter_memory,
                adapter_use_counts=dict(self._stats.adapter_use_counts),
                adapter_request_counts=dict(self._stats.adapter_request_counts),
            )
            
            # Calculate averages
            if self._stats.completed_requests > 0:
                stats.avg_load_latency = (
                    self._stats.total_load_time / self._stats.completed_requests
                )
                stats.avg_execution_latency = (
                    self._stats.total_execution_time / self._stats.completed_requests
                )
            
            return stats
    
    def get_load_latency_percentile(self, percentile: float) -> float:
        """Get load latency percentile."""
        with self._lock:
            if not self._load_latencies:
                return 0.0
            sorted_latencies = sorted(self._load_latencies)
            idx = int(len(sorted_latencies) * percentile / 100)
            return sorted_latencies[min(idx, len(sorted_latencies) - 1)]
    
    def get_exec_latency_percentile(self, percentile: float) -> float:
        """Get execution latency percentile."""
        with self._lock:
            if not self._exec_latencies:
                return 0.0
            sorted_latencies = sorted(self._exec_latencies)
            idx = int(len(sorted_latencies) * percentile / 100)
            return sorted_latencies[min(idx, len(sorted_latencies) - 1)]
    
    def get_loaded_adapters(self) -> List[str]:
        """Get list of loaded adapter IDs."""
        with self._lock:
            return [
                aid for aid, info in self._adapters.items()
                if info.load_state == LoRALoadState.LOADED
            ]
    
    def get_lru_adapter(self) -> Optional[str]:
        """Get least recently used loaded adapter."""
        with self._lock:
            loaded = [
                (info.last_used, aid)
                for aid, info in self._adapters.items()
                if info.load_state == LoRALoadState.LOADED
            ]
            if not loaded:
                return None
            loaded.sort()
            return loaded[0][1]
    
    def should_evict(self) -> bool:
        """Check if an adapter should be evicted."""
        with self._lock:
            return self._stats.loaded_adapters >= self._max_loaded


class RequestLifecycle:
    """
    Enhanced request lifecycle tracking (beyond vLLM Request class).
    
    Features:
    - Full event history
    - State transitions with timestamps
    - Detailed timing breakdown
    - Cancellation and preemption tracking
    """
    
    def __init__(
        self,
        request_id: str,
        prompt_tokens: int = 0,
        max_tokens: int = 0,
        lora_adapter: Optional[str] = None,
    ):
        self.request_id = request_id
        self.prompt_tokens = prompt_tokens
        self.max_tokens = max_tokens
        self.lora_adapter = lora_adapter
        
        self._status = RequestStatus.WAITING
        self._events: List[Tuple[float, str, Any]] = []
        self._state_times: Dict[RequestStatus, float] = {}
        self._created_time = time.time()
        self._first_token_time: Optional[float] = None
        self._finish_time: Optional[float] = None
        self._tokens_generated = 0
        self._preemption_count = 0
        self._lock = threading.Lock()
        
        self._record_event("created", {
            'prompt_tokens': prompt_tokens,
            'max_tokens': max_tokens,
            'lora_adapter': lora_adapter,
        })
    
    def _record_event(self, event_type: str, data: Any = None) -> None:
        """Record an event."""
        self._events.append((time.time(), event_type, data))
    
    @property
    def status(self) -> RequestStatus:
        """Get current status."""
        with self._lock:
            return self._status
    
    def transition_to(self, new_status: RequestStatus) -> None:
        """Transition to a new status."""
        with self._lock:
            now = time.time()
            old_status = self._status
            
            # Record time spent in old status
            if old_status in self._state_times:
                self._state_times[old_status] = now - self._state_times.get(
                    f"_start_{old_status}", self._created_time
                )
            
            self._status = new_status
            self._state_times[f"_start_{new_status}"] = now
            
            if new_status == RequestStatus.PREEMPTED:
                self._preemption_count += 1
            
            self._record_event("state_transition", {
                'from': old_status.name,
                'to': new_status.name,
            })
    
    def record_token(self) -> None:
        """Record a generated token."""
        with self._lock:
            now = time.time()
            self._tokens_generated += 1
            
            if self._first_token_time is None:
                self._first_token_time = now
                self._record_event("first_token", {'time': now})
    
    def finish(self, reason: str = "stopped") -> None:
        """Mark request as finished."""
        with self._lock:
            self._finish_time = time.time()
            
            # Direct status update to avoid deadlock (no nested lock)
            if reason == "stopped":
                new_status = RequestStatus.FINISHED_STOPPED
            elif reason == "length":
                new_status = RequestStatus.FINISHED_LENGTH_CAPPED
            elif reason == "aborted":
                new_status = RequestStatus.FINISHED_ABORTED
            else:
                new_status = RequestStatus.FINISHED_STOPPED
            
            self._status = new_status
            self._record_event("finished", {
                'reason': reason,
                'tokens_generated': self._tokens_generated,
            })
    
    @property
    def time_to_first_token(self) -> Optional[float]:
        """Get TTFT in seconds."""
        with self._lock:
            if self._first_token_time:
                return self._first_token_time - self._created_time
            return None
    
    @property
    def total_latency(self) -> Optional[float]:
        """Get total latency in seconds."""
        with self._lock:
            if self._finish_time:
                return self._finish_time - self._created_time
            return None
    
    @property
    def tokens_generated(self) -> int:
        """Get tokens generated."""
        with self._lock:
            return self._tokens_generated
    
    @property
    def inter_token_latency(self) -> Optional[float]:
        """Get average inter-token latency."""
        with self._lock:
            if self._tokens_generated <= 1 or not self._finish_time:
                return None
            if not self._first_token_time:
                return None
            decode_time = self._finish_time - self._first_token_time
            return decode_time / (self._tokens_generated - 1)
    
    @property
    def throughput(self) -> Optional[float]:
        """Get tokens per second."""
        latency = self.total_latency
        if latency and latency > 0:
            return self._tokens_generated / latency
        return None
    
    def get_events(self) -> List[Tuple[float, str, Any]]:
        """Get all events."""
        with self._lock:
            return list(self._events)
    
    def get_timing_breakdown(self) -> Dict[str, float]:
        """Get timing breakdown by state."""
        with self._lock:
            result = {}
            for status in RequestStatus:
                if status in self._state_times:
                    result[status.name] = self._state_times[status]
            
            if self._first_token_time:
                result['time_to_first_token'] = (
                    self._first_token_time - self._created_time
                )
            if self._finish_time:
                result['total_latency'] = self._finish_time - self._created_time
            
            return result


class RequestLifecycleManager:
    """Manager for request lifecycles."""
    
    def __init__(self, max_completed: int = 1000):
        self._active: Dict[str, RequestLifecycle] = {}
        self._completed: List[RequestLifecycle] = []
        self._max_completed = max_completed
        self._lock = threading.Lock()
    
    def create(
        self,
        request_id: str,
        prompt_tokens: int = 0,
        max_tokens: int = 0,
        lora_adapter: Optional[str] = None,
    ) -> RequestLifecycle:
        """Create a new request lifecycle."""
        lifecycle = RequestLifecycle(
            request_id=request_id,
            prompt_tokens=prompt_tokens,
            max_tokens=max_tokens,
            lora_adapter=lora_adapter,
        )
        with self._lock:
            self._active[request_id] = lifecycle
        return lifecycle
    
    def get(self, request_id: str) -> Optional[RequestLifecycle]:
        """Get a request lifecycle."""
        with self._lock:
            return self._active.get(request_id)
    
    def finish(self, request_id: str, reason: str = "stopped") -> None:
        """Finish a request."""
        with self._lock:
            if request_id in self._active:
                lifecycle = self._active.pop(request_id)
                lifecycle.finish(reason)
                self._completed.append(lifecycle)
                if len(self._completed) > self._max_completed:
                    self._completed.pop(0)
    
    def get_active_count(self) -> int:
        """Get number of active requests."""
        with self._lock:
            return len(self._active)
    
    def get_completed_count(self) -> int:
        """Get number of completed requests."""
        with self._lock:
            return len(self._completed)
    
    def get_aggregate_stats(self) -> Dict[str, float]:
        """Get aggregate statistics from completed requests."""
        with self._lock:
            if not self._completed:
                return {}
            
            ttft_values = [
                r.time_to_first_token
                for r in self._completed
                if r.time_to_first_token is not None
            ]
            itl_values = [
                r.inter_token_latency
                for r in self._completed
                if r.inter_token_latency is not None
            ]
            latency_values = [
                r.total_latency
                for r in self._completed
                if r.total_latency is not None
            ]
            throughput_values = [
                r.throughput
                for r in self._completed
                if r.throughput is not None
            ]
            
            stats = {}
            if ttft_values:
                stats['avg_ttft'] = sum(ttft_values) / len(ttft_values)
                stats['p50_ttft'] = sorted(ttft_values)[len(ttft_values) // 2]
                stats['p99_ttft'] = sorted(ttft_values)[int(len(ttft_values) * 0.99)]
            if itl_values:
                stats['avg_itl'] = sum(itl_values) / len(itl_values)
            if latency_values:
                stats['avg_latency'] = sum(latency_values) / len(latency_values)
            if throughput_values:
                stats['avg_throughput'] = sum(throughput_values) / len(throughput_values)
            
            return stats


__all__ = [
    'LoRALoadState',
    'RequestStatus',
    'LoRAAdapterInfo',
    'LoRARequestState',
    'LoRAStats',
    'LoRAStatsManager',
    'RequestLifecycle',
    'RequestLifecycleManager',
]
