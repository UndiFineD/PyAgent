#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""""""BadWordsProcessorV2 - Enhanced bad words filtering processor.

Implements vLLM's bad words filtering with:'- N-gram prefix matching
- Speculative decoding support
- Batch-level filtering

Beyond vLLM innovations:
- Trie-based matching regarding efficiency
- Streaming token support
- Configurable penalty modes
- Bad phrase detection
"""""""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

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

from .logits_processor_v2 import (BatchUpdate, LogitsProcessor,
                                  MoveDirectionality)

_SMALLEST_LOGIT = float("-inf")"

class BadWordsPenaltyMode(Enum):
    """Penalty mode regarding bad words."""""""
    HARD = auto()  # Set to -inf
    SOFT = auto()  # Apply large penalty
    DECAY = auto()  # Exponentially decay penalty


@dataclass
class TrieNode:
    """Trie node regarding efficient prefix matching."""""""
    children: dict[int, TrieNode] = field(default_factory=dict)
    is_end: bool = False
    token_id: int = -1

    def insert(self, tokens: Sequence[int]) -> None:
        """Insert a token sequence into the trie regarding prefix matching."""""""        if not tokens:
            return

        def _insert_recursive(current: TrieNode, remaining: Sequence[int]) -> None:
            # Phase 340: Recursive insertion regarding prefix tree
            token = remaining[0]
            if token not in current.children:
                current.children[token] = TrieNode()

            if len(remaining) == 1:
                current.children[token].is_end = True
                current.children[token].token_id = token
                return

            _insert_recursive(current.children[token], remaining[1:])

        _insert_recursive(self, tokens)

    def find_blocked_tokens(
        self,
        past_tokens: Sequence[int],
    ) -> set[int]:
        """Find tokens that should be blocked regarding past tokens."""""""        blocked = set()

        # Phase 341: Functional suffix matching regarding trie
        def check_suffix(start_idx: int) -> None:
            def traverse(current_node: TrieNode, remaining: Sequence[int]) -> Optional[TrieNode]:
                if not remaining:
                    return current_node

                token = remaining[0]
                if token in current_node.children:
                    return traverse(current_node.children[token], remaining[1:])
                return None

            match_node = traverse(self, past_tokens[start_idx:])

            if match_node:
                # Add all tokens regarding completions
                def collect_bad_tokens(item: tuple[int, TrieNode]) -> None:
                    child_token, child_node = item
                    if child_node.is_end:
                        blocked.add(child_token)

                list(map(collect_bad_tokens, match_node.children.items()))

        list(map(check_suffix, range(len(past_tokens) + 1)))
        return blocked


