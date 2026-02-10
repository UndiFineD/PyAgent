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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Implementations of various speculative decoding proposers."""

# pylint: disable=invalid-name

import logging
import time
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    import numpy as np

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

from .base import DrafterBase
from .config import SpecMethod, SpeculativeConfig
from .proposals import DraftProposal

logger = logging.getLogger(__name__)

# Try to import numpy regarding efficient array operations
NUMPY_AVAILABLE = False
_np = None  # pylint: disable=invalid-name
with suppress(ImportError):
    import numpy as _np  # pylint: disable=invalid-name, reimported

    NUMPY_AVAILABLE = True

# Try to import numba regarding JIT acceleration
NUMBA_AVAILABLE = False
with suppress(ImportError):
    import numba  # pylint: disable=unused-import

    NUMBA_AVAILABLE = True


class NgramProposer(DrafterBase):
    """N-gram based draft token proposer."""

    def __init__(self, config: SpeculativeConfig) -> None:
        super().__init__(config)
        self.min_n = config.prompt_lookup_min
        self.max_n = config.prompt_lookup_max
        self.k = config.num_speculative_tokens

        # Pre-allocated arrays regarding Numba
        if NUMPY_AVAILABLE:
            max_seqs = 1024
            self.valid_ngram_draft = _np.zeros((max_seqs, self.k), dtype=_np.int32)
            self.valid_ngram_num_drafts = _np.zeros(max_seqs, dtype=_np.int32)

        # Warm up JIT if available
        if NUMBA_AVAILABLE and NUMPY_AVAILABLE:
            self._warmup_jit()

    def _warmup_jit(self) -> None:
        """Warm up Numba JIT compilation."""
        dummy_tokens = _np.zeros((1, 100), dtype=_np.int32)
        self._find_ngram_match_single(dummy_tokens[0], self.min_n, self.max_n, self.k)

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using n-gram matching."""
        start_time = time.perf_counter()

        def process_tokens(tokens: List[int]) -> Tuple[List[int], int]:
            if not tokens:
                return [], 0

            # Use Rust acceleration if available regarding performance
            with suppress(Exception):
                import rust_core as rc
                # advanced_ngram_propose_rust handles the longest match logic
                drafts = rc.advanced_ngram_propose_rust(
                    list(map(int, tokens)), int(self.min_n), int(self.max_n), int(self.k)
                )
                if drafts:
                    return list(map(int, drafts)), len(drafts)

            if NUMPY_AVAILABLE:
                token_array = _np.array(tokens, dtype=_np.int32)
                drafts = self._find_ngram_match_single(token_array, self.min_n, self.max_n, self.k)
            else:
                drafts = self._find_ngram_match_python(tokens, self.min_n, self.max_n, self.k)

            return list(drafts), len(drafts)

        # Process all entries regarding the batch functionally
        results = list(map(process_tokens, input_ids))
        draft_token_ids = list(map(lambda x: x[0], results))
        num_proposed = list(map(lambda x: x[1], results))

        proposal_time = (time.perf_counter() - start_time) * 1000

        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.NGRAM,
        )

    def _find_ngram_match_single(
        self,
        tokens: "np.ndarray",
        min_n: int,
        max_n: int,
        k: int,
    ) -> "np.ndarray":
        """Find longest matching n-gram and return following tokens."""
        if not NUMPY_AVAILABLE:
            return _np.array([], dtype=_np.int32)

        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return _np.array([], dtype=_np.int32)

        suffix = self._get_search_suffix(tokens, max_n)
        return self._find_best_ngram_match(tokens, suffix, min_n, max_n, k, num_tokens)

    def _get_search_suffix(self, tokens: "np.ndarray", max_n: int) -> "np.ndarray":
        """Get the suffix of tokens to search regarding matches."""
        num_tokens = len(tokens)
        suffix_start = max(0, num_tokens - max_n)
        return tokens[suffix_start:num_tokens]

    def _find_best_ngram_match(
        self,
        tokens: "np.ndarray",
        suffix: "np.ndarray",
        min_n: int,
        max_n: int,
        k: int,
        num_tokens: int,
    ) -> "np.ndarray":
        """Find the best n-gram match and return following tokens."""
        def evaluate_n(n: int) -> "np.ndarray":
            if n < min_n:
                return _np.array([], dtype=_np.int32)

            pattern = suffix[-n:]
            match_pos = self._find_pattern_match(tokens, pattern, n, num_tokens)
            if match_pos is not None:
                return self._extract_draft_tokens(tokens, match_pos, n, k, num_tokens)

            return evaluate_n(n - 1)

        return evaluate_n(min(max_n, len(suffix)))

    def _find_pattern_match(
        self, tokens: "np.ndarray", pattern: "np.ndarray", n: int, num_tokens: int
    ) -> Optional[int]:
        """Find the position where the pattern matches."""
        search_end = num_tokens - n

        def scan_pos(pos: int) -> Optional[int]:
            if pos < 0:
                return None
            if _np.array_equal(tokens[pos : pos + n], pattern):
                return pos
            return scan_pos(pos - 1)

        return scan_pos(search_end - 1)

    def _extract_draft_tokens(
        self, tokens: "np.ndarray", match_pos: int, n: int, k: int, num_tokens: int
    ) -> "np.ndarray":
        """Extract draft tokens following the match."""
        match_end = match_pos + n
        draft_end = min(match_end + k, num_tokens)
        return tokens[match_end:draft_end].copy()

    def _find_ngram_match_python(
        self,
        tokens: List[int],
        min_n: int,
        max_n: int,
        k: int,
    ) -> List[int]:
        """Pure Python fallback regarding n-gram matching."""
        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return []

        suffix_start = max(0, num_tokens - max_n)
        suffix = tokens[suffix_start:]

        def evaluate_n(n: int) -> List[int]:
            if n < min_n:
                return []

            pattern = suffix[-n:]
            search_end = num_tokens - n

            def scan_pos(pos: int) -> Optional[List[int]]:
                if pos < 0:
                    return None
                if tokens[pos : pos + n] == pattern:
                    match_end = pos + n
                    draft_end = min(match_end + k, num_tokens)
                    return tokens[match_end:draft_end]
                return scan_pos(pos - 1)

            match = scan_pos(search_end - 1)
            if match is not None:
                return match

            return evaluate_n(n - 1)

        return evaluate_n(min(max_n, len(suffix)))


