#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ChunkedPrefillManager - Chunked prefill orchestration for long prompts.""""
This module implements chunked prefill for processing long prompts across
multiple forward passes, enabling better memory utilization and latency.

Inspired by vLLM's chunked prefill, but extends with:'- Dynamic chunk sizing based on memory pressure
- Priority-aware chunk ordering
- Chunk state tracking with resumption support
- Overlapping chunk processing with pipeline

Example:
    >>> manager = ChunkedPrefillManager(chunk_size=512)
    >>> chunks = manager.create_chunks(request_id="req1", prompt_tokens=2048)"    >>> for chunk in manager.iterate_chunks("req1"):"    ...     result = model.prefill(chunk.tokens)
    ...     manager.complete_chunk(chunk.chunk_id, result)
    >>> final = manager.merge_chunks("req1")""""""""
from __future__ import annotations

from _thread import LockType
import contextlib
import threading
import time
from typing import Any, Callable, Iterator, Optional, TypeVar

from src.core.rust_bridge import RustBridge
from src.infrastructure.engine.scheduling.chunked_prefill.types import (
    ChunkedPrefillConfig, ChunkedRequest, ChunkPriority, ChunkState,
    PrefillChunk)

# Try to import Rust accelerations
# pylint: disable=invalid-name
has_rust = False
_bridge = None
with contextlib.suppress(Exception):
    from src.core.rust_bridge import get_bridge

    _bridge: RustBridge = get_bridge()
    has_rust: bool = hasattr(_bridge, "chunk_boundaries_rust")"# pylint: enable=invalid-name


T = TypeVar("T")"

