from __future__ import annotations
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import numpy as np
from .config import GrammarType, GrammarSpec, ValidationResult
from .base import StructuredOutputGrammar, StructuredOutputBackend
from .impl import SimpleRegexGrammar, ChoiceGrammar

class StructuredOutputManager:
    """
    Engine-level manager for structured output constraints.
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

        self._backends: Dict[str, StructuredOutputBackend] = {}
        self._type_to_backend: Dict[GrammarType, str] = {}

        self._grammar_cache: Dict[str, StructuredOutputGrammar] = {}
        self._cache_order: List[str] = []
        self._cache_lock = threading.Lock()

        self._executor = ThreadPoolExecutor(
            max_workers=num_compile_workers,
            thread_name_prefix="grammar_compile",
        ) if enable_async else None
        self._pending_compilations: Dict[str, Future] = {}

        self._bitmask_buffer = np.zeros(
            (max_batch_size, vocab_size), dtype=np.bool_
        )

        self._total_requests = 0
        self._cache_hits = 0

    def register_backend(
        self,
        name: str,
        backend: StructuredOutputBackend,
        grammar_types: Optional[List[GrammarType]] = None,
    ) -> None:
        self._backends[name] = backend

        types_to_register = grammar_types or backend.get_supported_types()
        for gtype in types_to_register:
            self._type_to_backend[gtype] = name

    def get_backend(
        self,
        grammar_type: GrammarType,
    ) -> Optional[StructuredOutputBackend]:
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
        self._total_requests += 1
        cache_key = grammar_spec.to_cache_key()

        cached = self._get_from_cache(cache_key)
        if cached is not None:
            self._cache_hits += 1
            return self._clone_grammar(cached, request_id)

        backend = self.get_backend(grammar_spec.grammar_type)
        if backend is None:
            raise ValueError(
                f"No backend registered for grammar type: {grammar_spec.grammar_type}"
            )

        if async_compile and self._executor is not None:
            if cache_key in self._pending_compilations:
                return self._pending_compilations[cache_key]

            future = self._executor.submit(
                self._do_compile, backend, grammar_spec, request_id, cache_key
            )
            self._pending_compilations[cache_key] = future
            return future

        return self._do_compile(backend, grammar_spec, request_id, cache_key)

    def _do_compile(
        self,
        backend: StructuredOutputBackend,
        grammar_spec: GrammarSpec,
        request_id: Optional[str],
        cache_key: str,
    ) -> StructuredOutputGrammar:
        import time
        start = time.perf_counter()

        try:
            grammar = backend.compile_grammar(grammar_spec, request_id)
            elapsed_ms = (time.perf_counter() - start) * 1000

            with backend._lock:
                backend.stats.grammars_compiled += 1
                backend.stats.total_compile_time_ms += elapsed_ms

            self._add_to_cache(cache_key, grammar)
            return grammar
        except Exception:
            with backend._lock:
                backend.stats.compilations_failed += 1
            raise
        finally:
            self._pending_compilations.pop(cache_key, None)

    def _get_from_cache(self, key: str) -> Optional[StructuredOutputGrammar]:
        with self._cache_lock:
            if key in self._grammar_cache:
                self._cache_order.remove(key)
                self._cache_order.append(key)
                return self._grammar_cache[key]
        return None

    def _add_to_cache(self, key: str, grammar: StructuredOutputGrammar) -> None:
        with self._cache_lock:
            if key in self._grammar_cache:
                return

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
        backend = self.get_backend(grammar.grammar_spec.grammar_type)
        if backend:
            return backend.compile_grammar(grammar.grammar_spec, request_id)
        return grammar

    def fill_batch_bitmask(
        self,
        grammars: Sequence[Optional[StructuredOutputGrammar]],
        bitmask: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        batch_size = len(grammars)

        if bitmask is None:
            bitmask = self._bitmask_buffer[:batch_size]

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
                "avg_compile_time_ms": (
                    backend.stats.total_compile_time_ms / backend.stats.grammars_compiled
                    if backend.stats.grammars_compiled > 0 else 0.0
                ),
            }
        return stats

    def shutdown(self) -> None:
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None

class SimpleBackend(StructuredOutputBackend):
    """
    Simple backend implementation for basic grammar types.
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