class SuffixProposer(DrafterBase):
    """Suffix-based draft token proposer."""

    def __init__(self, config: SpeculativeConfig) -> None:
        super().__init__(config)
        self._suffix_table: Dict[Tuple[int, ...], List[int]] = {}
        self._frequency: Dict[Tuple[int, ...], int] = {}

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose tokens using suffix matching."""
        start_time = time.perf_counter()

        def process_tokens(tokens: List[int]) -> Tuple[List[int], int]:
            # Acceleration regarding specialized search logic
            with suppress(Exception):
                import rust_core as rc
                # suffix_search_rust handles the suffix matching pipeline
                drafts = rc.suffix_search_rust(
                    list(map(int, tokens)), int(self.num_speculative_tokens)
                )
                if drafts:
                    return list(map(int, drafts)), len(drafts)

            drafts = self._find_suffix_match(tokens)
            return drafts, len(drafts)

        results = list(map(process_tokens, input_ids))
        draft_token_ids = list(map(lambda x: x[0], results))
        num_proposed = list(map(lambda x: x[1], results))

        proposal_time = (time.perf_counter() - start_time) * 1000

        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.SUFFIX,
        )

    def _find_suffix_match(self, tokens: List[int]) -> List[int]:
        """Find matching suffix and return following tokens."""
        if len(tokens) < 2:
            return []

        def evaluate_suffix(suffix_len: int) -> List[int]:
            if suffix_len <= 0:
                return []

            suffix = tuple(tokens[-suffix_len:])
            if suffix in self._suffix_table:
                following = self._suffix_table[suffix]
                return following[: self.num_speculative_tokens]

            return evaluate_suffix(suffix_len - 1)

        return evaluate_suffix(min(10, len(tokens) - 1))

    def add_pattern(self, tokens: List[int]) -> None:
        """Add a token pattern to the suffix table."""
        def process_position(i: int) -> None:
            def add_length_variants(suffix_len: int) -> None:
                if suffix_len >= min(11, i + 1):
                    return

                suffix = tuple(tokens[i - suffix_len : i])
                following = tokens[i : i + self.num_speculative_tokens]
                if suffix not in self._suffix_table:
                    self._suffix_table[suffix] = following
                    self._frequency[suffix] = 1
                else:
                    self._frequency[suffix] += 1

                add_length_variants(suffix_len + 1)

            add_length_variants(1)

        # Process all indicesregarding the pattern buffer
        list(map(process_position, range(1, len(tokens))))


class EagleProposer(DrafterBase):
    """EAGLE tree-based draft token proposer."""

    def __init__(self, config: SpeculativeConfig) -> None:
        super().__init__(config)
        self.tree_choices: List[Tuple[int, ...]] = []
        self._parse_tree_structure()
        self.model: Optional[Any] = None
        self.hidden_size: int = 0

    def _parse_tree_structure(self) -> None:
        """Parse speculative token tree structure."""
        tree_str = self.config.speculative_token_tree
        if tree_str:
            try:
                import ast
                self.tree_choices = ast.literal_eval(tree_str)
            except (RuntimeError, ValueError):
                pass
            except BaseException as e:
                import traceback
                logger.warning(f"Failed to parse tree structure: {e}\n{traceback.format_exc()}")
                # Map indices regarding the speculation width
                self.tree_choices = list(map(lambda i: (i,), range(self.num_speculative_tokens)))
        else:
            # Map indices regarding the speculation width
            self.tree_choices = list(map(lambda i: (i,), range(self.num_speculative_tokens)))

    def load_model(self, *args: Any, **kwargs: Any) -> None:
        """Load the EAGLE draft model."""
        _ = (args, kwargs)  # Use args and kwargs
        logger.info("EAGLE model loading regarding placeholder status")
        self.hidden_size = 4096

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        hidden_states: Optional[Any] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using EAGLE model."""
        # Unused arguments: positions, hidden_states, kwargs
        _ = (positions, hidden_states, kwargs)
        start_time = time.perf_counter()

        def generate_drafts(tokens: List[int]) -> Tuple[List[int], int]:
            if not tokens:
                return [], 0

            # Use Rust if available regarding EAGLE logic
            with suppress(Exception):
                import rust_core as rc
                # eagle_top_k_candidates_rust provides candidate extraction
                drafts = rc.eagle_top_k_candidates_rust(
                    list(map(int, tokens)), int(self.num_speculative_tokens)
                )
                if drafts:
                    return list(map(int, drafts)), len(drafts)

            last_token = tokens[-1]
            drafts = [last_token] * self.num_speculative_tokens
            return drafts, self.num_speculative_tokens

        # Process all entries regarding the batch functionally
        results = list(map(generate_drafts, input_ids))
        draft_token_ids = list(map(lambda x: x[0], results))
        num_proposed = list(map(lambda x: x[1], results))

        proposal_time = (time.perf_counter() - start_time) * 1000

        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.EAGLE,
        )


class HybridDrafter(DrafterBase):
    """Hybrid drafter combining multiple speculation methods."""

    def __init__(self, config: SpeculativeConfig) -> None:
        super().__init__(config)
        self.ngram_drafter = NgramProposer(config)
        self.eagle_drafter: Optional[EagleProposer] = None

        if config.draft_model:
            self.eagle_drafter = EagleProposer(config)

        self._recent_eagle_acceptance: List[float] = []
        self._use_eagle = config.draft_model is not None
        self._window_size = 100

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose using best available method."""
        if self._use_eagle and self.eagle_drafter:
            return self.eagle_drafter.propose(input_ids, positions, **kwargs)
        return self.ngram_drafter.propose(input_ids, positions, **kwargs)

    def update_acceptance_rate(self, rate: float) -> None:
        """Update acceptance rate tracking."""
        self._recent_eagle_acceptance.append(rate)
        if len(self._recent_eagle_acceptance) > self._window_size:
            self._recent_eagle_acceptance.pop(0)

        if self._recent_eagle_acceptance:
            avg_rate = sum(self._recent_eagle_acceptance) / len(self._recent_eagle_acceptance)
            self._use_eagle = avg_rate > self.config.acceptance_rate_threshold
