"""
CUDAGraphConfig.py - CUDA graph mode management and configuration.

Inspired by vLLM's config/compilation.py. Provides CUDA graph capture
and replay management for optimized inference.

Phase 29: Execution Context, Batching & Async Streaming
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Set, Callable
from enum import Enum
import threading
import time
import logging

import numpy as np


logger = logging.getLogger(__name__)


# ============================================================================
# CUDA Graph Mode
# ============================================================================

class CUDAGraphMode(Enum):
    """
    CUDA graph execution modes.
    
    Based on vLLM's CUDAGraphMode enum.
    """
    NONE = 0       # No CUDA graphs, eager execution
    CAPTURE = 1    # Currently capturing a graph
    REPLAY = 2     # Replaying a captured graph
    DISABLED = 3   # Graphs explicitly disabled


# ============================================================================
# CUDA Graph Config
# ============================================================================

@dataclass
class CUDAGraphConfig:
    """
    Configuration for CUDA graph capture and replay.
    
    Based on vLLM's compilation config patterns.
    """
    # Enable/disable graphs
    enabled: bool = True
    
    # Max batch sizes for graph capture
    max_capture_batch_size: int = 256
    
    # Specific batch sizes to capture graphs for
    capture_sizes: List[int] = field(default_factory=lambda: [1, 2, 4, 8, 16, 32, 64, 128, 256])
    
    # Max sequence length for graph capture
    max_capture_seq_len: int = 8192
    
    # Memory pool options
    use_memory_pool: bool = True
    memory_pool_size_mb: int = 1024
    
    # Cudagraph recompilation settings
    cudagraph_copy_inputs: bool = True
    
    # Warmup iterations before capture
    warmup_iterations: int = 3
    
    # Per-layer graph capture
    per_layer_graphs: bool = False
    
    # Debug options
    debug_mode: bool = False
    
    def should_use_cudagraph(
        self,
        batch_size: int,
        seq_len: int,
    ) -> bool:
        """Check if CUDA graph should be used for given batch."""
        if not self.enabled:
            return False
        if batch_size > self.max_capture_batch_size:
            return False
        if seq_len > self.max_capture_seq_len:
            return False
        return True
    
    def get_padded_batch_size(self, batch_size: int) -> int:
        """Get padded batch size for graph lookup."""
        for size in sorted(self.capture_sizes):
            if size >= batch_size:
                return size
        return batch_size  # Fallback to exact size
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "enabled": self.enabled,
            "max_capture_batch_size": self.max_capture_batch_size,
            "capture_sizes": self.capture_sizes,
            "max_capture_seq_len": self.max_capture_seq_len,
            "use_memory_pool": self.use_memory_pool,
            "memory_pool_size_mb": self.memory_pool_size_mb,
            "cudagraph_copy_inputs": self.cudagraph_copy_inputs,
            "warmup_iterations": self.warmup_iterations,
            "per_layer_graphs": self.per_layer_graphs,
            "debug_mode": self.debug_mode,
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CUDAGraphConfig":
        """Create from dictionary."""
        return cls(**d)
    
    @classmethod
    def disabled(cls) -> "CUDAGraphConfig":
        """Create a disabled config."""
        return cls(enabled=False)


# ============================================================================
# CUDA Graph Entry
# ============================================================================

@dataclass
class CUDAGraphEntry:
    """
    A captured CUDA graph entry.
    
    Stores the graph and associated metadata.
    """
    # Key for lookup
    batch_size: int
    seq_len: int
    
    # Graph (simulated - real impl uses torch.cuda.CUDAGraph)
    graph_id: int
    
    # Input/output placeholders
    input_buffers: Dict[str, np.ndarray] = field(default_factory=dict)
    output_buffers: Dict[str, np.ndarray] = field(default_factory=dict)
    
    # Stats
    capture_time_ms: float = 0.0
    replay_count: int = 0
    total_replay_time_ms: float = 0.0
    
    def replay(self, inputs: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Replay the graph with given inputs.
        
        In real implementation, copies inputs to placeholders and replays.
        """
        start = time.perf_counter()
        
        # Copy inputs to placeholders
        for name, arr in inputs.items():
            if name in self.input_buffers:
                np.copyto(self.input_buffers[name], arr)
        
        # Simulate graph replay (real impl: self.graph.replay())
        # For simulation, just return output buffers
        outputs = {name: arr.copy() for name, arr in self.output_buffers.items()}
        
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        self.replay_count += 1
        self.total_replay_time_ms += elapsed_ms
        
        return outputs
    
    @property
    def key(self) -> Tuple[int, int]:
        """Get lookup key."""
        return (self.batch_size, self.seq_len)
    
    @property
    def avg_replay_time_ms(self) -> float:
        """Average replay time in milliseconds."""
        if self.replay_count == 0:
            return 0.0
        return self.total_replay_time_ms / self.replay_count


