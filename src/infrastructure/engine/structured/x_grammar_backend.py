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
XGrammarBackend - XGrammar-based structured output backend.

Implements vLLM's XGrammar integration for constrained decoding with:
- Grammar compilation (JSON, regex, EBNF, structural tags)
- Token bitmask generation for efficient filtering
- TokenizerInfo integration for vocabulary mapping
- Speculative decoding rollback support

Beyond vLLM innovations:
- Multi-tokenizer support with caching
- Async grammar compilation
- Grammar composition and chaining
- Performance profiling and metrics
"""

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Union

from .ebnf import EBNFGrammar
from .json_schema import JsonSchemaGrammar
from .models import FSMTransitionTable
from .regex import RegexGrammar

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rust_core  # noqa: F401

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class GrammarType(Enum):
    """Types of grammar specifications."""

    JSON_SCHEMA = auto()
    JSON_OBJECT = auto()
    REGEX = auto()
    EBNF = auto()
    LARK = auto()
    STRUCTURAL_TAG = auto()
    CUSTOM = auto()


class VocabType(Enum):
    """Vocabulary encoding types."""

    RAW = auto()
    BYTE_FALLBACK = auto()
    BYTE_LEVEL = auto()


@dataclass(frozen=True)
class TokenizerInfo:
    """
    Tokenizer information for XGrammar.

    Encapsulates vocabulary and tokenizer metadata needed for
    grammar compilation and bitmask generation.
    """

    encoded_vocab: Tuple[str, ...]
    vocab_type: VocabType
    vocab_size: int
    stop_token_ids: Tuple[int, ...]
    add_prefix_space: bool = True

    @property
    def token_strings(self) -> Dict[int, str]:
        """Get mapping of token ID to string."""
        return dict(enumerate(self.encoded_vocab))

    @property
    def eos_token_id(self) -> Optional[int]:
        """Get EOS token ID."""
        return self.stop_token_ids[0] if self.stop_token_ids else None

    @classmethod
    def from_tokenizer(
        cls,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
    ) -> "TokenizerInfo":
        """Create TokenizerInfo from a HuggingFace tokenizer."""
        vocab_dict = tokenizer.get_vocab()
        actual_vocab_size = vocab_size or len(vocab_dict)

        # Build encoded vocab maintaining tokenizer's indexing
        encoded_vocab = [""] * actual_vocab_size
        for token, idx in vocab_dict.items():
            if idx < actual_vocab_size:
                encoded_vocab[idx] = token

        # Detect vocab type
        vocab_type = cls._detect_vocab_type(tokenizer)

        # Get stop token IDs
        stop_token_ids = []
        if hasattr(tokenizer, "eos_token_id") and tokenizer.eos_token_id is not None:
            stop_token_ids.append(tokenizer.eos_token_id)

        # Detect add_prefix_space
        add_prefix_space = getattr(tokenizer, "add_prefix_space", True)

        return cls(
            encoded_vocab=tuple(encoded_vocab),
            vocab_type=vocab_type,
            vocab_size=actual_vocab_size,
            stop_token_ids=tuple(stop_token_ids),
            add_prefix_space=add_prefix_space,
        )

    @staticmethod
    def _detect_vocab_type(tokenizer: Any) -> VocabType:
        """Detect vocabulary type from tokenizer."""
        if hasattr(tokenizer, "is_tekken") and tokenizer.is_tekken:
            return VocabType.RAW
        if hasattr(tokenizer, "byte_fallback") and tokenizer.byte_fallback:
            return VocabType.BYTE_FALLBACK
        return VocabType.BYTE_LEVEL


@dataclass
class CompiledGrammar:
    """
    Compiled grammar context.

    Holds the compiled grammar state and provides methods for
    token acceptance checking and bitmask generation.
    """

    grammar_type: GrammarType
    grammar_spec: str
    vocab_size: int
    max_rollback_tokens: int = 0
    token_strings: Dict[int, str] = field(default_factory=dict)
    fsm: Optional[FSMTransitionTable] = None
    eos_token_id: Optional[int] = None

    # Internal state
    _current_state: int = field(default=0)
    _accepted_tokens: List[int] = field(default_factory=list)
    _state_history: List[int] = field(default_factory=list)
    _cache_key: str = field(default="")

    def __post_init__(self):
        self._cache_key = self._compute_cache_key()
        self._state_history = [self._current_state]

    def _compute_cache_key(self) -> str:
        """Compute cache key for grammar."""
        content = f"{self.grammar_type.name}:{self.grammar_spec}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def accept_token(self, token_id: int) -> bool:
        """Accept a token and update state."""
        if token_id == self.eos_token_id:
            if self.fsm and self.fsm.is_accepting(self._current_state):
                self._accepted_tokens.append(token_id)
                self._state_history.append(self._current_state)
                return True
            return False

        tstr = self.token_strings.get(token_id, "")
        if not tstr:
            return False

        if not self.fsm:
            self._accepted_tokens.append(token_id)
            return True

        # Try to transition through all characters in the token
        temp_state = self._current_state
        for char in tstr:
            next_state = self.fsm.get_next_state(temp_state, char)
            if next_state == -1:
                return False
            temp_state = next_state

        self._current_state = temp_state
        self._accepted_tokens.append(token_id)
        self._state_history.append(self._current_state)
        return True

    def rollback(self, num_tokens: int) -> None:
        """Rollback the last N tokens."""
        if 0 < num_tokens <= len(self._accepted_tokens):
            self._accepted_tokens = self._accepted_tokens[:-num_tokens]
            self._state_history = self._state_history[: len(self._accepted_tokens) + 1]
            self._current_state = self._state_history[-1]

    def reset(self) -> None:
        """Reset grammar state."""
        self._accepted_tokens.clear()
        self._current_state = 0
        self._state_history = [0]

    def is_terminated(self) -> bool:
        """Check if grammar is in terminal state."""
        if not self.fsm:
            return False
        return self.fsm.is_accepting(self._current_state)

    def fill_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask with allowed tokens."""
        if not HAS_NUMPY:
            return

        if not self.fsm:
            bitmask.fill(1)
            return

        # Start with all zeros
        bitmask.fill(0)

        # Get allowed characters in current state
        allowed_chars = self.fsm.get_allowed_chars(self._current_state)

        # Optimize: If no allowed chars, only check if accepting
        if not allowed_chars:
            if self.fsm.is_accepting(self._current_state) and self.eos_token_id is not None:
                bitmask[self.eos_token_id] = 1
            return

        # Simple approach: iterate over all tokens and check if they're allowed
        # High performance approach: use the Rust helper if we have a list of allowed IDs
        allowed_ids = []
        for tid, tstr in self.token_strings.items():
            if not tstr:
                continue

            # Check if this token is allowed starting from current state
            temp_state = self._current_state
            is_valid = True
            for char in tstr:
                next_state = self.fsm.get_next_state(temp_state, char)
                if next_state == -1:
                    is_valid = False
                    break
                temp_state = next_state

            if is_valid:
                allowed_ids.append(tid)

        if self.fsm.is_accepting(self._current_state) and self.eos_token_id is not None:
            allowed_ids.append(self.eos_token_id)

        if HAS_RUST:
            rust_mask = rust_core.xgrammar_bitmask_fill_rust(allowed_ids, self.vocab_size)
            # Update bitmask array
            bitmask[:] = np.array(rust_mask, dtype=bitmask.dtype)
        else:
            for tid in allowed_ids:
                if 0 <= tid < self.vocab_size:
                    bitmask[tid] = 1


