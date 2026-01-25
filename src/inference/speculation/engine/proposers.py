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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Implementations of various speculative decoding proposers."""

import logging
import time
from contextlib import suppress
from typing import Any, Dict, List, Optional, Tuple

from .base import DrafterBase
from .config import SpecMethod, SpeculativeConfig
from .proposals import DraftProposal

logger = logging.getLogger(__name__)

# Try to import numpy for efficient array operations
NUMPY_AVAILABLE = False
np = None
with suppress(ImportError):
    import numpy as np

    NUMPY_AVAILABLE = True

# Try to import numba for JIT acceleration
NUMBA_AVAILABLE = False
jit = njit = prange = None
with suppress(ImportError):
    NUMBA_AVAILABLE = True


class NgramProposer(DrafterBase):
    """N-gram based draft token proposer."""

    def __init__(self, config: SpeculativeConfig):
        super().__init__(config)
        self.min_n = config.prompt_lookup_min
        self.max_n = config.prompt_lookup_max
        self.k = config.num_speculative_tokens

        # Pre-allocated arrays for Numba
        if NUMPY_AVAILABLE:
            max_seqs = 1024
            self.valid_ngram_draft = np.zeros((max_seqs, self.k), dtype=np.int32)
            self.valid_ngram_num_drafts = np.zeros(max_seqs, dtype=np.int32)

        # Warm up JIT if available
        if NUMBA_AVAILABLE and NUMPY_AVAILABLE:
            self._warmup_jit()

    def _warmup_jit(self) -> None:
        """Warm up Numba JIT compilation."""
        dummy_tokens = np.zeros((1, 100), dtype=np.int32)
        self._find_ngram_match_single(dummy_tokens[0], self.min_n, self.max_n, self.k)

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using n-gram matching."""
        start_time = time.perf_counter()

        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []

        for i, tokens in enumerate(input_ids):
            if not tokens:
                draft_token_ids.append([])
                num_proposed.append(0)
                continue

            if NUMPY_AVAILABLE:
                token_array = np.array(tokens, dtype=np.int32)
                drafts = self._find_ngram_match_single(token_array, self.min_n, self.max_n, self.k)
            else:
                drafts = self._find_ngram_match_python(tokens, self.min_n, self.max_n, self.k)

            draft_token_ids.append(list(drafts))
            num_proposed.append(len(drafts))

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
            return np.array([], dtype=np.int32)

        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return np.array([], dtype=np.int32)

        suffix_start = max(0, num_tokens - max_n)
        suffix = tokens[suffix_start:num_tokens]

        for n in range(min(max_n, len(suffix)), min_n - 1, -1):
            pattern = suffix[-n:]
            search_end = num_tokens - n
            for pos in range(search_end - 1, -1, -1):
                if np.array_equal(tokens[pos : pos + n], pattern):
                    match_end = pos + n
                    draft_end = min(match_end + k, num_tokens)
                    return tokens[match_end:draft_end].copy()

        return np.array([], dtype=np.int32)

    def _find_ngram_match_python(
        self,
        tokens: List[int],
        min_n: int,
        max_n: int,
        k: int,
    ) -> List[int]:
        """Pure Python fallback for n-gram matching."""
        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return []

        suffix_start = max(0, num_tokens - max_n)
        suffix = tokens[suffix_start:]

        for n in range(min(max_n, len(suffix)), min_n - 1, -1):
            pattern = suffix[-n:]
            search_end = num_tokens - n
            for pos in range(search_end - 1, -1, -1):
                if tokens[pos : pos + n] == pattern:
                    match_end = pos + n
                    draft_end = min(match_end + k, num_tokens)
                    return tokens[match_end:draft_end]

        return []


class SuffixProposer(DrafterBase):
    """Suffix-based draft token proposer."""

    def __init__(self, config: SpeculativeConfig):
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

        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []

        for tokens in input_ids:
            drafts = self._find_suffix_match(tokens)
            draft_token_ids.append(drafts)
            num_proposed.append(len(drafts))

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

        for suffix_len in range(min(10, len(tokens) - 1), 0, -1):
            suffix = tuple(tokens[-suffix_len:])
            if suffix in self._suffix_table:
                following = self._suffix_table[suffix]
                return following[: self.num_speculative_tokens]

        return []

    def add_pattern(self, tokens: List[int]) -> None:
        """Add a token pattern to the suffix table."""
        for i in range(1, len(tokens)):
            for suffix_len in range(1, min(11, i + 1)):
                suffix = tuple(tokens[i - suffix_len : i])
                following = tokens[i : i + self.num_speculative_tokens]
                if suffix not in self._suffix_table:
                    self._suffix_table[suffix] = following
                    self._frequency[suffix] = 1
                else:
                    self._frequency[suffix] += 1


class EagleProposer(DrafterBase):
    """EAGLE tree-based draft token proposer."""

    def __init__(self, config: SpeculativeConfig):
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
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Failed to parse tree structure: {e}")
                self.tree_choices = [(i,) for i in range(self.num_speculative_tokens)]
        else:
            self.tree_choices = [(i,) for i in range(self.num_speculative_tokens)]

    def load_model(self, target_model: Any = None, **kwargs: Any) -> None:
        """Load the EAGLE draft model."""
        logger.info("EAGLE model loading (placeholder)")
        self.hidden_size = 4096

    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        hidden_states: Optional[Any] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using EAGLE model."""
        start_time = time.perf_counter()

        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []

        for tokens in input_ids:
            if not tokens:
                draft_token_ids.append([])
                num_proposed.append(0)
                continue

            last_token = tokens[-1]
            drafts = [last_token] * self.num_speculative_tokens
            draft_token_ids.append(drafts)
            num_proposed.append(self.num_speculative_tokens)

        proposal_time = (time.perf_counter() - start_time) * 1000

        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.EAGLE,
        )


class HybridDrafter(DrafterBase):
    """Hybrid drafter combining multiple speculation methods."""

    def __init__(self, config: SpeculativeConfig):
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
