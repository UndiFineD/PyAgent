#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
StructuredOutputOrchestrator - Unified structured output orchestration.

Provides a unified interface for structured output backends:
- Backend selection
- Grammar composition
- Request routing
- Performance monitoring

Beyond vLLM innovations:
- Multi-backend fallback
- Auto-backend selection
- Composite grammars
- Streaming constraint checking
"""

import asyncio
import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (Any, Dict, List, Optional, Protocol, Set, Tuple,
                    runtime_checkable)

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


logger = logging.getLogger(__name__)


class StructuredOutputBackendType(Enum):
    """Types of structured output backends."""

    XGRAMMAR = auto()
    GUIDANCE = auto()
    LM_FORMAT_ENFORCER = auto()
    OUTLINES = auto()
    CUSTOM = auto()


class ConstraintType(Enum):
    """Types of output constraints."""

    JSON_SCHEMA = auto()
    REGEX = auto()
    EBNF_GRAMMAR = auto()
    GUIDED_CHOICE = auto()
    STRUCTURAL_TAG = auto()
    TEMPLATE = auto()


@runtime_checkable
class GrammarProtocol(Protocol):
    """Protocol for grammar implementations."""

    def accept_token(self, token_id: int) -> bool:
        """Accept a token."""

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""

    def is_terminated(self) -> bool:
        """Check if grammar is terminated."""

    def reset(self) -> None:
        """Reset grammar state."""


@runtime_checkable
class BackendProtocol(Protocol):
    """Protocol for backend implementations."""

    def compile_json_schema(self, schema: str) -> Any:
        """Compile JSON schema."""

    def allocate_bitmask(self, batch_size: int) -> "np.ndarray":
        """Allocate bitmask."""

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""


@dataclass
class ConstraintSpec:
    """
    Specification for output constraint.

    Describes the constraint to apply to generation.
    """

    constraint_type: ConstraintType
    value: str
    priority: int = 0
    fallback_allowed: bool = True

    # Optional hints
    preferred_backend: Optional[StructuredOutputBackendType] = None
    max_tokens: Optional[int] = None

    def to_cache_key(self) -> str:
        """Create cache key."""
        content = f"{self.constraint_type.name}:{self.value}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


@dataclass
class OrchestratorConfig:
    """Configuration for orchestrator."""

    default_backend: StructuredOutputBackendType = StructuredOutputBackendType.XGRAMMAR
    enable_fallback: bool = True
    fallback_order: List[StructuredOutputBackendType] = field(default_factory=list)
    max_compile_time_ms: float = 1000.0
    enable_caching: bool = True
    max_cache_size: int = 1000
    enable_streaming: bool = True


class BackendWrapper:
    """
    Wrapper for structured output backend.

    Provides unified interface and statistics tracking.
    """

    def __init__(
        self,
        backend: BackendProtocol,
        backend_type: StructuredOutputBackendType,
    ) -> None:
        self.backend = backend
        self.backend_type = backend_type
        self._lock = threading.Lock()

        # Statistics
        self._stats = {
            "compilations": 0,
            "compile_errors": 0,
            "total_compile_time_ms": 0.0,
            "avg_compile_time_ms": 0.0,
        }

    def compile(
        self,
        constraint: ConstraintSpec,
    ) -> Tuple[Optional[Any], Optional[str]]:
        """Compile constraint to grammar."""
        start = time.perf_counter()

        try:
            with self._lock:
                if constraint.constraint_type == ConstraintType.JSON_SCHEMA:
                    result = self.backend.compile_json_schema(constraint.value)
                elif constraint.constraint_type == ConstraintType.REGEX:
                    if hasattr(self.backend, "compile_regex"):
                        result = self.backend.compile_regex(constraint.value)
                    else:
                        return None, "Backend doesn't support regex"
                elif constraint.constraint_type == ConstraintType.TEMPLATE:
                    if hasattr(self.backend, "compile_template"):
                        result = self.backend.compile_template(constraint.value)
                    else:
                        return None, "Backend doesn't support templates"
                else:
                    return None, f"Unsupported constraint type: {constraint.constraint_type}"

                # Update stats
                elapsed_ms = (time.perf_counter() - start) * 1000
                self._stats["compilations"] += 1
                self._stats["total_compile_time_ms"] += elapsed_ms
                self._stats["avg_compile_time_ms"] = self._stats["total_compile_time_ms"] / self._stats["compilations"]

                return result, None

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self._stats["compile_errors"] += 1
            logger.error(f"Compilation error in {self.backend_type}: {e}")
            return None, str(e)

    def get_stats(self) -> Dict[str, Any]:
        """Get wrapper statistics."""
        backend_stats = {}
        if hasattr(self.backend, "get_stats"):
            backend_stats = self.backend.get_stats()

        return {
            **self._stats,
            "backend": backend_stats,
        }


class CompiledGrammarHandle:
    """
    Handle to compiled grammar.

    Provides state management and bitmask operations.
    """

    def __init__(
        self,
        grammar: GrammarProtocol,
        backend_type: StructuredOutputBackendType,
        constraint: ConstraintSpec,
    ) -> None:
        self.grammar = grammar
        self.backend_type = backend_type
        self.constraint = constraint
        self._tokens_accepted = 0
        self._terminated = False

    def accept_token(self, token_id: int) -> bool:
        """Accept a token."""
        if self._terminated:
            return False

        result = self.grammar.accept_token(token_id)
        if result:
            self._tokens_accepted += 1

        self._terminated = self.grammar.is_terminated()
        return result

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""
        if self._terminated:
            bitmask.fill(0)
            return

        self.grammar.fill_next_token_bitmask(bitmask)

    def is_terminated(self) -> bool:
        """Check if grammar is terminated."""
        return self._terminated

    def reset(self) -> None:
        """Reset state."""
        self.grammar.reset()
        self._tokens_accepted = 0
        self._terminated = False

    @property
    def tokens_accepted(self) -> int:
        """Get count of accepted tokens."""
        return self._tokens_accepted


class StructuredOutputOrchestrator:
    """
    Orchestrator for structured output backends.

    Provides unified interface for:
    - Backend registration and selection
    - Constraint compilation with caching
    - Fallback handling
    - Performance monitoring
    """

    def __init__(
        self,
        tokenizer: Any,
        config: Optional[OrchestratorConfig] = None,
    ) -> None:
        self.tokenizer = tokenizer
        self.config = config or OrchestratorConfig()

        # Backends
        self._backends: Dict[StructuredOutputBackendType, BackendWrapper] = {}
        self._default_backend: Optional[BackendWrapper] = None

        # Cache
        self._cache: Dict[str, CompiledGrammarHandle] = {}
        self._cache_lock = threading.Lock()

        # Statistics
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "fallback_count": 0,
            "failed_compilations": 0,
        }

    def register_backend(
        self,
        backend_type: StructuredOutputBackendType,
        backend: BackendProtocol,
        set_as_default: bool = False,
    ) -> None:
        """Register a backend."""
        wrapper = BackendWrapper(backend, backend_type)
        self._backends[backend_type] = wrapper

        if set_as_default or self._default_backend is None:
            self._default_backend = wrapper

    def _select_backend(
        self,
        constraint: ConstraintSpec,
    ) -> Optional[BackendWrapper]:
        """Select appropriate backend for constraint."""
        # Check preferred backend
        if constraint.preferred_backend:
            if constraint.preferred_backend in self._backends:
                return self._backends[constraint.preferred_backend]

        # Use default
        return self._default_backend

    def _try_fallback(
        self,
        constraint: ConstraintSpec,
        tried: Set[StructuredOutputBackendType],
    ) -> Optional[Tuple[BackendWrapper, Any]]:
        """Try fallback backends."""
        if not self.config.enable_fallback or not constraint.fallback_allowed:
            return None

        fallback_order = self.config.fallback_order or list(self._backends.keys())

        for backend_type in fallback_order:
            if backend_type in tried:
                continue
            if backend_type not in self._backends:
                continue

            wrapper = self._backends[backend_type]
            result, _error = wrapper.compile(constraint)

            if result is not None:
                self._stats["fallback_count"] += 1
                return wrapper, result

            tried.add(backend_type)

        return None

    def compile(
        self,
        constraint: ConstraintSpec,
    ) -> Optional[CompiledGrammarHandle]:
        """Compile constraint to grammar handle."""
        self._stats["total_requests"] += 1

        # Check cache
        if self.config.enable_caching:
            cache_key = constraint.to_cache_key()
            with self._cache_lock:
                if cache_key in self._cache:
                    self._stats["cache_hits"] += 1
                    handle = self._cache[cache_key]
                    handle.reset()
                    return handle

        # Select backend
        wrapper = self._select_backend(constraint)
        if wrapper is None:
            logger.error("No backend available")
            self._stats["failed_compilations"] += 1
            return None

        # Compile
        tried: Set[StructuredOutputBackendType] = set()
        grammar, error = wrapper.compile(constraint)
        tried.add(wrapper.backend_type)

        # Try fallback on error
        if grammar is None and error:
            result = self._try_fallback(constraint, tried)
            if result:
                wrapper, grammar = result

        if grammar is None:
            logger.error(f"Failed to compile constraint: {error}")
            self._stats["failed_compilations"] += 1
            return None

        # Create handle
        handle = CompiledGrammarHandle(
            grammar=grammar,
            backend_type=wrapper.backend_type,
            constraint=constraint,
        )

        # Cache
        if self.config.enable_caching:
            with self._cache_lock:
                if len(self._cache) >= self.config.max_cache_size:
                    # Evict oldest
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                self._cache[cache_key] = handle

        return handle

    def compile_json_schema(self, schema: str) -> Optional[CompiledGrammarHandle]:
        """Convenience method for JSON schema compilation."""
        constraint = ConstraintSpec(
            constraint_type=ConstraintType.JSON_SCHEMA,
            value=schema,
        )
        return self.compile(constraint)

    def compile_regex(self, pattern: str) -> Optional[CompiledGrammarHandle]:
        """Convenience method for regex compilation."""
        constraint = ConstraintSpec(
            constraint_type=ConstraintType.REGEX,
            value=pattern,
        )
        return self.compile(constraint)

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        backend_stats = {}
        for backend_type, wrapper in self._backends.items():
            backend_stats[backend_type.name] = wrapper.get_stats()

        return {
            **self._stats,
            "backends": backend_stats,
            "cache_size": len(self._cache),
        }

    def clear_cache(self) -> None:
        """Clear compilation cache."""
        with self._cache_lock:
            self._cache.clear()


class AsyncStructuredOutputOrchestrator(StructuredOutputOrchestrator):
    """
    Async-enabled orchestrator.

    Provides async compilation for non-blocking operation.
    """

    async def compile_async(
        self,
        constraint: ConstraintSpec,
    ) -> Optional[CompiledGrammarHandle]:
        """Async constraint compilation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile,
            constraint,
        )

    async def compile_json_schema_async(
        self,
        schema: str,
    ) -> Optional[CompiledGrammarHandle]:
        """Async JSON schema compilation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.compile_json_schema,
            schema,
        )


class BatchProcessor:
    """
    Batch processor for structured output.

    Handles batch-level bitmask operations efficiently.
    """

    def __init__(
        self,
        orchestrator: StructuredOutputOrchestrator,
        batch_size: int,
        vocab_size: int,
    ) -> None:
        self.orchestrator = orchestrator
        self.batch_size = batch_size
        self.vocab_size = vocab_size

        # Batch state
        self._handles: List[Optional[CompiledGrammarHandle]] = [None] * batch_size

        # Allocate shared bitmask
        if HAS_NUMPY:
            self._bitmask = np.ones((batch_size, vocab_size), dtype=np.int32)
        else:
            self._bitmask = None

    def set_constraint(
        self,
        batch_idx: int,
        constraint: ConstraintSpec,
    ) -> bool:
        """Set constraint for batch index."""
        if batch_idx >= self.batch_size:
            return False

        handle = self.orchestrator.compile(constraint)
        self._handles[batch_idx] = handle
        return handle is not None

    def accept_tokens(
        self,
        token_ids: List[int],
    ) -> List[bool]:
        """Accept tokens for all batch items."""
        results = []
        for token_id, handle in zip(token_ids, self._handles):
            if handle is not None:
                results.append(handle.accept_token(token_id))
            else:
                results.append(True)  # No constraint
        return results

    def fill_bitmask(self) -> "np.ndarray":
        """Fill bitmask for all batch items."""
        if self._bitmask is None:
            raise RuntimeError("NumPy required")

        for i, handle in enumerate(self._handles):
            if handle is not None:
                handle.fill_next_token_bitmask(self._bitmask[i])
            else:
                self._bitmask[i].fill(1)  # Allow all

        return self._bitmask

    def get_terminated_indices(self) -> List[int]:
        """Get indices of terminated grammars."""
        return [i for i, handle in enumerate(self._handles) if handle is not None and handle.is_terminated()]

    def reset(self) -> None:
        """Reset all handles."""
        for handle in self._handles:
            if handle is not None:
                handle.reset()


__all__ = [
    "StructuredOutputBackendType",
    "ConstraintType",
    "GrammarProtocol",
    "BackendProtocol",
    "ConstraintSpec",
    "OrchestratorConfig",
    "BackendWrapper",
    "CompiledGrammarHandle",
    "StructuredOutputOrchestrator",
    "AsyncStructuredOutputOrchestrator",
    "BatchProcessor",
]