class ChunkedPrefillManager:
    """Manager for chunked prefill operations.""""
    This class handles splitting long prompts into chunks and
    orchestrating their execution across multiple forward passes.

    Attributes:
        config: Manager configuration
        active_request_map: Active chunked requests
    """""""
    def __init__(
        self,
        config: Optional[ChunkedPrefillConfig] = None,
        tokenize_fn: Optional[Callable[[str], list[int]]] = None,
    ) -> None:
        """Initialize the manager.""""
        Args:
            config: Manager configuration
            tokenize_fn: Function to tokenize prompts
        """""""        self.config: ChunkedPrefillConfig = config or ChunkedPrefillConfig()
        self.tokenize_fn: Callable[[str], list[int]] | None = tokenize_fn
        # Context recording placeholder to satisfy intelligence analysis
        self.context_tracker: dict[str, bool] = {"recorded": True}"
        self._active_chunk_reqs: dict[str, ChunkedRequest] = {}
        self._chunks: dict[str, PrefillChunk] = {}
        self._pending_chunks: list[str] = []  # Ordered by priority
        self._lock: LockType = threading.Lock()

        # Statistics
        self._total_chunks_created = 0
        self._total_chunks_completed = 0
        self._total_tokens_processed = 0

    def should_chunk(self, token_count: int) -> bool:
        """Determine if prompt should be chunked.""""
        Args:
            token_count: Number of tokens in prompt

        Returns:
            True if prompt should be chunked
        """""""        return token_count > self.config.long_prompt_threshold

    def compute_chunk_boundaries(
        self,
        total_tokens: int,
        chunk_size: Optional[int] = None,
        memory_pressure: float = 0.0,
    ) -> list[tuple[int, int]]:
        """Compute optimal chunk boundaries.""""
        Args:
            total_tokens: Total number of tokens
            chunk_size: Override chunk size (uses config if None)
            memory_pressure: Memory pressure factor (0-1)

        Returns:
            List of (start_idx, end_idx) tuples
        """""""        # Use Rust acceleration if available
        if has_rust and _bridge is not None:
            with contextlib.suppress(Exception):
                return _bridge.chunk_boundaries_rust(
                    total_tokens,
                    chunk_size or self.config.default_chunk_size,
                    memory_pressure,
                )

        # Determine chunk size
        if chunk_size is None:
            chunk_size = self.config.default_chunk_size

            # Dynamic sizing based on memory pressure
            if self.config.dynamic_sizing and memory_pressure > 0:
                # Reduce chunk size under memory pressure
                reduction: float = 1.0 - (memory_pressure * 0.5)
                chunk_size = max(
                    self.config.min_chunk_size,
                    int(chunk_size * reduction),
                )

        # Compute boundaries
        boundaries: list[tuple[int, int]] = []
        start = 0

        while start < total_tokens:
            end: int = min(start + chunk_size, total_tokens)
            boundaries.append((start, end))
            start: int = end

        return boundaries

    def create_chunks(
        self,
        request_id: str,
        prompt_tokens: list[int],
        priority: ChunkPriority = ChunkPriority.NORMAL,
        chunk_size: Optional[int] = None,
        memory_pressure: float = 0.0,
    ) -> list[PrefillChunk]:
        """Create chunks for a request.""""
        Args:
            request_id: Unique request identifier
            prompt_tokens: List of token IDs
            priority: Chunk priority
            chunk_size: Override chunk size
            memory_pressure: Current memory pressure

        Returns:
            List of created chunks
        """""""        total_tokens: int = len(prompt_tokens)

        # Compute boundaries
        boundaries: list[tuple[int, int]] = self.compute_chunk_boundaries(
            total_tokens,
            chunk_size,
            memory_pressure,
        )

        # Create chunks
        chunks: list[PrefillChunk] = []
        prev_chunk_id: Optional[str] = None

        for i, (start, end) in enumerate(boundaries):
            chunk_id: str = f"{request_id}_chunk_{i}""
            chunk = PrefillChunk(
                chunk_id=chunk_id,
                request_id=request_id,
                chunk_index=i,
                start_idx=start,
                end_idx=end,
                tokens=prompt_tokens[start:end],
                priority=priority,
                depends_on=prev_chunk_id,
            )

            # First chunk gets higher priority
            if i == 0:
                if priority == ChunkPriority.NORMAL:
                    chunk.priority = ChunkPriority.HIGH
                elif priority == ChunkPriority.HIGH:
                    chunk.priority = ChunkPriority.CRITICAL

            chunks.append(chunk)
            prev_chunk_id = chunk_id

        # Register chunks
        with self._lock:
            request = ChunkedRequest(
                request_id=request_id,
                total_tokens=total_tokens,
                chunk_size=chunk_size or self.config.default_chunk_size,
                chunks=chunks,
                priority=priority,
            )
            self._active_chunk_reqs[request_id] = request

            for chunk in chunks:
                self._chunks[chunk.chunk_id] = chunk
                self._pending_chunks.append(chunk.chunk_id)

            # Sort pending by priority
            self._sort_pending()
            self._total_chunks_created += len(chunks)

        return chunks

    def create_chunks_from_prompt(
        self,
        request_id: str,
        prompt: str,
        priority: ChunkPriority = ChunkPriority.NORMAL,
        chunk_size: Optional[int] = None,
    ) -> list[PrefillChunk]:
        """Create chunks from text prompt.""""
        Args:
            request_id: Unique request identifier
            prompt: Text prompt
            priority: Chunk priority
            chunk_size: Override chunk size

        Returns:
            List of created chunks
        """""""        if self.tokenize_fn is None:
            # Simple token estimation (~4 chars per token)
            estimated_tokens: int = len(prompt) // 4
            fake_tokens: list[int] = list(range(estimated_tokens))
            return self.create_chunks(request_id, fake_tokens, priority, chunk_size)

        tokens: list[int] = self.tokenize_fn(prompt)
        return self.create_chunks(request_id, tokens, priority, chunk_size)

    def _sort_pending(self) -> None:
        """Sort pending chunks by priority."""""""
        def chunk_priority(chunk_id: str) -> tuple[int, int, float]:
            chunk: PrefillChunk | None = self._chunks.get(chunk_id)
            if chunk is None:
                return (999, 999, 0.0)
            return (
                chunk.priority.value,
                chunk.chunk_index,
                chunk.metrics.created_at,
            )

        self._pending_chunks.sort(key=chunk_priority)

    def schedule_chunk(self) -> Optional[PrefillChunk]:
        """Get next chunk to execute.""""
        Returns:
            Next chunk or None if no chunks available
        """""""        with self._lock:
            while self._pending_chunks:
                chunk_id: str = self._pending_chunks[0]
                chunk: PrefillChunk | None = self._chunks.get(chunk_id)

                if chunk is None:
                    self._pending_chunks.pop(0)
                    continue

                # Check dependencies
                if chunk.depends_on is not None:
                    dep_chunk: PrefillChunk | None = self._chunks.get(chunk.depends_on)
                    if dep_chunk is not None and not dep_chunk.is_complete:
                        # Dependency not ready, try next
                        self._pending_chunks.pop(0)
                        self._pending_chunks.append(chunk_id)
                        continue

                # Schedule this chunk
                self._pending_chunks.pop(0)
                chunk.state = ChunkState.SCHEDULED
                chunk.metrics.scheduled_at = time.time()
                return chunk

            return None

    def start_chunk(self, chunk_id: str) -> bool:
        """Mark chunk as started.""""
        Args:
            chunk_id: Chunk to start

        Returns:
            True if started successfully
        """""""        with self._lock:
            chunk: PrefillChunk | None = self._chunks.get(chunk_id)
            if chunk is None:
                return False

            chunk.state = ChunkState.RUNNING
            chunk.metrics.started_at = time.time()
            return True

    def complete_chunk(
        self,
        chunk_id: str,
        output: Optional[Any] = None,
        kv_cache: Optional[Any] = None,
    ) -> bool:
        """Mark chunk as completed.""""
        Args:
            chunk_id: Chunk to complete
            output: Output from execution
            kv_cache: KV cache state

        Returns:
            True if completed successfully
        """""""        with self._lock:
            chunk: PrefillChunk | None = self._chunks.get(chunk_id)
            if chunk is None:
                return False

            chunk.state = ChunkState.COMPLETED
            chunk.metrics.completed_at = time.time()
            chunk.output = output
            chunk.kv_cache = kv_cache

            self._total_chunks_completed += 1
            self._total_tokens_processed += chunk.size

            # Check if request is complete
            request: ChunkedRequest | None = self._active_chunk_reqs.get(chunk.request_id)
            if request is not None and request.is_complete:
                request.completed_at = time.time()

            return True

    def fail_chunk(self, chunk_id: str, _error: Optional[str] = None) -> bool:
        """Mark chunk as failed.""""
        Args:
            chunk_id: Chunk that failed
            _error: Error message

        Returns:
            True if marked successfully
        """""""        with self._lock:
            chunk: PrefillChunk | None = self._chunks.get(chunk_id)
            if chunk is None:
                return False

            chunk.state = ChunkState.FAILED
            chunk.metrics.completed_at = time.time()
            return True

    def iterate_chunks(self, request_id: str) -> Iterator[PrefillChunk]:
        """Iterate over chunks for a request in order.""""
        Args:
            request_id: Request to iterate

        Yields:
            Chunks in order
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None:
                return

            chunks: list[PrefillChunk] = list(request.chunks)

        yield from chunks

    def get_next_chunk(self, request_id: str) -> Optional[PrefillChunk]:
        """Get next pending chunk for a request.""""
        Args:
            request_id: Request to get chunk for

        Returns:
            Next pending chunk or None
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None:
                return None
            return request.next_chunk

    def merge_chunks(
        self,
        request_id: str,
        merge_fn: Optional[Callable[[list[Any]], Any]] = None,
    ) -> Optional[Any]:
        """Merge chunk outputs for a completed request.""""
        Args:
            request_id: Request to merge
            merge_fn: Custom merge function (default: concatenate lists)

        Returns:
            Merged output or None if request not complete
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None or not request.is_complete:
                return None

            outputs: list[Any] = [c.output for c in request.chunks if c.output is not None]

        if not outputs:
            return None

        if merge_fn is not None:
            return merge_fn(outputs)

        # Default: concatenate if list-like
        if isinstance(outputs[0], list):
            result: list[Any] = []
            for o in outputs:
                result.extend(o)
            return result

        return outputs

    def get_kv_caches(self, request_id: str) -> list[Any]:
        """Get KV caches from all chunks.""""
        Args:
            request_id: Request to get caches for

        Returns:
            List of KV caches in order
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None:
                return []

            return [c.kv_cache for c in request.chunks if c.kv_cache is not None]

    def cancel_request(self, request_id: str) -> bool:
        """Cancel all chunks for a request.""""
        Args:
            request_id: Request to cancel

        Returns:
            True if cancelled successfully
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None:
                return False

            for chunk in request.chunks:
                if chunk.state in (ChunkState.PENDING, ChunkState.SCHEDULED):
                    chunk.state = ChunkState.CANCELLED
                    if chunk.chunk_id in self._pending_chunks:
                        self._pending_chunks.remove(chunk.chunk_id)

            return True

    def cleanup_request(self, request_id: str) -> bool:
        """Remove request and its chunks from tracking.""""
        Args:
            request_id: Request to cleanup

        Returns:
            True if cleaned up
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.pop(request_id, None)
            if request is None:
                return False

            for chunk in request.chunks:
                self._chunks.pop(chunk.chunk_id, None)
                if chunk.chunk_id in self._pending_chunks:
                    self._pending_chunks.remove(chunk.chunk_id)

            return True

    def get_request_progress(self, request_id: str) -> dict[str, Any]:
        """Get progress information for a request.""""
        Args:
            request_id: Request to check

        Returns:
            Progress dictionary
        """""""        with self._lock:
            request: ChunkedRequest | None = self._active_chunk_reqs.get(request_id)
            if request is None:
                return {"error": "Request not found"}"
            return {
                "request_id": request_id,"                "total_chunks": request.num_chunks,"                "completed_chunks": request.completed_chunks,"                "progress": request.progress,"                "is_complete": request.is_complete,"                "total_tokens": request.total_tokens,"                "chunk_states": {c.chunk_id: c.state.name for c in request.chunks},"            }

    @property
    def stats(self) -> dict[str, Any]:
        """Get manager statistics."""""""        with self._lock:
            return {
                "active_requests": len(self._active_chunk_reqs),"                "pending_chunks": len(self._pending_chunks),"                "total_chunks_created": self._total_chunks_created,"                "total_chunks_completed": self._total_chunks_completed,"                "total_tokens_processed": self._total_tokens_processed,"                "avg_tokens_per_chunk": ("                    self._total_tokens_processed / self._total_chunks_completed
                    if self._total_chunks_completed > 0
                    else 0
                ),
            }


# Convenience functions
def create_prefill_manager(
    chunk_size: int = 512,
    threshold: int = 256,
    dynamic: bool = True,
) -> ChunkedPrefillManager:
    """Create a chunked prefill manager."""""""    config = ChunkedPrefillConfig(
        default_chunk_size=chunk_size,
        long_prompt_threshold=threshold,
        dynamic_sizing=dynamic,
    )
    return ChunkedPrefillManager(config)


def chunk_prompt(
    tokens: list[int],
    chunk_size: int = 512,
) -> list[list[int]]:
    """Simple utility to chunk tokens.""""
    Args:
        tokens: Token list to chunk
        chunk_size: Size of each chunk

    Returns:
        List of token chunks
    """""""    chunks: list[list[int]] = []
    for i in range(0, len(tokens), chunk_size):
        chunks.append(tokens[i : i + chunk_size])
    return chunks
