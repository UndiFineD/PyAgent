"""
MemorySnapshot - Device memory profiling with GC tracking.

Inspired by vLLM's mem_utils.py and gc_utils.py patterns for production
memory monitoring and garbage collection optimization.

Phase 17: vLLM Pattern Integration
"""
from __future__ import annotations
import gc
import os
import sys
import time
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Optional, Iterator, Any
import tracemalloc


@dataclass
class MemorySnapshot:
    """
    Snapshot of memory usage at a point in time.
    
    Tracks Python, system, and optionally GPU memory.
    """
    timestamp: float = field(default_factory=time.time)
    
    # Python memory (via tracemalloc)
    python_current_mb: float = 0.0
    python_peak_mb: float = 0.0
    
    # System memory (RSS)
    rss_mb: float = 0.0
    vms_mb: float = 0.0
    
    # GPU memory (if available)
    gpu_allocated_mb: float = 0.0
    gpu_reserved_mb: float = 0.0
    gpu_peak_mb: float = 0.0
    
    # GC stats
    gc_generation_0: int = 0
    gc_generation_1: int = 0
    gc_generation_2: int = 0
    gc_objects: int = 0
    
    def delta(self, other: 'MemorySnapshot') -> dict:
        """Calculate memory change from another snapshot."""
        return {
            'python_current_delta_mb': self.python_current_mb - other.python_current_mb,
            'rss_delta_mb': self.rss_mb - other.rss_mb,
            'gpu_allocated_delta_mb': self.gpu_allocated_mb - other.gpu_allocated_mb,
            'gc_objects_delta': self.gc_objects - other.gc_objects,
            'elapsed_seconds': self.timestamp - other.timestamp,
        }
    
    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'python_current_mb': round(self.python_current_mb, 2),
            'python_peak_mb': round(self.python_peak_mb, 2),
            'rss_mb': round(self.rss_mb, 2),
            'vms_mb': round(self.vms_mb, 2),
            'gpu_allocated_mb': round(self.gpu_allocated_mb, 2),
            'gpu_reserved_mb': round(self.gpu_reserved_mb, 2),
            'gpu_peak_mb': round(self.gpu_peak_mb, 2),
            'gc_generation_0': self.gc_generation_0,
            'gc_generation_1': self.gc_generation_1,
            'gc_generation_2': self.gc_generation_2,
            'gc_objects': self.gc_objects,
        }


def capture_memory_snapshot(include_gpu: bool = True) -> MemorySnapshot:
    """
    Capture a complete memory snapshot.
    
    Args:
        include_gpu: Whether to capture GPU memory (requires torch)
        
    Returns:
        MemorySnapshot with current memory state
    """
    snapshot = MemorySnapshot()
    
    # Python memory via tracemalloc
    if tracemalloc.is_tracing():
        current, peak = tracemalloc.get_traced_memory()
        snapshot.python_current_mb = current / (1024 * 1024)
        snapshot.python_peak_mb = peak / (1024 * 1024)
    
    # System memory via psutil (if available)
    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        snapshot.rss_mb = mem_info.rss / (1024 * 1024)
        snapshot.vms_mb = mem_info.vms / (1024 * 1024)
    except ImportError:
        pass
    
    # GPU memory via torch (if available)
    if include_gpu:
        try:
            import torch
            if torch.cuda.is_available():
                snapshot.gpu_allocated_mb = torch.cuda.memory_allocated() / (1024 * 1024)
                snapshot.gpu_reserved_mb = torch.cuda.memory_reserved() / (1024 * 1024)
                snapshot.gpu_peak_mb = torch.cuda.max_memory_allocated() / (1024 * 1024)
        except ImportError:
            pass
    
    # GC stats
    gc_counts = gc.get_count()
    if len(gc_counts) >= 3:
        snapshot.gc_generation_0 = gc_counts[0]
        snapshot.gc_generation_1 = gc_counts[1]
        snapshot.gc_generation_2 = gc_counts[2]
    snapshot.gc_objects = len(gc.get_objects())
    
    return snapshot


class MemoryProfiler:
    """
    Context manager for profiling memory usage.
    
    Example:
        >>> with MemoryProfiler("model_load") as profiler:
        ...     model = load_model()
        >>> print(profiler.report())
    """
    
    def __init__(self, name: str = "profile", include_gpu: bool = True) -> None:
        self.name = name
        self.include_gpu = include_gpu
        self.start_snapshot: Optional[MemorySnapshot] = None
        self.end_snapshot: Optional[MemorySnapshot] = None
        self._start_trace = False
    
    def __enter__(self) -> 'MemoryProfiler':
        # Start tracemalloc if not running
        if not tracemalloc.is_tracing():
            tracemalloc.start()
            self._start_trace = True
        
        self.start_snapshot = capture_memory_snapshot(self.include_gpu)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end_snapshot = capture_memory_snapshot(self.include_gpu)
        
        if self._start_trace:
            tracemalloc.stop()
    
    def delta(self) -> Optional[dict]:
        """Get memory change during profiling."""
        if self.start_snapshot and self.end_snapshot:
            return self.end_snapshot.delta(self.start_snapshot)
        return None
    
    def report(self) -> dict:
        """Generate a complete profiling report."""
        delta = self.delta() or {}
        return {
            'name': self.name,
            'start': self.start_snapshot.to_dict() if self.start_snapshot else None,
            'end': self.end_snapshot.to_dict() if self.end_snapshot else None,
            'delta': delta,
        }


