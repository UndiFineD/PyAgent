# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Structured Output Manager
# Inspired by vLLM's v1/structured_output/__init__.py

"""
StructuredOutputManager: Engine-level orchestration for constrained generation.

Provides:
- Multiple backend support (regex, JSON schema, grammar, choice)
- Async grammar compilation
- Bitmask-based token constraints
- Speculative decoding integration with rollback
"""

from __future__ import annotations

import hashlib
import json
import threading
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import numpy as np


# =============================================================================
# Enums & Types
# =============================================================================

class GrammarType(Enum):
    """Types of grammar constraints supported."""
    NONE = auto()
    JSON = auto()           # JSON Schema validation
    JSON_OBJECT = auto()    # Any valid JSON object
    REGEX = auto()          # Regular expression
    GRAMMAR = auto()        # EBNF/Lark grammar
    CHOICE = auto()         # Choice from list
    FUNCTION_CALL = auto()  # Function call schema
    STRUCTURAL_TAG = auto() # XML-like structural tags


class CompilationStatus(Enum):
    """Status of grammar compilation."""
    PENDING = auto()
    COMPILING = auto()
    READY = auto()
    FAILED = auto()
    CACHED = auto()


# =============================================================================
# Data Classes
# =============================================================================

@dataclass(frozen=True)
class GrammarSpec:
    """Specification for a grammar constraint."""
    grammar_type: GrammarType
    spec: str  # JSON schema string, regex pattern, EBNF, or choice list
    strict: bool = True  # Whether to strictly enforce the grammar
    max_tokens: Optional[int] = None  # Maximum tokens to generate
    
    def to_cache_key(self) -> str:
        """Generate cache key for this spec."""
        content = f"{self.grammar_type.name}:{self.spec}:{self.strict}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class CompilationResult:
    """Result of grammar compilation."""
    status: CompilationStatus
    grammar: Optional["StructuredOutputGrammar"] = None
    error: Optional[str] = None
    compile_time_ms: float = 0.0
    
    @property
    def is_ready(self) -> bool:
        return self.status == CompilationStatus.READY
    
    @property
    def is_failed(self) -> bool:
        return self.status == CompilationStatus.FAILED


@dataclass
class ValidationResult:
    """Result of token validation."""
    is_valid: bool
    accepted_prefix_length: int = 0
    error_message: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class BackendStats:
    """Statistics for a structured output backend."""
    grammars_compiled: int = 0
    grammars_cached: int = 0
    compilations_failed: int = 0
    total_compile_time_ms: float = 0.0
    total_tokens_validated: int = 0
    validation_rejections: int = 0


# =============================================================================
# Abstract Base Classes
# =============================================================================

class StructuredOutputGrammar(ABC):
    """
    Abstract base class for grammar instances.
    
    Each grammar tracks FSM state for a single generation request,
    supports token acceptance, and provides bitmask generation.
    """
    
    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: Optional[str] = None,
    ):
        self.grammar_spec = grammar_spec
        self.vocab_size = vocab_size
        self.request_id = request_id
        self._is_terminated = False
        self._tokens_accepted = 0
        self._state_history: List[Any] = []
    
    @abstractmethod
    def accept_tokens(self, tokens: Sequence[int]) -> bool:
        """
        Accept tokens and advance FSM state.
        
        Args:
            tokens: Token IDs to accept.
            
        Returns:
            True if all tokens were accepted, False if any were rejected.
        """
        pass
    
    @abstractmethod
    def validate_tokens(self, tokens: Sequence[int]) -> int:
        """
        Validate tokens without advancing state.
        
        Args:
            tokens: Token IDs to validate.
            
        Returns:
            Length of the longest valid prefix.
        """
        pass
    
    @abstractmethod
    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        """
        Fill a bitmask with allowed tokens at current state.
        
        Args:
            bitmask: Pre-allocated numpy array of shape [batch_size, vocab_size].
            batch_index: Which row to fill.
        """
        pass
    
    @abstractmethod
    def get_allowed_tokens(self) -> List[int]:
        """Get list of allowed token IDs at current state."""
        pass
    
    def rollback(self, num_tokens: int) -> None:
        """
        Rollback FSM state by the specified number of tokens.
        
        Used for speculative decoding when draft tokens are rejected.
        """
        if num_tokens <= 0:
            return
        
        rollback_count = min(num_tokens, len(self._state_history))
        for _ in range(rollback_count):
            if self._state_history:
                self._state_history.pop()
        
        self._tokens_accepted = max(0, self._tokens_accepted - rollback_count)
        self._is_terminated = False
    
    def is_terminated(self) -> bool:
        """Check if the grammar has reached an accepting state."""
        return self._is_terminated
    
    def reset(self) -> None:
        """Reset grammar to initial state."""
        self._is_terminated = False
        self._tokens_accepted = 0
        self._state_history.clear()


