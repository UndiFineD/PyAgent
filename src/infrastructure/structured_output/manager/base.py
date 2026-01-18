from __future__ import annotations
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, Sequence
import numpy as np
from .config import GrammarSpec, BackendStats, GrammarType

class StructuredOutputGrammar(ABC):
    """
    Abstract base class for grammar instances.
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
        pass
    
    @abstractmethod
    def validate_tokens(self, tokens: Sequence[int]) -> int:
        pass
    
    @abstractmethod
    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        pass
    
    @abstractmethod
    def get_allowed_tokens(self) -> List[int]:
        pass
    
    def rollback(self, num_tokens: int) -> None:
        if num_tokens <= 0:
            return
        
        rollback_count = min(num_tokens, len(self._state_history))
        for _ in range(rollback_count):
            if self._state_history:
                self._state_history.pop()
        
        self._tokens_accepted = max(0, self._tokens_accepted - rollback_count)
        self._is_terminated = False
    
    def is_terminated(self) -> bool:
        return self._is_terminated
    
    def reset(self) -> None:
        self._is_terminated = False
        self._tokens_accepted = 0
        self._state_history.clear()

class StructuredOutputBackend(ABC):
    """
    Abstract backend for grammar compilation and management.
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
        pass
    
    @abstractmethod
    def get_supported_types(self) -> List[GrammarType]:
        pass
    
    def allocate_token_bitmask(
        self,
        max_batch_size: int,
    ) -> np.ndarray:
        return np.zeros((max_batch_size, self.vocab_size), dtype=np.bool_)
    
    def get_stats(self) -> BackendStats:
        with self._lock:
            return BackendStats(
                grammars_compiled=self.stats.grammars_compiled,
                grammars_cached=self.stats.grammars_cached,
                compilations_failed=self.stats.compilations_failed,
                total_compile_time_ms=self.stats.total_compile_time_ms,
                total_tokens_validated=self.stats.total_tokens_validated,
                validation_rejections=self.stats.validation_rejections,
            )