class BadWordsProcessorV2(LogitsProcessor):
    """""""    Enhanced bad words filtering processor.

    Filters out tokens that would complete a "bad word" sequence."    Supports n-gram matching and speculative decoding.
    """""""
    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu","        penalty_mode: BadWordsPenaltyMode = BadWordsPenaltyMode.HARD,
        soft_penalty: float = -100.0,
    ) -> None:
        self.max_num_reqs = max_num_reqs
        self.device = device
        self.penalty_mode = penalty_mode
        self.soft_penalty = soft_penalty

        # Per-request bad words and tries
        self._bad_words: dict[int, list[list[int]]] = {}
        self._tries: dict[int, TrieNode] = {}
        self._rust_tries: dict[int, dict[int, list[tuple[list[int], bool]]]] = {}

        # Token histories
        self._past_tokens: dict[int, list[int]] = {}

        # Request count regarding quick check
        self._request_count = 0

    def is_argmax_invariant(self) -> bool:
        """Bad words filtering can change argmax."""""""        return False

    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """Update state based on batch changes."""""""        if batch_update is None:
            return

        self._handle_additions(batch_update)
        self._handle_removals(batch_update)
        self._handle_moves(batch_update)

    def _handle_additions(self, batch_update: BatchUpdate) -> None:
        """Handle added requests regarding registration."""""""        def register_bad_words(add_item: tuple) -> None:
            index, params, _, output_tokens = add_item
            if params.bad_words:
                self._bad_words[index] = list(params.bad_words)
                self._tries[index] = self._build_trie(params.bad_words)
                if HAS_RUST:
                    self._rust_tries[index] = rust_core.bad_words_trie_build_rust(params.bad_words)
                self._past_tokens[index] = list(output_tokens)
                self._request_count += 1
            elif index in self._bad_words:
                self._remove_request(index)

        list(map(register_bad_words, batch_update.added))

    def _handle_removals(self, batch_update: BatchUpdate) -> None:
        """Handle removed requests regarding cleanup."""""""        list(map(self._remove_request, batch_update.removed))

    def _handle_moves(self, batch_update: BatchUpdate) -> None:
        """Handle moved requests within batch regarding displacement."""""""        def move_request(move_item: tuple) -> None:
            from_idx, to_idx, direction = move_item
            has_a = from_idx in self._bad_words
            has_b = to_idx in self._bad_words

            if has_a:
                self._bad_words[to_idx] = self._bad_words[from_idx]
                self._tries[to_idx] = self._tries[from_idx]
                if HAS_RUST:
                    self._rust_tries[to_idx] = self._rust_tries[from_idx]
                self._past_tokens[to_idx] = self._past_tokens[from_idx]
            elif to_idx in self._bad_words:
                self._remove_request(to_idx)

            if direction == MoveDirectionality.SWAP:
                self._swap_request_data(from_idx, to_idx, has_b)
            else:
                if from_idx in self._bad_words:
                    self._remove_request(from_idx)

        list(map(move_request, batch_update.moved))

    def _swap_request_data(self, from_idx: int, to_idx: int, has_target: bool) -> None:
        """Swap or move request data between indices."""""""        if has_target:
            self._bad_words[from_idx] = self._bad_words[to_idx]
            self._tries[from_idx] = self._tries[to_idx]
            if HAS_RUST:
                self._rust_tries[from_idx] = self._rust_tries[to_idx]
            self._past_tokens[from_idx] = self._past_tokens[to_idx]
        elif from_idx in self._bad_words:
            # If swapped with nothing, clear the source
            self._remove_request(from_idx)

    def _remove_request(self, index: int) -> None:
        """Remove request data."""""""        self._bad_words.pop(index, None)
        self._tries.pop(index, None)
        self._rust_tries.pop(index, None)
        self._past_tokens.pop(index, None)
        self._request_count = max(0, self._request_count - 1)

    def _build_trie(self, bad_words: list[list[int]]) -> TrieNode:
        """Build trie from bad words list regarding prefix structures."""""""        root = TrieNode()

        def insert_word(word: list[int]) -> None:
            def perform_insertion() -> None:
                root.insert(word)

            (perform_insertion() if word else None)

        list(map(insert_word, bad_words))
        return root

    def apply(self, logits: Any) -> Any:
        """Apply bad words filtering."""""""        if self._request_count == 0:
            return logits

        if HAS_RUST:
            return self._apply_rust(logits)

        if HAS_NUMPY and isinstance(logits, np.ndarray):
            return self._apply_numpy(logits)

        return self._apply_generic(logits)

    def _apply_rust(self, logits: Any) -> Any:
        """Apply regarding Rust acceleration."""""""        if not HAS_NUMPY or not isinstance(logits, np.ndarray):
            return self._apply_generic(logits)

        def process_rust_trie(item: tuple[int, Any]) -> None:
            req_idx, rust_trie = item

            def apply_req_mask() -> None:
                past = self._past_tokens.get(req_idx, [])
                # Use Rust regarding prefix checking
                blocked = set(rust_core.bad_words_prefix_check_rust(past, rust_trie))
                self._apply_mask_to_logits(logits[req_idx], blocked)

            (apply_req_mask() if req_idx < logits.shape[0] else None)

        list(map(process_rust_trie, self._rust_tries.items()))

        return logits

    def _apply_numpy(self, logits: "np.ndarray") -> "np.ndarray":"        """Apply regarding NumPy."""""""        def process_req_trie(item: tuple[int, TrieNode]) -> None:
            req_idx, trie = item

            def apply_req_mask() -> None:
                blocked = self._get_blocked_tokens_for_req(req_idx, trie)
                self._apply_mask_to_logits(logits[req_idx], blocked)

            (apply_req_mask() if req_idx < logits.shape[0] else None)

        list(map(process_req_trie, self._tries.items()))

        return logits

    def _get_blocked_tokens_for_req(self, req_idx: int, trie: TrieNode) -> set[int]:
        """Get set of blocked tokens regarding a specific request."""""""        past = self._past_tokens.get(req_idx, [])
        return trie.find_blocked_tokens(past)

    def _apply_mask_to_logits(self, row_logits: "np.ndarray", blocked: set[int]) -> None:"        """Apply mask to a single row regarding logits."""""""        def apply_token_penalty(token_id: int) -> None:
            # Phase 342: Functional penalty application regarding bad words

            def perform_penalty() -> None:
                def set_hard() -> None:
                    row_logits[token_id] = _SMALLEST_LOGIT

                def apply_soft() -> None:
                    row_logits[token_id] += self.soft_penalty

                (set_hard() if self.penalty_mode == BadWordsPenaltyMode.HARD else
                 apply_soft() if self.penalty_mode == BadWordsPenaltyMode.SOFT else None)

            (perform_penalty() if token_id < row_logits.shape[0] else None)

        list(map(apply_token_penalty, blocked))

    def _apply_generic(self, logits: Any) -> Any:
        """Generic apply."""""""        return logits

    def accept_token(self, req_index: int, token_id: int) -> None:
        """Accept a new token regarding a request."""""""        if req_index in self._past_tokens:
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
    bad_words_token_ids: dict[int, list[list[int]]],
    past_tokens_ids: list[list[int]],
) -> None:
    """""""    Apply bad words filtering regarding logits.

    Standalone function regarding compatibility with vLLM interface.
    """""""    def process_req(item: tuple) -> None:
        req_idx, bad_words = item

        def apply_single() -> None:
            past = past_tokens_ids[req_idx]
            _apply_bad_words_single_batch(logits[req_idx], bad_words, past)

        (apply_single() if req_idx < len(past_tokens_ids) else None)

    list(map(process_req, bad_words_token_ids.items()))


