"""Types and data structures for chunked prefill."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, TypeVar

T = TypeVar('T')


class ChunkState(Enum):
    """State of a prefill chunk."""
    PENDING = auto()      # Not yet scheduled
    SCHEDULED = auto()    # Scheduled for execution
    RUNNING = auto()      # Currently executing
    COMPLETED = auto()    # Finished successfully
    FAILED = auto()       # Error during execution
    CANCELLED = auto()    # Cancelled before completion


class ChunkPriority(Enum):
    """Priority for chunk scheduling."""
    CRITICAL = 0    # First chunks of critical requests
    HIGH = 1        # Continuation of in-flight requests
    NORMAL = 2      # Standard priority
    LOW = 3         # Background requests


@dataclass
class ChunkMetrics:
    """Metrics for chunk processing."""
    created_at: float = 0.0
    scheduled_at: float = 0.0
    started_at: float = 0.0
    completed_at: float = 0.0
    
    @property
    def queue_time_ms(self) -> float:
        """Time spent waiting to be scheduled."""
        if self.scheduled_at > 0:
            return (self.scheduled_at - self.created_at) * 1000
        return 0.0
    
    @property
    def execution_time_ms(self) -> float:
        """Time spent executing."""
        if self.completed_at > 0 and self.started_at > 0:
            return (self.completed_at - self.started_at) * 1000
        return 0.0
    
    @property
    def total_time_ms(self) -> float:
        """Total time from creation to completion."""
        if self.completed_at > 0:
            return (self.completed_at - self.created_at) * 1000
        return 0.0


@dataclass
class PrefillChunk:
    """A single chunk of prefill tokens.
    
    Attributes:
        chunk_id: Unique identifier for this chunk
        request_id: Parent request identifier
        chunk_index: Index within the request (0-based)
        start_idx: Start token index in original prompt
        end_idx: End token index (exclusive)
        tokens: Token IDs for this chunk
    """
    chunk_id: str
    request_id: str
    chunk_index: int
    start_idx: int
    end_idx: int
    tokens: list[int] = field(default_factory=list)
    
    state: ChunkState = ChunkState.PENDING
    priority: ChunkPriority = ChunkPriority.NORMAL
    metrics: ChunkMetrics = field(default_factory=ChunkMetrics)
    
    # Output from execution
    output: Optional[Any] = None
    kv_cache: Optional[Any] = None
    
    # Dependencies
    depends_on: Optional[str] = None  # Previous chunk ID
    
    def __post_init__(self) -> None:
        """Initialize metrics."""
        self.metrics.created_at = time.time()
    
    @property
    def size(self) -> int:
        """Number of tokens in this chunk."""
        return self.end_idx - self.start_idx
    
    @property
    def is_first(self) -> bool:
        """Whether this is the first chunk."""
        return self.chunk_index == 0
    
    @property
    def is_complete(self) -> bool:
        """Whether chunk has been processed."""
        return self.state == ChunkState.COMPLETED


@dataclass
class ChunkedRequest:
    """A request split into multiple chunks.
    
    Attributes:
        request_id: Unique request identifier
        total_tokens: Total prompt tokens
        chunks: List of chunks for this request
    """
    request_id: str
    total_tokens: int
    chunk_size: int
    
    chunks: list[PrefillChunk] = field(default_factory=list)
    priority: ChunkPriority = ChunkPriority.NORMAL
    
    # State tracking
    created_at: float = field(default_factory=time.time)
    completed_at: float = 0.0
    current_chunk: int = 0
    
    @property
    def num_chunks(self) -> int:
        """Total number of chunks."""
        return len(self.chunks)
    
    @property
    def completed_chunks(self) -> int:
        """Number of completed chunks."""
        return sum(1 for c in self.chunks if c.is_complete)
    
    @property
    def progress(self) -> float:
        """Progress as fraction (0-1)."""
        if not self.chunks:
            return 0.0
        return self.completed_chunks / len(self.chunks)
    
    @property
    def is_complete(self) -> bool:
        """Whether all chunks are complete."""
        return all(c.is_complete for c in self.chunks)
    
    @property
    def next_chunk(self) -> Optional[PrefillChunk]:
        """Get next chunk to process."""
        for chunk in self.chunks:
            if chunk.state == ChunkState.PENDING:
                return chunk
        return None


@dataclass
class ChunkedPrefillConfig:
    """Configuration for chunked prefill."""
    default_chunk_size: int = 512
    min_chunk_size: int = 64
    max_chunk_size: int = 2048
    long_prompt_threshold: int = 256
    dynamic_sizing: bool = True
    overlap_enabled: bool = False
    max_concurrent_chunks: int = 2
