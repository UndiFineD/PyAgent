"""
Scheduler Statistics.

Comprehensive metrics for LLM inference scheduling:
- Request queue and running state tracking
- Prefix cache hit/miss statistics
- Speculative decoding acceptance rates
- Performance timing breakdown

Inspired by vLLM's v1/metrics/stats.py architecture.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MetricExportFormat(str, Enum):
    """Format for metric export."""
    DICT = "dict"
    PROMETHEUS = "prometheus"
    JSON = "json"


@dataclass
class PrefixCacheStats:
    """Statistics for prefix cache performance."""
    
    num_tokens: int = 0
    num_hits: int = 0
    num_misses: int = 0
    preempted: bool = False
    
    def record(
        self,
        num_tokens: int,
        num_hits: int,
        preempted: bool = False,
    ) -> None:
        """Record cache access."""
        self.num_tokens += num_tokens
        self.num_hits += num_hits
        self.num_misses += num_tokens - num_hits
        if preempted:
            self.preempted = True
    
    @property
    def hit_rate(self) -> float:
        total = self.num_hits + self.num_misses
        if total == 0:
            return 0.0
        return self.num_hits / total
    
    def reset(self) -> None:
        self.num_tokens = 0
        self.num_hits = 0
        self.num_misses = 0
        self.preempted = False
    
    def clone(self) -> PrefixCacheStats:
        return PrefixCacheStats(
            num_tokens=self.num_tokens,
            num_hits=self.num_hits,
            num_misses=self.num_misses,
            preempted=self.preempted,
        )
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "num_tokens": self.num_tokens,
            "num_hits": self.num_hits,
            "num_misses": self.num_misses,
            "hit_rate": self.hit_rate,
            "preempted": self.preempted,
        }


@dataclass
class SpecDecodingStats:
    """Statistics for speculative decoding."""
    
    num_spec_tokens: int = 5  # Max speculative tokens
    num_drafts: int = 0
    num_draft_tokens: int = 0
    num_accepted_tokens: int = 0
    num_accepted_tokens_per_pos: list[int] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.num_accepted_tokens_per_pos:
            self.num_accepted_tokens_per_pos = [0] * self.num_spec_tokens
    
    @classmethod
    def new(cls, num_spec_tokens: int) -> SpecDecodingStats:
        return cls(
            num_spec_tokens=num_spec_tokens,
            num_accepted_tokens_per_pos=[0] * num_spec_tokens,
        )
    
    def observe_draft(
        self,
        num_draft_tokens: int,
        num_accepted_tokens: int,
        accepted_positions: list[int] | None = None,
    ) -> None:
        """Record a draft verification result."""
        self.num_drafts += 1
        self.num_draft_tokens += num_draft_tokens
        self.num_accepted_tokens += num_accepted_tokens
        
        if accepted_positions:
            for pos in accepted_positions:
                if 0 <= pos < len(self.num_accepted_tokens_per_pos):
                    self.num_accepted_tokens_per_pos[pos] += 1
    
    @property
    def acceptance_rate(self) -> float:
        if not self.num_draft_tokens:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens
    
    @property
    def avg_accepted_per_draft(self) -> float:
        if not self.num_drafts:
            return 0.0
        return self.num_accepted_tokens / self.num_drafts
    
    @property
    def position_acceptance_rates(self) -> list[float]:
        if not self.num_drafts:
            return [0.0] * len(self.num_accepted_tokens_per_pos)
        return [count / self.num_drafts for count in self.num_accepted_tokens_per_pos]
    
    def reset(self) -> None:
        self.num_drafts = 0
        self.num_draft_tokens = 0
        self.num_accepted_tokens = 0
        self.num_accepted_tokens_per_pos = [0] * self.num_spec_tokens
    
    def clone(self) -> SpecDecodingStats:
        return SpecDecodingStats(
            num_spec_tokens=self.num_spec_tokens,
            num_drafts=self.num_drafts,
            num_draft_tokens=self.num_draft_tokens,
            num_accepted_tokens=self.num_accepted_tokens,
            num_accepted_tokens_per_pos=list(self.num_accepted_tokens_per_pos),
        )
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "num_drafts": self.num_drafts,
            "num_draft_tokens": self.num_draft_tokens,
            "num_accepted_tokens": self.num_accepted_tokens,
            "acceptance_rate": self.acceptance_rate,
            "avg_accepted_per_draft": self.avg_accepted_per_draft,
            "position_acceptance_rates": self.position_acceptance_rates,
        }


@dataclass
class CUDAGraphStats:
    """Statistics for CUDA graph capture and replay."""
    
    num_captures: int = 0
    num_replays: int = 0
    capture_time_ms: float = 0.0
    replay_time_ms: float = 0.0
    graph_memory_mb: float = 0.0
    
    def record_capture(self, time_ms: float, memory_mb: float) -> None:
        self.num_captures += 1
        self.capture_time_ms += time_ms
        self.graph_memory_mb = max(self.graph_memory_mb, memory_mb)
    
    def record_replay(self, time_ms: float) -> None:
        self.num_replays += 1
        self.replay_time_ms += time_ms
    
    @property
    def avg_capture_time_ms(self) -> float:
        if not self.num_captures:
            return 0.0
        return self.capture_time_ms / self.num_captures
    
    @property
    def avg_replay_time_ms(self) -> float:
        if not self.num_replays:
            return 0.0
        return self.replay_time_ms / self.num_replays
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "num_captures": self.num_captures,
            "num_replays": self.num_replays,
            "capture_time_ms": self.capture_time_ms,
            "replay_time_ms": self.replay_time_ms,
            "avg_capture_time_ms": self.avg_capture_time_ms,
            "avg_replay_time_ms": self.avg_replay_time_ms,
            "graph_memory_mb": self.graph_memory_mb,
        }


@dataclass
class PerfStats:
    """Performance timing breakdown."""
    
    # Scheduler timing
    schedule_time_ms: float = 0.0
    
    # Model timing
    model_forward_time_ms: float = 0.0
    model_execute_time_ms: float = 0.0
    
    # Sampling timing
    sample_time_ms: float = 0.0
    
    # Communication timing
    all_reduce_time_ms: float = 0.0
    
    # Memory timing
    cache_swap_time_ms: float = 0.0
    
    # Step counter
    num_steps: int = 0
    
    def record_step(
        self,
        schedule_ms: float = 0.0,
        forward_ms: float = 0.0,
        sample_ms: float = 0.0,
    ) -> None:
        """Record timing for one step."""
        self.num_steps += 1
        self.schedule_time_ms += schedule_ms
        self.model_forward_time_ms += forward_ms
        self.sample_time_ms += sample_ms
    
    @property
    def total_time_ms(self) -> float:
        return (
            self.schedule_time_ms +
            self.model_forward_time_ms +
            self.sample_time_ms +
            self.all_reduce_time_ms +
            self.cache_swap_time_ms
        )
    
    @property
    def avg_step_time_ms(self) -> float:
        if not self.num_steps:
            return 0.0
        return self.total_time_ms / self.num_steps
    
    def reset(self) -> None:
        self.schedule_time_ms = 0.0
        self.model_forward_time_ms = 0.0
        self.model_execute_time_ms = 0.0
        self.sample_time_ms = 0.0
        self.all_reduce_time_ms = 0.0
        self.cache_swap_time_ms = 0.0
        self.num_steps = 0
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "num_steps": self.num_steps,
            "schedule_time_ms": self.schedule_time_ms,
            "model_forward_time_ms": self.model_forward_time_ms,
            "sample_time_ms": self.sample_time_ms,
            "total_time_ms": self.total_time_ms,
            "avg_step_time_ms": self.avg_step_time_ms,
        }


@dataclass
class KVCacheEvictionEvent:
    """Event tracking KV cache eviction."""
    
    timestamp: float
    request_id: str
    num_blocks: int
    reason: str  # "memory_pressure", "timeout", "manual"
    
    @classmethod
    def now(cls, request_id: str, num_blocks: int, reason: str) -> KVCacheEvictionEvent:
        return cls(
            timestamp=time.time(),
            request_id=request_id,
            num_blocks=num_blocks,
            reason=reason,
        )
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "num_blocks": self.num_blocks,
            "reason": self.reason,
        }


@dataclass
class SchedulerStats:
    """Comprehensive scheduler statistics."""
    
    # Queue state
    num_running_reqs: int = 0
    num_waiting_reqs: int = 0
    
    # Step tracking
    step_counter: int = 0
    current_wave: int = 0
    
    # KV cache usage
    kv_cache_usage: float = 0.0
    
    # Prefix cache
    prefix_cache_stats: PrefixCacheStats = field(default_factory=PrefixCacheStats)
    connector_prefix_cache_stats: PrefixCacheStats | None = None
    
    # Eviction events
    kv_cache_eviction_events: list[KVCacheEvictionEvent] = field(default_factory=list)
    
    # Speculative decoding
    spec_decoding_stats: SpecDecodingStats | None = None
    
    # KV connector (for disaggregated inference)
    kv_connector_stats: dict[str, Any] | None = None
    
    # LoRA adapters
    waiting_lora_adapters: dict[str, int] = field(default_factory=dict)
    running_lora_adapters: dict[str, int] = field(default_factory=dict)
    
    # CUDA graphs
    cudagraph_stats: CUDAGraphStats | None = None
    
    # Performance
    perf_stats: PerfStats | None = None
    
    def record_step(
        self,
        num_running: int,
        num_waiting: int,
        kv_usage: float,
    ) -> None:
        """Record scheduler step."""
        self.step_counter += 1
        self.num_running_reqs = num_running
        self.num_waiting_reqs = num_waiting
        self.kv_cache_usage = kv_usage
    
    def record_eviction(self, event: KVCacheEvictionEvent) -> None:
        """Record eviction event."""
        self.kv_cache_eviction_events.append(event)
    
    @property
    def total_requests(self) -> int:
        return self.num_running_reqs + self.num_waiting_reqs
    
    def reset(self) -> None:
        """Reset all stats."""
        self.num_running_reqs = 0
        self.num_waiting_reqs = 0
        self.step_counter = 0
        self.kv_cache_usage = 0.0
        self.prefix_cache_stats.reset()
        self.kv_cache_eviction_events.clear()
        if self.spec_decoding_stats:
            self.spec_decoding_stats.reset()
        if self.perf_stats:
            self.perf_stats.reset()
    
    def clone(self) -> SchedulerStats:
        """Create a snapshot of current stats."""
        return SchedulerStats(
            num_running_reqs=self.num_running_reqs,
            num_waiting_reqs=self.num_waiting_reqs,
            step_counter=self.step_counter,
            current_wave=self.current_wave,
            kv_cache_usage=self.kv_cache_usage,
            prefix_cache_stats=self.prefix_cache_stats.clone(),
            spec_decoding_stats=self.spec_decoding_stats.clone() if self.spec_decoding_stats else None,
            cudagraph_stats=self.cudagraph_stats,
            perf_stats=self.perf_stats,
        )
    
    def as_dict(self) -> dict[str, Any]:
        result = {
            "num_running_reqs": self.num_running_reqs,
            "num_waiting_reqs": self.num_waiting_reqs,
            "total_requests": self.total_requests,
            "step_counter": self.step_counter,
            "current_wave": self.current_wave,
            "kv_cache_usage": self.kv_cache_usage,
            "prefix_cache": self.prefix_cache_stats.as_dict(),
        }
        
        if self.spec_decoding_stats:
            result["spec_decoding"] = self.spec_decoding_stats.as_dict()
        
        if self.cudagraph_stats:
            result["cudagraph"] = self.cudagraph_stats.as_dict()
        
        if self.perf_stats:
            result["performance"] = self.perf_stats.as_dict()
        
        return result
    
    def to_prometheus(self) -> str:
        """Export as Prometheus format."""
        lines = [
            f'scheduler_running_requests {{}} {self.num_running_reqs}',
            f'scheduler_waiting_requests {{}} {self.num_waiting_reqs}',
            f'scheduler_step_counter {{}} {self.step_counter}',
            f'kv_cache_usage {{}} {self.kv_cache_usage}',
            f'prefix_cache_hit_rate {{}} {self.prefix_cache_stats.hit_rate}',
            f'prefix_cache_hits_total {{}} {self.prefix_cache_stats.num_hits}',
            f'prefix_cache_misses_total {{}} {self.prefix_cache_stats.num_misses}',
        ]
        
        if self.spec_decoding_stats:
            lines.extend([
                f'spec_decode_drafts_total {{}} {self.spec_decoding_stats.num_drafts}',
                f'spec_decode_acceptance_rate {{}} {self.spec_decoding_stats.acceptance_rate}',
            ])
        
        return '\n'.join(lines)


class SchedulerStatsCollector:
    """Collects and aggregates scheduler statistics over time."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self._history: list[SchedulerStats] = []
        self._current = SchedulerStats()
    
    @property
    def current(self) -> SchedulerStats:
        return self._current
    
    def record_step(
        self,
        num_running: int,
        num_waiting: int,
        kv_usage: float,
    ) -> None:
        """Record a scheduler step."""
        self._current.record_step(num_running, num_waiting, kv_usage)
    
    def commit(self) -> SchedulerStats:
        """Commit current stats to history and reset."""
        snapshot = self._current.clone()
        self._history.append(snapshot)
        
        # Trim history
        if len(self._history) > self.window_size:
            self._history = self._history[-self.window_size:]
        
        self._current.reset()
        return snapshot
    
    def get_averages(self) -> dict[str, float]:
        """Get average stats over history."""
        if not self._history:
            return {}
        
        n = len(self._history)
        return {
            "avg_running_reqs": sum(s.num_running_reqs for s in self._history) / n,
            "avg_waiting_reqs": sum(s.num_waiting_reqs for s in self._history) / n,
            "avg_kv_usage": sum(s.kv_cache_usage for s in self._history) / n,
            "avg_prefix_hit_rate": sum(s.prefix_cache_stats.hit_rate for s in self._history) / n,
        }
    
    def drain_events(self) -> list[KVCacheEvictionEvent]:
        """Get and clear eviction events."""
        events = list(self._current.kv_cache_eviction_events)
        self._current.kv_cache_eviction_events.clear()
        return events


# =============================================================================
# Convenience Functions
# =============================================================================

def create_scheduler_stats(
    enable_spec_decoding: bool = False,
    num_spec_tokens: int = 5,
) -> SchedulerStats:
    """Create scheduler stats with optional spec decoding."""
    stats = SchedulerStats()
    if enable_spec_decoding:
        stats.spec_decoding_stats = SpecDecodingStats.new(num_spec_tokens)
    stats.perf_stats = PerfStats()
    return stats


def create_stats_collector(window_size: int = 100) -> SchedulerStatsCollector:
    """Create a stats collector."""
    return SchedulerStatsCollector(window_size)