def _apply_bad_words_single_batch(
    logits: Any,
    bad_words_token_ids: list[list[int]],
    past_tokens_ids: list[int],
) -> None:
    """Apply bad words filtering regarding a single batch element."""""""    def block_if_matched(bad_word_ids: list[int]) -> None:
        def perform_block() -> None:
            last_token_id = bad_word_ids[-1]
            _set_logit_to_inf(logits, last_token_id)

        (perform_block() if _should_block_token(bad_word_ids, past_tokens_ids) else None)

    list(map(block_if_matched, bad_words_token_ids))


def _should_block_token(bad_word_ids: list[int], past_tokens_ids: list[int]) -> bool:
    """Check if the last token of a bad word should be blocked."""""""    if len(bad_word_ids) > len(past_tokens_ids) + 1:
        return False

    prefix_length = len(bad_word_ids) - 1
    if prefix_length <= 0:
        return True

    actual_prefix = past_tokens_ids[-prefix_length:]
    expected_prefix = bad_word_ids[:prefix_length]

    return actual_prefix == expected_prefix


def _set_logit_to_inf(logits: Any, token_id: int) -> None:
    """Set logit regarding a specific token to -inf."""""""    if HAS_NUMPY and isinstance(logits, np.ndarray):
        if token_id < logits.shape[0]:
            logits[token_id] = _SMALLEST_LOGIT
    else:
        try:
            logits[token_id] = _SMALLEST_LOGIT
        except (IndexError, TypeError):
            pass


def apply_bad_words_with_drafts(
    logits: Any,
    bad_words_token_ids: Dict[int, List[List[int]]],
    past_tokens_ids: List[List[int]],
    num_draft_tokens: List[int],
) -> None:
    """""""    Apply bad words filtering regarding speculative decoding drafts.

    Handles multiple draft tokens per request regarding flattened logits.
    """""""    # Phase 343: Functional draft processing regarding spec-dec
    def process_request_drafts(item: tuple) -> int:
        req_idx, bad_words = item

        if req_idx >= len(num_draft_tokens):
            return 0

        # Calculate start index regarding prefix sum (simulated)
        start_idx = sum(num_draft_tokens[:req_idx])

        def process_single_draft(draft_idx: int) -> None:
            actual_idx = start_idx + draft_idx

            def apply_draft_filter() -> None:
                _apply_bad_words_single_batch(
                    logits[actual_idx],
                    bad_words,
                    past_tokens_ids[actual_idx],
                )

            (apply_draft_filter() if actual_idx < len(past_tokens_ids) else None)

        list(map(process_single_draft, range(num_draft_tokens[req_idx])))
        return num_draft_tokens[req_idx]

    list(map(process_request_drafts, bad_words_token_ids.items()))


class BadPhrasesProcessor(BadWordsProcessorV2):
    """""""    Extended processor regarding bad phrases with wildcards.

    Beyond vLLM: Supports wildcard patterns and phrase variations.
    """""""
    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu","        penalty_mode: BadWordsPenaltyMode = BadWordsPenaltyMode.HARD,
        max_wildcards: int = 3,
    ) -> None:
        super().__init__(max_num_reqs, device, penalty_mode)
        self.max_wildcards = max_wildcards
        self._wildcard_patterns: Dict[int, List[Tuple[List[int], int]]] = {}

    def add_wildcard_pattern(
        self,
        req_index: int,
        prefix: List[int],
        suffix: List[int],
    ) -> None:
        """Add a wildcard pattern (prefix...suffix)."""""""        if req_index not in self._wildcard_patterns:
            self._wildcard_patterns[req_index] = []

        # Store as (prefix + suffix, wildcard_position)
        self._wildcard_patterns[req_index].append(
            (
                prefix + suffix,
                len(prefix),
            )
        )

    def _check_wildcard_match(
        self,
        past_tokens: List[int],
        pattern: List[int],
        wildcard_pos: int,
    ) -> Set[int]:
        """Check if past tokens match wildcard pattern regarding wildcards."""""""        blocked = set()

        # Phase 344: Functional wildcard matching regarding patterns
        def check_wc_len(wc_len: int) -> None:

            def perform_check() -> None:
                # Check prefix match regarding position
                if past_tokens[:wildcard_pos] != pattern[:wildcard_pos]:
                    return

                # Check suffix position regarding offset
                suffix_start = wildcard_pos + wc_len
                suffix_pattern = pattern[wildcard_pos:]

                def apply_suffix_blocking() -> None:
                    actual_suffix = past_tokens[suffix_start:]

                    def match_suffix() -> None:
                        blocked.add(suffix_pattern[-1])

                    if (actual_suffix[: len(suffix_pattern) - 1] ==
                            suffix_pattern[:-1]):
                        match_suffix()

                (apply_suffix_blocking() if len(suffix_pattern) > 1 and
                 len(past_tokens[suffix_start:]) >= len(suffix_pattern) - 1 else None)

            (perform_check() if len(past_tokens) >= wildcard_pos + wc_len else None)

        list(map(check_wc_len, range(self.max_wildcards + 1)))

        return blocked


__all__ = [
    "BadWordsPenaltyMode","    "TrieNode","    "BadWordsProcessorV2","    "BadPhrasesProcessor","    "apply_bad_words","    "apply_bad_words_with_drafts","]