class StructuredOutputBackend(ABC):
    """
    Abstract backend for grammar compilation and management.
    
    Backends implement different constraint engines:
    - Regex-based (outlines, interegular)
    - Grammar-based (xgrammar, guidance)
    - JSON Schema validators
    """
    
    def __init__(
        self,
        vocab_size: int,
        tokenizer_encode: Optional[Callable[[str], List[int]]] = None,
        tokenizer_decode: Optional[Callable[[List[int]], str]] = None,
    ):
        self.vocab_size = vocab_size
        self.tokenizer_encode = tokenizer_encode
        self.tokenizer_decode = tokenizer_decode
        self.stats = BackendStats()
        self._lock = threading.Lock()
    
    @abstractmethod
    def compile_grammar(
        self,
        grammar_spec: GrammarSpec,
        request_id: Optional[str] = None,
    ) -> StructuredOutputGrammar:
        """
        Compile a grammar specification into a usable grammar instance.
        
        Args:
            grammar_spec: The grammar specification to compile.
            request_id: Optional request identifier.
            
        Returns:
            Compiled grammar instance.
        """
        pass
    
    @abstractmethod
    def get_supported_types(self) -> List[GrammarType]:
        """Get list of grammar types this backend supports."""
        pass
    
    def allocate_token_bitmask(
        self,
        max_batch_size: int,
    ) -> np.ndarray:
        """
        Allocate a reusable token bitmask.
        
        Args:
            max_batch_size: Maximum batch size to support.
            
        Returns:
            Numpy array of shape [max_batch_size, vocab_size], dtype=bool.
        """
        return np.zeros((max_batch_size, self.vocab_size), dtype=np.bool_)
    
    def get_stats(self) -> BackendStats:
        """Get backend statistics."""
        with self._lock:
            return BackendStats(
                grammars_compiled=self.stats.grammars_compiled,
                grammars_cached=self.stats.grammars_cached,
                compilations_failed=self.stats.compilations_failed,
                total_compile_time_ms=self.stats.total_compile_time_ms,
                total_tokens_validated=self.stats.total_tokens_validated,
                validation_rejections=self.stats.validation_rejections,
            )


# =============================================================================
# Structured Output Manager
# =============================================================================