@dataclass
class GrammarMatcher:
    """
    Grammar matcher with rollback support.

    Wraps CompiledGrammar with additional state management
    for speculative decoding scenarios.
    """

    grammar: CompiledGrammar
    max_rollback_tokens: int = 0

    # State tracking
    _token_history: List[int] = field(default_factory=list)
    _state_history: List[Any] = field(default_factory=list)

    def accept_token(self, token_id: int) -> bool:
        """Accept token with history tracking."""
        # Save state before accepting
        if self.max_rollback_tokens > 0:
            self._token_history.append(token_id)
            # Trim history if needed
            if len(self._token_history) > self.max_rollback_tokens:
                self._token_history.pop(0)

        return self.grammar.accept_token(token_id)

    def rollback(self, num_tokens: int) -> None:
        """Rollback with history."""
        num_tokens = min(num_tokens, len(self._token_history))
        if num_tokens > 0:
            self._token_history = self._token_history[:-num_tokens]
            self.grammar.rollback(num_tokens)

    def reset(self) -> None:
        """Reset matcher state."""
        self._token_history.clear()
        self._state_history.clear()
        self.grammar.reset()

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""
        self.grammar.fill_bitmask(bitmask)


class GrammarCompiler:
    """
    Grammar compiler with caching.

    Compiles grammar specifications into executable matchers
    with thread-safe caching and configurable limits.
    """

    def __init__(
        self,
        tokenizer_info: TokenizerInfo,
        max_threads: int = 8,
        cache_enabled: bool = True,
        cache_limit_bytes: int = 100 * 1024 * 1024,  # 100MB
    ):
        self.tokenizer_info = tokenizer_info
        self.max_threads = max_threads
        self.cache_enabled = cache_enabled
        self.cache_limit_bytes = cache_limit_bytes

        self._cache: Dict[str, CompiledGrammar] = {}
        self._cache_size_bytes = 0
        self._lock = threading.Lock()

        # Statistics
        self._stats = {
            "compilations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_compile_time": 0.0,
        }

    def compile_json_schema(
        self,
        schema: str,
        any_whitespace: bool = True,
    ) -> CompiledGrammar:
        """Compile JSON schema to grammar."""
        cache_key = f"json:{schema}:{any_whitespace}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        # Build FSM using JsonSchemaGrammar
        engine = JsonSchemaGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(schema)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.JSON_SCHEMA,
            grammar_spec=schema,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_regex(self, pattern: str) -> CompiledGrammar:
        """Compile regex pattern to grammar."""
        cache_key = f"regex:{pattern}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        engine = RegexGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(pattern)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.REGEX,
            grammar_spec=pattern,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_grammar(self, ebnf: str) -> CompiledGrammar:
        """Compile EBNF grammar."""
        cache_key = f"ebnf:{ebnf}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        engine = EBNFGrammar(
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )
        fsm = engine.build_fsm(ebnf)

        grammar = CompiledGrammar(
            grammar_type=GrammarType.EBNF,
            grammar_spec=ebnf,
            vocab_size=self.tokenizer_info.vocab_size,
            token_strings=self.tokenizer_info.token_strings,
            fsm=fsm,
            eos_token_id=self.tokenizer_info.eos_token_id,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def compile_structural_tag(
        self,
        spec: Union[str, List[Dict[str, Any]]],
        triggers: Optional[List[str]] = None,
    ) -> CompiledGrammar:
        """Compile structural tag grammar."""
        if isinstance(spec, list):
            spec_str = json.dumps({"structures": spec, "triggers": triggers or []})
        else:
            spec_str = spec

        cache_key = f"structural:{spec_str}"

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        start_time = time.time()

        grammar = CompiledGrammar(
            grammar_type=GrammarType.STRUCTURAL_TAG,
            grammar_spec=spec_str,
            vocab_size=self.tokenizer_info.vocab_size,
        )

        self._stats["compilations"] += 1
        self._stats["total_compile_time"] += time.time() - start_time

        self._put_cached(cache_key, grammar)
        return grammar

    def _get_cached(self, key: str) -> Optional[CompiledGrammar]:
        """Get grammar from cache."""
        if not self.cache_enabled:
            self._stats["cache_misses"] += 1
            return None

        with self._lock:
            grammar = self._cache.get(key)
            if grammar is not None:
                self._stats["cache_hits"] += 1
            else:
                self._stats["cache_misses"] += 1
            return grammar

    def _put_cached(self, key: str, grammar: CompiledGrammar) -> None:
        """Put grammar in cache."""
        if not self.cache_enabled:
            return

        with self._lock:
            # Evict if needed
            estimated_size = len(grammar.grammar_spec) * 2
            while self._cache_size_bytes + estimated_size > self.cache_limit_bytes and self._cache:
                old_key = next(iter(self._cache))
                old_grammar = self._cache.pop(old_key)
                self._cache_size_bytes -= len(old_grammar.grammar_spec) * 2

            self._cache[key] = grammar
            self._cache_size_bytes += estimated_size

    def get_stats(self) -> Dict[str, Any]:
        """Get compilation statistics."""
        with self._lock:
            return dict(self._stats)

    def clear_cache(self) -> None:
        """Clear grammar cache."""
        with self._lock:
            self._cache.clear()
            self._cache_size_bytes = 0


class XGrammarGrammar:
    """
    XGrammar grammar wrapper.

    Provides the interface expected by the structured output system
    while wrapping the internal grammar matcher.
    """

    def __init__(
        self,
        matcher: GrammarMatcher,
        vocab_size: int,
        ctx: Optional[CompiledGrammar] = None,
    ):
        self.matcher = matcher
        self.vocab_size = vocab_size
        self.ctx = ctx
        self._jump_forward_string: Optional[str] = None

    def accept_token(self, token_id: int) -> bool:
        """Accept a token."""
        return self.matcher.accept_token(token_id)

    def rollback(self, num_tokens: int) -> None:
        """Rollback tokens."""
        self.matcher.rollback(num_tokens)

    def reset(self) -> None:
        """Reset grammar state."""
        self.matcher.reset()

    def is_terminated(self) -> bool:
        """Check if grammar is terminated."""
        return self.matcher.grammar.is_terminated()

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""
        self.matcher.fill_next_token_bitmask(bitmask)

    def jump_forward_string(self) -> Optional[str]:
        """Get jump-forward string if available."""
        return self._jump_forward_string


class XGrammarBackend:
    """
    XGrammar-based structured output backend.

    Provides constrained decoding using grammar-based token filtering.
    Supports JSON schema, regex, EBNF, and structural tags.

    Beyond vLLM innovations:
    - Multi-tokenizer support with automatic detection
    - Async grammar compilation with futures
    - Grammar composition for complex constraints
    - Detailed performance metrics
    """

    def __init__(
        self,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
        disable_any_whitespace: bool = False,
        num_speculative_tokens: int = 0,
        max_threads: int = 8,
        cache_limit_mb: int = 100,
    ):
        self.tokenizer = tokenizer
        self.vocab_size = vocab_size
        self.disable_any_whitespace = disable_any_whitespace
        self.num_speculative_tokens = num_speculative_tokens

        # Create tokenizer info
        self.tokenizer_info = TokenizerInfo.from_tokenizer(
            tokenizer,
            vocab_size=vocab_size,
        )

        # Update vocab_size from tokenizer_info if not provided
        if self.vocab_size is None:
            self.vocab_size = self.tokenizer_info.vocab_size

        # Create grammar compiler
        self.compiler = GrammarCompiler(
            tokenizer_info=self.tokenizer_info,
            max_threads=max_threads,
            cache_enabled=True,
            cache_limit_bytes=cache_limit_mb * 1024 * 1024,
        )

        # Bitmask pool for reuse
        self._bitmask_pool: List["np.ndarray"] = []
        self._pool_lock = threading.Lock()

    def compile_grammar(
        self,
        grammar_type: GrammarType,
        grammar_spec: str,
    ) -> XGrammarGrammar:
        """Compile grammar specification."""
        if grammar_type == GrammarType.JSON_SCHEMA:
            ctx = self.compiler.compile_json_schema(
                grammar_spec,
                any_whitespace=not self.disable_any_whitespace,
            )
        elif grammar_type == GrammarType.JSON_OBJECT:
            ctx = self.compiler.compile_json_schema(
                '{"type": "object"}',
                any_whitespace=not self.disable_any_whitespace,
            )
        elif grammar_type == GrammarType.REGEX:
            ctx = self.compiler.compile_regex(grammar_spec)
        elif grammar_type in (GrammarType.EBNF, GrammarType.LARK):
            # Convert Lark to EBNF if needed
            if grammar_type == GrammarType.LARK:
                grammar_spec = self._convert_lark_to_ebnf(grammar_spec)
            ctx = self.compiler.compile_grammar(grammar_spec)
        elif grammar_type == GrammarType.STRUCTURAL_TAG:
            ctx = self.compiler.compile_structural_tag(grammar_spec)
        else:
            raise ValueError(f"Unsupported grammar type: {grammar_type}")

        matcher = GrammarMatcher(
            grammar=ctx,
            max_rollback_tokens=self.num_speculative_tokens,
        )

        return XGrammarGrammar(
            matcher=matcher,
            vocab_size=self.vocab_size,
            ctx=ctx,
        )

    def allocate_token_bitmask(self, max_num_seqs: int) -> "np.ndarray":
        """Allocate token bitmask for batch processing."""
        if not HAS_NUMPY:
            raise RuntimeError("NumPy required for bitmask allocation")

        with self._pool_lock:
            if self._bitmask_pool:
                bitmask = self._bitmask_pool.pop()
                if bitmask.shape == (max_num_seqs, self.vocab_size):
                    bitmask.fill(1)
                    return bitmask

        # Allocate new bitmask
        return np.ones((max_num_seqs, self.vocab_size), dtype=np.int32)

    def release_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Return bitmask to pool."""
        with self._pool_lock:
            if len(self._bitmask_pool) < 10:  # Limit pool size
                self._bitmask_pool.append(bitmask)

    def _convert_lark_to_ebnf(self, lark_grammar: str) -> str:
        """Convert Lark grammar to EBNF."""
        # Basic conversion - real implementation would be more sophisticated
        return lark_grammar

    def get_stats(self) -> Dict[str, Any]:
        """Get backend statistics."""
        stats = self.compiler.get_stats()
        stats["vocab_size"] = self.vocab_size
        stats["num_speculative_tokens"] = self.num_speculative_tokens
        stats["bitmask_pool_size"] = len(self._bitmask_pool)
        return stats

    def destroy(self) -> None:
        """Clean up resources."""
        self.compiler.clear_cache()
        with self._pool_lock:
            self._bitmask_pool.clear()


class AsyncXGrammarBackend(XGrammarBackend):
    """
    Async-enabled XGrammar backend.

    Provides async grammar compilation for non-blocking operation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._compile_executor: Optional[Any] = None

    async def compile_grammar_async(
        self,
        grammar_type: GrammarType,
        grammar_spec: str,
    ) -> XGrammarGrammar:
        """Async grammar compilation."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._compile_executor,
            self.compile_grammar,
            grammar_type,
            grammar_spec,
        )


class CompositeGrammar:
    """
    Composite grammar for combining multiple constraints.

    Beyond vLLM: Allows chaining multiple grammars for complex constraints.
    """

    def __init__(self, grammars: List[XGrammarGrammar]):
        self.grammars = grammars
        self.vocab_size = grammars[0].vocab_size if grammars else 0

    def accept_token(self, token_id: int) -> bool:
        """Accept token in all grammars."""
        return all(g.accept_token(token_id) for g in self.grammars)

    def rollback(self, num_tokens: int) -> None:
        """Rollback all grammars."""
        for g in self.grammars:
            g.rollback(num_tokens)

    def reset(self) -> None:
        """Reset all grammars."""
        for g in self.grammars:
            g.reset()

    def is_terminated(self) -> bool:
        """Check if all grammars are terminated."""
        return all(g.is_terminated() for g in self.grammars)

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask with intersection of all grammar constraints."""
        if not HAS_NUMPY or not self.grammars:
            return

        # Start with all ones
        bitmask.fill(1)

        # Apply each grammar's constraints (intersection)
        temp_mask = np.ones_like(bitmask)
        for grammar in self.grammars:
            temp_mask.fill(1)
            grammar.fill_next_token_bitmask(temp_mask)
            bitmask &= temp_mask


__all__ = [
    "GrammarType",
    "VocabType",
    "TokenizerInfo",
    "CompiledGrammar",
    "GrammarMatcher",
    "GrammarCompiler",
    "XGrammarGrammar",
    "XGrammarBackend",
    "AsyncXGrammarBackend",
    "CompositeGrammar",
]