# ============================================================================
# CUDA Graph Registry
# ============================================================================

class CUDAGraphRegistry:
    """
    Registry for captured CUDA graphs.
    
    Manages graph capture, storage, and lookup.
    """
    
    def __init__(self, config: Optional[CUDAGraphConfig] = None):
        self.config = config or CUDAGraphConfig()
        self._graphs: Dict[Tuple[int, int], CUDAGraphEntry] = {}
        self._lock = threading.Lock()
        self._next_id = 0
        self._capture_count = 0
    
    def capture(
        self,
        batch_size: int,
        seq_len: int,
        capture_fn: Callable[[], Dict[str, np.ndarray]],
        input_shapes: Dict[str, Tuple[int, ...]],
        output_shapes: Dict[str, Tuple[int, ...]],
    ) -> CUDAGraphEntry:
        """
        Capture a new CUDA graph.
        
        Args:
            batch_size: Batch size for the graph
            seq_len: Sequence length for the graph
            capture_fn: Function to capture (called during graph capture)
            input_shapes: Shapes of input buffers
            output_shapes: Shapes of output buffers
            
        Returns:
            Captured graph entry
        """
        start = time.perf_counter()
        
        # Allocate input/output buffers
        input_buffers = {
            name: np.zeros(shape, dtype=np.float32)
            for name, shape in input_shapes.items()
        }
        output_buffers = {
            name: np.zeros(shape, dtype=np.float32)
            for name, shape in output_shapes.items()
        }
        
        # Warmup
        for _ in range(self.config.warmup_iterations):
            capture_fn()
        
        # Capture (simulated - real impl uses torch.cuda.graph)
        with self._lock:
            graph_id = self._next_id
            self._next_id += 1
        
        capture_fn()  # Final capture run
        
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        
        entry = CUDAGraphEntry(
            batch_size=batch_size,
            seq_len=seq_len,
            graph_id=graph_id,
            input_buffers=input_buffers,
            output_buffers=output_buffers,
            capture_time_ms=elapsed_ms,
        )
        
        # Store in registry
        with self._lock:
            self._graphs[entry.key] = entry
            self._capture_count += 1
        
        logger.debug(
            f"Captured CUDA graph {graph_id} for batch_size={batch_size}, "
            f"seq_len={seq_len} in {elapsed_ms:.2f}ms"
        )
        
        return entry
    
    def get(
        self,
        batch_size: int,
        seq_len: int,
    ) -> Optional[CUDAGraphEntry]:
        """Get a captured graph for the given dimensions."""
        # Try exact match first
        key = (batch_size, seq_len)
        with self._lock:
            if key in self._graphs:
                return self._graphs[key]
        
        # Try padded batch size
        padded_batch = self.config.get_padded_batch_size(batch_size)
        padded_key = (padded_batch, seq_len)
        with self._lock:
            return self._graphs.get(padded_key)
    
    def has(self, batch_size: int, seq_len: int) -> bool:
        """Check if a graph exists."""
        return self.get(batch_size, seq_len) is not None
    
    def remove(self, batch_size: int, seq_len: int) -> bool:
        """Remove a graph from the registry."""
        key = (batch_size, seq_len)
        with self._lock:
            if key in self._graphs:
                del self._graphs[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all captured graphs."""
        with self._lock:
            self._graphs.clear()
    
    @property
    def num_graphs(self) -> int:
        """Number of captured graphs."""
        return len(self._graphs)
    
    def stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        with self._lock:
            total_replays = sum(g.replay_count for g in self._graphs.values())
            total_replay_time = sum(g.total_replay_time_ms for g in self._graphs.values())
            
            return {
                "num_graphs": len(self._graphs),
                "capture_count": self._capture_count,
                "total_replays": total_replays,
                "total_replay_time_ms": total_replay_time,
                "avg_replay_time_ms": total_replay_time / total_replays if total_replays > 0 else 0.0,
                "graphs": {
                    f"{g.batch_size}x{g.seq_len}": {
                        "graph_id": g.graph_id,
                        "capture_time_ms": g.capture_time_ms,
                        "replay_count": g.replay_count,
                        "avg_replay_time_ms": g.avg_replay_time_ms,
                    }
                    for g in self._graphs.values()
                },
            }


# ============================================================================
# CUDA Graph Manager
# ============================================================================

class CUDAGraphManager:
    """
    High-level manager for CUDA graph operations.
    
    Provides convenient interface for graph capture and replay.
    """
    
    def __init__(self, config: Optional[CUDAGraphConfig] = None):
        self.config = config or CUDAGraphConfig()
        self.registry = CUDAGraphRegistry(self.config)
        self._mode = CUDAGraphMode.NONE
        self._lock = threading.Lock()
    
    @property
    def mode(self) -> CUDAGraphMode:
        """Current CUDA graph mode."""
        return self._mode
    
    @mode.setter
    def mode(self, value: CUDAGraphMode) -> None:
        """Set CUDA graph mode."""
        with self._lock:
            self._mode = value
    
    def is_enabled(self) -> bool:
        """Check if CUDA graphs are enabled."""
        return self.config.enabled and self._mode != CUDAGraphMode.DISABLED
    
    def should_capture(self, batch_size: int, seq_len: int) -> bool:
        """Check if we should capture a graph for given dimensions."""
        if not self.is_enabled():
            return False
        if not self.config.should_use_cudagraph(batch_size, seq_len):
            return False
        if self.registry.has(batch_size, seq_len):
            return False
        return True
    
    def get_mode_for_batch(self, batch_size: int, seq_len: int) -> CUDAGraphMode:
        """Get the appropriate mode for a batch."""
        if not self.is_enabled():
            return CUDAGraphMode.DISABLED
        
        if not self.config.should_use_cudagraph(batch_size, seq_len):
            return CUDAGraphMode.NONE
        
        if self.registry.has(batch_size, seq_len):
            return CUDAGraphMode.REPLAY
        
        return CUDAGraphMode.CAPTURE
    
    def capture_graph(
        self,
        batch_size: int,
        seq_len: int,
        capture_fn: Callable[[], Dict[str, np.ndarray]],
        input_shapes: Dict[str, Tuple[int, ...]],
        output_shapes: Dict[str, Tuple[int, ...]],
    ) -> Optional[CUDAGraphEntry]:
        """
        Capture a CUDA graph.
        
        Sets mode to CAPTURE during capture, then restores.
        """
        if not self.is_enabled():
            return None
        
        old_mode = self._mode
        try:
            self.mode = CUDAGraphMode.CAPTURE
            return self.registry.capture(
                batch_size=batch_size,
                seq_len=seq_len,
                capture_fn=capture_fn,
                input_shapes=input_shapes,
                output_shapes=output_shapes,
            )
        finally:
            self.mode = old_mode
    
    def replay_graph(
        self,
        batch_size: int,
        seq_len: int,
        inputs: Dict[str, np.ndarray],
    ) -> Optional[Dict[str, np.ndarray]]:
        """
        Replay a captured graph.
        
        Returns None if no graph found.
        """
        entry = self.registry.get(batch_size, seq_len)
        if entry is None:
            return None
        
        old_mode = self._mode
        try:
            self.mode = CUDAGraphMode.REPLAY
            return entry.replay(inputs)
        finally:
            self.mode = old_mode
    
    def execute_or_capture(
        self,
        batch_size: int,
        seq_len: int,
        execute_fn: Callable[[Dict[str, np.ndarray]], Dict[str, np.ndarray]],
        inputs: Dict[str, np.ndarray],
        input_shapes: Optional[Dict[str, Tuple[int, ...]]] = None,
        output_shapes: Optional[Dict[str, Tuple[int, ...]]] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Execute using graph replay if available, otherwise capture and execute.
        
        This is the main entry point for graph-aware execution.
        """
        # Try replay first
        outputs = self.replay_graph(batch_size, seq_len, inputs)
        if outputs is not None:
            return outputs
        
        # Check if we should capture
        if self.should_capture(batch_size, seq_len):
            if input_shapes is None:
                input_shapes = {name: arr.shape for name, arr in inputs.items()}
            
            if output_shapes is None:
                # Execute once to get output shapes
                sample_outputs = execute_fn(inputs)
                output_shapes = {name: arr.shape for name, arr in sample_outputs.items()}
            
            # Capture
            def capture_fn():
                return execute_fn(inputs)
            
            self.capture_graph(
                batch_size=batch_size,
                seq_len=seq_len,
                capture_fn=capture_fn,
                input_shapes=input_shapes,
                output_shapes=output_shapes,
            )
            
            # Replay the newly captured graph
            return self.replay_graph(batch_size, seq_len, inputs) or execute_fn(inputs)
        
        # Eager execution
        return execute_fn(inputs)
    
    def stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "enabled": self.config.enabled,
            "mode": self._mode.name,
            "registry": self.registry.stats(),
            "config": self.config.to_dict(),
        }
    
    def reset(self) -> None:
        """Reset the manager."""
        self.registry.clear()
        self._mode = CUDAGraphMode.NONE