@contextmanager
def memory_profile(name: str = "profile", include_gpu: bool = True) -> Iterator[MemoryProfiler]:
    """
    Convenience context manager for memory profiling.
    
    Example:
        >>> with memory_profile("data_load") as prof:
        ...     data = load_data()
        >>> print(prof.delta())
    """
    profiler = MemoryProfiler(name, include_gpu)
    with profiler:
        yield profiler


class GCDebugger:
    """
    Garbage collection debugger for production monitoring.
    
    Inspired by vLLM's GCDebugger for tracking GC activity.
    
    Example:
        >>> debugger = GCDebugger()
        >>> debugger.start()
        >>> # ... run code ...
        >>> debugger.stop()
        >>> print(debugger.report())
    """
    
    def __init__(self, log_collections: bool = False) -> None:
        self.log_collections = log_collections
        self.collections: list[dict] = []
        self._original_callbacks: list = []
        self._running = False
        self._lock = threading.Lock()
        
        # Stats
        self.total_collections = 0
        self.total_collected = 0
        self.total_uncollectable = 0
        self.total_time_ms = 0.0
    
    def start(self) -> None:
        """Start GC debugging."""
        if self._running:
            return
        
        self._running = True
        self._original_callbacks = gc.callbacks.copy()
        gc.callbacks.append(self._gc_callback)
    
    def stop(self) -> None:
        """Stop GC debugging."""
        if not self._running:
            return
        
        self._running = False
        if self._gc_callback in gc.callbacks:
            gc.callbacks.remove(self._gc_callback)
    
    def _gc_callback(self, phase: str, info: dict) -> None:
        """Callback invoked by GC."""
        with self._lock:
            if phase == 'start':
                self._gc_start_time = time.time()
            elif phase == 'stop':
                elapsed_ms = (time.time() - getattr(self, '_gc_start_time', time.time())) * 1000
                
                self.total_collections += 1
                self.total_collected += info.get('collected', 0)
                self.total_uncollectable += info.get('uncollectable', 0)
                self.total_time_ms += elapsed_ms
                
                if self.log_collections:
                    collection_info = {
                        'generation': info.get('generation', -1),
                        'collected': info.get('collected', 0),
                        'uncollectable': info.get('uncollectable', 0),
                        'elapsed_ms': round(elapsed_ms, 3),
                        'timestamp': time.time(),
                    }
                    self.collections.append(collection_info)
    
    def force_collection(self, generation: int = 2) -> dict:
        """Force a garbage collection and return stats."""
        start = time.time()
        collected = gc.collect(generation)
        elapsed_ms = (time.time() - start) * 1000
        
        return {
            'generation': generation,
            'collected': collected,
            'elapsed_ms': round(elapsed_ms, 3),
        }
    
    def get_top_objects(self, n: int = 10) -> list[tuple[str, int]]:
        """Get the top N most common object types by count."""
        type_counts: dict[str, int] = {}
        for obj in gc.get_objects():
            type_name = type(obj).__name__
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def report(self) -> dict:
        """Generate a GC debugging report."""
        return {
            'total_collections': self.total_collections,
            'total_collected': self.total_collected,
            'total_uncollectable': self.total_uncollectable,
            'total_time_ms': round(self.total_time_ms, 2),
            'avg_collection_time_ms': round(
                self.total_time_ms / max(1, self.total_collections), 2
            ),
            'current_gc_counts': gc.get_count(),
            'total_objects': len(gc.get_objects()),
            'collection_log': self.collections[-10:] if self.collections else [],
        }
    
    def __enter__(self) -> 'GCDebugger':
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


def freeze_gc_heap() -> int:
    """
    Freeze the GC heap after initialization.
    
    This marks all current objects as "immortal" to reduce GC overhead.
    Should be called after all static/long-lived objects are created.
    
    Returns:
        Number of objects frozen
    """
    gc.collect()  # Full collection first
    gc.freeze()
    return len(gc.get_freeze_count()) if hasattr(gc, 'get_freeze_count') else -1


def unfreeze_gc_heap() -> None:
    """Unfreeze the GC heap."""
    gc.unfreeze()


def gc_stats() -> dict:
    """Get current GC statistics."""
    counts = gc.get_count()
    thresholds = gc.get_threshold()
    
    return {
        'counts': {
            'generation_0': counts[0],
            'generation_1': counts[1],
            'generation_2': counts[2],
        },
        'thresholds': {
            'generation_0': thresholds[0],
            'generation_1': thresholds[1],
            'generation_2': thresholds[2],
        },
        'total_objects': len(gc.get_objects()),
        'gc_enabled': gc.isenabled(),
    }


__all__ = [
    'MemorySnapshot',
    'MemoryProfiler',
    'GCDebugger',
    'capture_memory_snapshot',
    'memory_profile',
    'freeze_gc_heap',
    'unfreeze_gc_heap',
    'gc_stats',
]
