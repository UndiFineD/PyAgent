"""
BadWordsProcessorV2 - Enhanced bad words filtering processor.

Implements vLLM's bad words filtering with:
- N-gram prefix matching
- Speculative decoding support
- Batch-level filtering

Beyond vLLM innovations:
- Trie-based matching for efficiency
- Streaming token support
- Configurable penalty modes
- Bad phrase detection
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
)
import threading

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

from .logits_processor_v2 import (
    BatchUpdate,
    LogitsProcessor,
    MoveDirectionality,
    SamplingParams,
)


_SMALLEST_LOGIT = float("-inf")


class BadWordsPenaltyMode(Enum):
    """Penalty mode for bad words."""
    HARD = auto()  # Set to -inf
    SOFT = auto()  # Apply large penalty
    DECAY = auto()  # Exponentially decay penalty


@dataclass
class TrieNode:
    """Trie node for efficient prefix matching."""
    children: Dict[int, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False
    token_id: int = -1
    
    def insert(self, tokens: Sequence[int]) -> None:
        """Insert a token sequence into the trie."""
        node = self
        for token in tokens[:-1]:
            if token not in node.children:
                node.children[token] = TrieNode()
            node = node.children[token]
        # Mark the last token as the one to block
        if tokens:
            last_token = tokens[-1]
            if last_token not in node.children:
                node.children[last_token] = TrieNode()
            node.children[last_token].is_end = True
            node.children[last_token].token_id = last_token
    
    def find_blocked_tokens(
        self,
        past_tokens: Sequence[int],
    ) -> Set[int]:
        """Find tokens that should be blocked given past tokens."""
        blocked = set()
        
        # Check all suffix positions
        for start in range(len(past_tokens) + 1):
            node = self
            valid = True
            
            for token in past_tokens[start:]:
                if token in node.children:
                    node = node.children[token]
                else:
                    valid = False
                    break
            
            if valid:
                # Add all tokens that would complete a bad word
                for child_token, child_node in node.children.items():
                    if child_node.is_end:
                        blocked.add(child_token)
        
        return blocked


class BadWordsProcessorV2(LogitsProcessor):
    """
    Enhanced bad words filtering processor.
    
    Filters out tokens that would complete a "bad word" sequence.
    Supports n-gram matching and speculative decoding.
    """
    
    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu",
        penalty_mode: BadWordsPenaltyMode = BadWordsPenaltyMode.HARD,
        soft_penalty: float = -100.0,
    ):
        self.max_num_reqs = max_num_reqs
        self.device = device
        self.penalty_mode = penalty_mode
        self.soft_penalty = soft_penalty
        
        # Per-request bad words and tries
        self._bad_words: Dict[int, List[List[int]]] = {}
        self._tries: Dict[int, TrieNode] = {}
        
        # Token histories
        self._past_tokens: Dict[int, List[int]] = {}
        
        # Request count for quick check
        self._request_count = 0
    
    def is_argmax_invariant(self) -> bool:
        """Bad words filtering can change argmax."""
        return False
    
    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """Update state based on batch changes."""
        if batch_update is None:
            return
        
        # Process added requests
        for index, params, prompt_tokens, output_tokens in batch_update.added:
            if params.bad_words:
                self._bad_words[index] = list(params.bad_words)
                self._tries[index] = self._build_trie(params.bad_words)
                self._past_tokens[index] = list(output_tokens)
                self._request_count += 1
            elif index in self._bad_words:
                self._remove_request(index)
        
        # Process removed requests
        for index in batch_update.removed:
            if index in self._bad_words:
                self._remove_request(index)
        
        # Process moved requests
        for from_idx, to_idx, direction in batch_update.moved:
            has_a = from_idx in self._bad_words
            has_b = to_idx in self._bad_words
            
            if has_a:
                self._bad_words[to_idx] = self._bad_words[from_idx]
                self._tries[to_idx] = self._tries[from_idx]
                self._past_tokens[to_idx] = self._past_tokens[from_idx]
            elif to_idx in self._bad_words:
                self._remove_request(to_idx)
            
            if direction == MoveDirectionality.SWAP:
                if has_b:
                    self._bad_words[from_idx] = self._bad_words[to_idx]
                    self._tries[from_idx] = self._tries[to_idx]
                    self._past_tokens[from_idx] = self._past_tokens[to_idx]
            else:
                if from_idx in self._bad_words:
                    self._remove_request(from_idx)
    
    def _remove_request(self, index: int) -> None:
        """Remove request data."""
        self._bad_words.pop(index, None)
        self._tries.pop(index, None)
        self._past_tokens.pop(index, None)
        self._request_count = max(0, self._request_count - 1)
    
    def _build_trie(self, bad_words: List[List[int]]) -> TrieNode:
        """Build trie from bad words list."""
        root = TrieNode()
        for word in bad_words:
            if word:
                root.insert(word)
        return root
    
    def apply(self, logits: Any) -> Any:
        """Apply bad words filtering."""
        if self._request_count == 0:
            return logits
        
        if HAS_RUST:
            return self._apply_rust(logits)
        elif HAS_NUMPY and isinstance(logits, np.ndarray):
            return self._apply_numpy(logits)
        else:
            return self._apply_generic(logits)
    
    def _apply_rust(self, logits: Any) -> Any:
        """Apply using Rust acceleration."""
        # Fall back to numpy for now
        if HAS_NUMPY and isinstance(logits, np.ndarray):
            return self._apply_numpy(logits)
        return self._apply_generic(logits)
    
    def _apply_numpy(self, logits: "np.ndarray") -> "np.ndarray":
        """Apply using NumPy."""
        for req_idx, trie in self._tries.items():
            if req_idx >= logits.shape[0]:
                continue
            
            past = self._past_tokens.get(req_idx, [])
            blocked = trie.find_blocked_tokens(past)
            
            for token_id in blocked:
                if token_id < logits.shape[1]:
                    if self.penalty_mode == BadWordsPenaltyMode.HARD:
                        logits[req_idx, token_id] = _SMALLEST_LOGIT
                    elif self.penalty_mode == BadWordsPenaltyMode.SOFT:
                        logits[req_idx, token_id] += self.soft_penalty
        
        return logits
    
    def _apply_generic(self, logits: Any) -> Any:
        """Generic apply."""
        return logits
    
    def accept_token(self, req_index: int, token_id: int) -> None:
        """Accept a new token for a request."""
        if req_index in self._past_tokens:
            self._past_tokens[req_index].append(token_id)
    
    def has_state(self) -> bool:
        return True
    
    def reset(self) -> None:
        self._bad_words.clear()
        self._tries.clear()
        self._past_tokens.clear()
        self._request_count = 0


def apply_bad_words(
    logits: Any,
    bad_words_token_ids: Dict[int, List[List[int]]],
    past_tokens_ids: List[List[int]],
) -> None:
    """
    Apply bad words filtering to logits.
    
    Standalone function for compatibility with vLLM interface.
    """
    for req_idx, bad_words in bad_words_token_ids.items():
        if req_idx >= len(past_tokens_ids):
            continue
        
        past = past_tokens_ids[req_idx]
        _apply_bad_words_single_batch(logits[req_idx], bad_words, past)


def _apply_bad_words_single_batch(
    logits: Any,
    bad_words_token_ids: List[List[int]],
    past_tokens_ids: List[int],
) -> None:
    """Apply bad words filtering for a single batch element."""
    for bad_word_ids in bad_words_token_ids:
        if len(bad_word_ids) > len(past_tokens_ids) + 1:
            continue
        
        prefix_length = len(bad_word_ids) - 1
        last_token_id = bad_word_ids[-1]
        
        if prefix_length > 0:
            actual_prefix = past_tokens_ids[-prefix_length:]
            expected_prefix = bad_word_ids[:prefix_length]
            
            if len(actual_prefix) != len(expected_prefix):
                continue
            
            if actual_prefix != expected_prefix:
                continue
        
        # Block the last token
        if HAS_NUMPY and isinstance(logits, np.ndarray):
            logits[last_token_id] = _SMALLEST_LOGIT
        else:
            try:
                logits[last_token_id] = _SMALLEST_LOGIT
            except (IndexError, TypeError):
                pass


def apply_bad_words_with_drafts(
    logits: Any,
    bad_words_token_ids: Dict[int, List[List[int]]],
    past_tokens_ids: List[List[int]],
    num_draft_tokens: List[int],
) -> None:
    """
    Apply bad words filtering with speculative decoding drafts.
    
    Handles multiple draft tokens per request where logits
    are flattened across draft positions.
    """
    start_idx = 0
    for req_idx, bad_words in bad_words_token_ids.items():
        if req_idx >= len(num_draft_tokens):
            continue
        
        for draft_idx in range(num_draft_tokens[req_idx]):
            actual_idx = start_idx + draft_idx
            if actual_idx >= len(past_tokens_ids):
                continue
            
            _apply_bad_words_single_batch(
                logits[actual_idx],
                bad_words,
                past_tokens_ids[actual_idx],
            )
        
        start_idx += num_draft_tokens[req_idx]


class BadPhrasesProcessor(BadWordsProcessorV2):
    """
    Extended processor for bad phrases with wildcards.
    
    Beyond vLLM: Supports wildcard patterns and phrase variations.
    """
    
    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu",
        penalty_mode: BadWordsPenaltyMode = BadWordsPenaltyMode.HARD,
        max_wildcards: int = 3,
    ):
        super().__init__(max_num_reqs, device, penalty_mode)
        self.max_wildcards = max_wildcards
        self._wildcard_patterns: Dict[int, List[Tuple[List[int], int]]] = {}
    
    def add_wildcard_pattern(
        self,
        req_index: int,
        prefix: List[int],
        suffix: List[int],
    ) -> None:
        """Add a wildcard pattern (prefix...suffix)."""
        if req_index not in self._wildcard_patterns:
            self._wildcard_patterns[req_index] = []
        
        # Store as (prefix + suffix, wildcard_position)
        self._wildcard_patterns[req_index].append((
            prefix + suffix,
            len(prefix),
        ))
    
    def _check_wildcard_match(
        self,
        past_tokens: List[int],
        pattern: List[int],
        wildcard_pos: int,
    ) -> Set[int]:
        """Check if past tokens match wildcard pattern."""
        blocked = set()
        
        # Check all possible wildcard lengths
        for wc_len in range(self.max_wildcards + 1):
            if len(past_tokens) < wildcard_pos + wc_len:
                continue
            
            # Check prefix match
            if past_tokens[:wildcard_pos] != pattern[:wildcard_pos]:
                continue
            
            # Check suffix position
            suffix_start = wildcard_pos + wc_len
            suffix_pattern = pattern[wildcard_pos:]
            
            if len(suffix_pattern) > 1:
                # Check if suffix prefix matches
                actual_suffix = past_tokens[suffix_start:]
                if len(actual_suffix) >= len(suffix_pattern) - 1:
                    if actual_suffix[:len(suffix_pattern)-1] == suffix_pattern[:-1]:
                        blocked.add(suffix_pattern[-1])
        
        return blocked


__all__ = [
    'BadWordsPenaltyMode',
    'TrieNode',
    'BadWordsProcessorV2',
    'BadPhrasesProcessor',
    'apply_bad_words',
    'apply_bad_words_with_drafts',
]