class StructuredOutputManager:
    """
    Engine-level manager for structured output constraints.
    
    Features:
    - Multiple backend support with automatic fallback
    - Async grammar compilation via thread pool
    - LRU caching of compiled grammars
    - Batch bitmask allocation and management
    
    Usage:
        manager = StructuredOutputManager(vocab_size=32000)
        manager.register_backend("regex", RegexBackend(...))
        
        grammar = manager.compile_grammar(
            GrammarSpec(GrammarType.JSON, '{"type": "object"}')
        )
        
        # Generate with constraints
        allowed = grammar.get_allowed_tokens()
    """
    
    def __init__(
        self,
        vocab_size: int,
        max_batch_size: int = 256,
        cache_size: int = 1000,
        num_compile_workers: int = 4,
        enable_async: bool = True,
    ):
        self.vocab_size = vocab_size
        self.max_batch_size = max_batch_size
        self.cache_size = cache_size
        self.enable_async = enable_async
        
        # Backends by name
        self._backends: Dict[str, StructuredOutputBackend] = {}
        
        # Grammar type to backend mapping
        self._type_to_backend: Dict[GrammarType, str] = {}
        
        # Compiled grammar cache (LRU)
        self._grammar_cache: Dict[str, StructuredOutputGrammar] = {}
        self._cache_order: List[str] = []
        self._cache_lock = threading.Lock()
        
        # Async compilation
        self._executor = ThreadPoolExecutor(
            max_workers=num_compile_workers,
            thread_name_prefix="grammar_compile",
        ) if enable_async else None
        self._pending_compilations: Dict[str, Future] = {}
        
        # Shared bitmask buffer
        self._bitmask_buffer = np.zeros(
            (max_batch_size, vocab_size), dtype=np.bool_
        )
        
        # Statistics
        self._total_requests = 0
        self._cache_hits = 0
    
    def register_backend(
        self,
        name: str,
        backend: StructuredOutputBackend,
        grammar_types: Optional[List[GrammarType]] = None,
    ) -> None:
        """
        Register a backend for grammar compilation.
        
        Args:
            name: Backend name for identification.
            backend: The backend instance.
            grammar_types: Types this backend handles. If None, uses backend's
                          get_supported_types().
        """
        self._backends[name] = backend
        
        types_to_register = grammar_types or backend.get_supported_types()
        for gtype in types_to_register:
            self._type_to_backend[gtype] = name
    
    def get_backend(
        self,
        grammar_type: GrammarType,
    ) -> Optional[StructuredOutputBackend]:
        """Get the backend for a grammar type."""
        backend_name = self._type_to_backend.get(grammar_type)
        if backend_name:
            return self._backends.get(backend_name)
        return None
    
    def compile_grammar(
        self,
        grammar_spec: GrammarSpec,
        request_id: Optional[str] = None,
        async_compile: bool = False,
    ) -> Union[StructuredOutputGrammar, Future]:
        """
        Compile a grammar specification.
        
        Args:
            grammar_spec: The grammar specification.
            request_id: Optional request identifier.
            async_compile: If True and async enabled, return a Future.
            
        Returns:
            Compiled grammar or Future if async.
        """
        self._total_requests += 1
        cache_key = grammar_spec.to_cache_key()
        
        # Check cache first
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            self._cache_hits += 1
            # Clone for new request
            return self._clone_grammar(cached, request_id)
        
        # Get appropriate backend
        backend = self.get_backend(grammar_spec.grammar_type)
        if backend is None:
            raise ValueError(
                f"No backend registered for grammar type: {grammar_spec.grammar_type}"
            )
        
        # Async compilation
        if async_compile and self._executor is not None:
            if cache_key in self._pending_compilations:
                return self._pending_compilations[cache_key]
            
            future = self._executor.submit(
                self._do_compile, backend, grammar_spec, request_id, cache_key
            )
            self._pending_compilations[cache_key] = future
            return future
        
        # Sync compilation
        return self._do_compile(backend, grammar_spec, request_id, cache_key)
    
    def _do_compile(
        self,
        backend: StructuredOutputBackend,
        grammar_spec: GrammarSpec,
        request_id: Optional[str],
        cache_key: str,
    ) -> StructuredOutputGrammar:
        """Perform grammar compilation."""
        import time
        start = time.perf_counter()
        
        try:
            grammar = backend.compile_grammar(grammar_spec, request_id)
            elapsed_ms = (time.perf_counter() - start) * 1000
            
            # Update stats
            with backend._lock:
                backend.stats.grammars_compiled += 1
                backend.stats.total_compile_time_ms += elapsed_ms
            
            # Cache the grammar
            self._add_to_cache(cache_key, grammar)
            
            return grammar
            
        except Exception as e:
            with backend._lock:
                backend.stats.compilations_failed += 1
            raise
        finally:
            # Remove from pending
            self._pending_compilations.pop(cache_key, None)
    
    def _get_from_cache(self, key: str) -> Optional[StructuredOutputGrammar]:
        """Get grammar from cache with LRU update."""
        with self._cache_lock:
            if key in self._grammar_cache:
                # Move to end (most recently used)
                self._cache_order.remove(key)
                self._cache_order.append(key)
                return self._grammar_cache[key]
        return None
    
    def _add_to_cache(self, key: str, grammar: StructuredOutputGrammar) -> None:
        """Add grammar to cache with LRU eviction."""
        with self._cache_lock:
            if key in self._grammar_cache:
                return
            
            # Evict oldest if at capacity
            while len(self._grammar_cache) >= self.cache_size:
                oldest_key = self._cache_order.pop(0)
                del self._grammar_cache[oldest_key]
            
            self._grammar_cache[key] = grammar
            self._cache_order.append(key)
    
    def _clone_grammar(
        self,
        grammar: StructuredOutputGrammar,
        request_id: Optional[str],
    ) -> StructuredOutputGrammar:
        """Clone a grammar for a new request."""
        # Re-compile to get fresh state
        backend = self.get_backend(grammar.grammar_spec.grammar_type)
        if backend:
            return backend.compile_grammar(grammar.grammar_spec, request_id)
        return grammar
    
    def fill_batch_bitmask(
        self,
        grammars: Sequence[Optional[StructuredOutputGrammar]],
        bitmask: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Fill bitmask for a batch of grammars.
        
        Args:
            grammars: Sequence of grammars, None for unconstrained.
            bitmask: Optional pre-allocated bitmask.
            
        Returns:
            Filled bitmask array.
        """
        batch_size = len(grammars)
        
        if bitmask is None:
            bitmask = self._bitmask_buffer[:batch_size]
        
        # Default: all tokens allowed
        bitmask.fill(True)
        
        for i, grammar in enumerate(grammars):
            if grammar is not None and not grammar.is_terminated():
                grammar.fill_bitmask(bitmask, i)
        
        return bitmask
    
    def validate_and_accept(
        self,
        grammar: StructuredOutputGrammar,
        tokens: Sequence[int],
    ) -> ValidationResult:
        """
        Validate and accept tokens for a grammar.
        
        Args:
            grammar: The grammar instance.
            tokens: Token IDs to validate.
            
        Returns:
            Validation result with acceptance info.
        """
        if grammar.is_terminated():
            return ValidationResult(
                is_valid=False,
                accepted_prefix_length=0,
                error_message="Grammar already terminated",
            )
        
        valid_prefix_len = grammar.validate_tokens(tokens)
        
        if valid_prefix_len == len(tokens):
            grammar.accept_tokens(tokens)
            return ValidationResult(
                is_valid=True,
                accepted_prefix_length=len(tokens),
            )
        else:
            return ValidationResult(
                is_valid=False,
                accepted_prefix_length=valid_prefix_len,
                error_message=f"Rejected at token {valid_prefix_len}",
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        stats = {
            "total_requests": self._total_requests,
            "cache_hits": self._cache_hits,
            "cache_hit_rate": (
                self._cache_hits / self._total_requests 
                if self._total_requests > 0 else 0.0
            ),
            "cache_size": len(self._grammar_cache),
            "pending_compilations": len(self._pending_compilations),
            "backends": {},
        }
        
        for name, backend in self._backends.items():
            stats["backends"][name] = {
                "grammars_compiled": backend.stats.grammars_compiled,
                "grammars_cached": backend.stats.grammars_cached,
                "compilations_failed": backend.stats.compilations_failed,
                "avg_compile_time_ms": (
                    backend.stats.total_compile_time_ms / backend.stats.grammars_compiled
                    if backend.stats.grammars_compiled > 0 else 0.0
                ),
            }
        
        return stats
    
    def clear_cache(self) -> int:
        """Clear the grammar cache. Returns number of items cleared."""
        with self._cache_lock:
            count = len(self._grammar_cache)
            self._grammar_cache.clear()
            self._cache_order.clear()
            return count
    
    def shutdown(self) -> None:
        """Shutdown the manager and thread pool."""
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None


# =============================================================================
# Built-in Grammar Implementations
# =============================================================================

class SimpleRegexGrammar(StructuredOutputGrammar):
    """
    Simple regex-based grammar using Python's re module.
    
    For production use, consider integrating with interegular or outlines
    for proper FSM-based token constraint.
    """
    
    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: Optional[str] = None,
        token_strings: Optional[Dict[int, str]] = None,
    ):
        super().__init__(grammar_spec, vocab_size, request_id)
        
        import re
        self._pattern = re.compile(grammar_spec.spec)
        self._generated_text = ""
        self._token_strings = token_strings or {}
    
    def accept_tokens(self, tokens: Sequence[int]) -> bool:
        for token_id in tokens:
            token_str = self._token_strings.get(token_id, "")
            new_text = self._generated_text + token_str
            
            # Check if still matches partial
            if self._pattern.fullmatch(new_text) or self._is_partial_match(new_text):
                self._state_history.append(self._generated_text)
                self._generated_text = new_text
                self._tokens_accepted += 1
                
                # Check for termination
                if self._pattern.fullmatch(self._generated_text):
                    self._is_terminated = True
            else:
                return False
        
        return True
    
    def _is_partial_match(self, text: str) -> bool:
        """Check if text could still match the pattern with more characters."""
        try:
            return self._pattern.match(text) is not None
        except Exception:
            return False
    
    def validate_tokens(self, tokens: Sequence[int]) -> int:
        """Validate without accepting."""
        temp_text = self._generated_text
        
        for i, token_id in enumerate(tokens):
            token_str = self._token_strings.get(token_id, "")
            new_text = temp_text + token_str
            
            if not (self._pattern.fullmatch(new_text) or self._is_partial_match(new_text)):
                return i
            
            temp_text = new_text
        
        return len(tokens)
    
    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        """Fill bitmask - simple implementation allows all tokens."""
        # A proper implementation would use FSM to determine allowed tokens
        # For now, we allow all and rely on validate_tokens
        bitmask[batch_index, :] = True
    
    def get_allowed_tokens(self) -> List[int]:
        """Get allowed tokens - returns all for simple implementation."""
        return list(range(self.vocab_size))


class ChoiceGrammar(StructuredOutputGrammar):
    """Grammar for choosing from a fixed set of options."""
    
    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: Optional[str] = None,
        token_strings: Optional[Dict[int, str]] = None,
        encode_fn: Optional[Callable[[str], List[int]]] = None,
    ):
        super().__init__(grammar_spec, vocab_size, request_id)
        
        # Parse choices from spec (JSON list)
        self._choices: List[str] = json.loads(grammar_spec.spec)
        self._token_strings = token_strings or {}
        self._encode_fn = encode_fn
        
        self._generated_text = ""
        self._valid_choices: List[str] = list(self._choices)
        
        # Pre-compute allowed token sets for each prefix
        self._allowed_tokens_cache: Dict[str, set] = {}
    
    def accept_tokens(self, tokens: Sequence[int]) -> bool:
        for token_id in tokens:
            token_str = self._token_strings.get(token_id, "")
            new_text = self._generated_text + token_str
            
            # Filter valid choices
            new_valid = [c for c in self._valid_choices if c.startswith(new_text)]
            
            if not new_valid:
                return False
            
            self._state_history.append((self._generated_text, self._valid_choices.copy()))
            self._generated_text = new_text
            self._valid_choices = new_valid
            self._tokens_accepted += 1
            
            # Check for exact match (termination)
            if new_text in self._choices:
                self._is_terminated = True
        
        return True
    
    def validate_tokens(self, tokens: Sequence[int]) -> int:
        temp_text = self._generated_text
        temp_valid = list(self._valid_choices)
        
        for i, token_id in enumerate(tokens):
            token_str = self._token_strings.get(token_id, "")
            new_text = temp_text + token_str
            
            new_valid = [c for c in temp_valid if c.startswith(new_text)]
            if not new_valid:
                return i
            
            temp_text = new_text
            temp_valid = new_valid
        
        return len(tokens)
    
    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        """Fill bitmask based on valid continuations."""
        allowed = self._compute_allowed_tokens()
        bitmask[batch_index, :] = False
        for token_id in allowed:
            if token_id < bitmask.shape[1]:
                bitmask[batch_index, token_id] = True
    
    def get_allowed_tokens(self) -> List[int]:
        return list(self._compute_allowed_tokens())
    
    def _compute_allowed_tokens(self) -> set:
        """Compute allowed tokens based on current state."""
        cache_key = self._generated_text
        if cache_key in self._allowed_tokens_cache:
            return self._allowed_tokens_cache[cache_key]
        
        allowed = set()
        
        for choice in self._valid_choices:
            if len(choice) > len(self._generated_text):
                # Get next character
                next_char = choice[len(self._generated_text)]
                
                # Find tokens that start with this character
                for token_id, token_str in self._token_strings.items():
                    if token_str and token_str[0] == next_char:
                        allowed.add(token_id)
        
        self._allowed_tokens_cache[cache_key] = allowed
        return allowed
    
    def rollback(self, num_tokens: int) -> None:
        """Rollback with state restoration."""
        for _ in range(min(num_tokens, len(self._state_history))):
            if self._state_history:
                self._generated_text, self._valid_choices = self._state_history.pop()
                self._tokens_accepted -= 1
        
        self._is_terminated = False


# =============================================================================
# Simple Backend Implementation
# =============================================================================

class SimpleBackend(StructuredOutputBackend):
    """
    Simple backend implementation for basic grammar types.
    
    Supports:
    - REGEX: Regular expression patterns
    - CHOICE: Fixed choice selection
    """
    
    def __init__(
        self,
        vocab_size: int,
        tokenizer_encode: Optional[Callable[[str], List[int]]] = None,
        tokenizer_decode: Optional[Callable[[List[int]], str]] = None,
        token_strings: Optional[Dict[int, str]] = None,
    ):
        super().__init__(vocab_size, tokenizer_encode, tokenizer_decode)
        self._token_strings = token_strings or {}
    
    def compile_grammar(
        self,
        grammar_spec: GrammarSpec,
        request_id: Optional[str] = None,
    ) -> StructuredOutputGrammar:
        if grammar_spec.grammar_type == GrammarType.REGEX:
            return SimpleRegexGrammar(
                grammar_spec=grammar_spec,
                vocab_size=self.vocab_size,
                request_id=request_id,
                token_strings=self._token_strings,
            )
        elif grammar_spec.grammar_type == GrammarType.CHOICE:
            return ChoiceGrammar(
                grammar_spec=grammar_spec,
                vocab_size=self.vocab_size,
                request_id=request_id,
                token_strings=self._token_strings,
                encode_fn=self.tokenizer_encode,
            )
        else:
            raise ValueError(f"Unsupported grammar type: {grammar_spec.grammar_type}")
    
    def get_supported_types(self) -> List[GrammarType]:
        return [GrammarType.REGEX, GrammarType.CHOICE]
