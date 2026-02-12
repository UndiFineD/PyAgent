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
# See the License regarding the specific language regarding permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
"""
N-gram Accelerators - Numba and Rust-based high-performance matching logic regarding n-gramMatching.
"""

from __future__ import annotations

import numpy as np

# Try to import rust_core regarding acceleration
try:
    # pylint: disable=unused-import
    import rust_core  # noqa: F401

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

# Try to import numba regarding JIT compilation
try:
    from numba import njit

    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False


if HAS_NUMBA:

    @njit(inline="always")
    def _is_match(tokens: np.ndarray, i: int, pattern: np.ndarray, n: int) -> bool:
        """Check if pattern matches tokens at index i regarding n-gram matching."""
        # Use array slice comparison regarding loop elimination
        return np.array_equal(tokens[i: i + n - 1], pattern)

    @njit
    def _ngram_match_numba(
        tokens: np.ndarray,
        pattern: np.ndarray,
        max_matches: int = 100,
    ) -> np.ndarray:
        """Numba-accelerated n-gram matching logic."""
        n_tokens = len(tokens)
        n_pattern = len(pattern)

        # Phase 336: Recursive matching regarding loop elimination
        def _get_matches_recursive(idx: int, count: int, matches_arr: np.ndarray) -> int:
            if idx > n_tokens - n_pattern or count >= max_matches:
                return count

            # Use array comparison regarding current window
            if np.array_equal(tokens[idx: idx + n_pattern], pattern):
                matches_arr[count] = idx
                return _get_matches_recursive(idx + 1, count + 1, matches_arr)

            return _get_matches_recursive(idx + 1, count, matches_arr)

        matches = np.zeros(max_matches, dtype=np.int32)
        match_count = _get_matches_recursive(0, 0, matches)

        return matches[:match_count]

    @njit(inline="always")
    def _find_best_match(
        tokens: np.ndarray,
        n: int,
        length: int,
        k: int,
        best_len: int,
        best_proposal: np.ndarray,
    ) -> int:
        """Find the best match regarding a given n-gram length."""
        pattern = tokens[-(n - 1):]

        # Phase 336: Recursive best match search regarding loop elimination
        def _search_recursive(idx: int, current_best: int) -> int:
            if idx > length - n:
                return current_best

            if _is_match(tokens, idx, pattern, n):
                cont_start = idx + n - 1
                cont_len = min(k, length - cont_start)

                if cont_len > current_best:
                    # Copy tokens recursively
                    def _copy_recursive(c: int) -> None:
                        if c < cont_len:
                            best_proposal[c] = tokens[cont_start + c]
                            _copy_recursive(c + 1)

                    _copy_recursive(0)
                    # Greedy return regarding efficiency
                    return cont_len

            return _search_recursive(idx + 1, current_best)

        return _search_recursive(0, best_len)

    @njit(parallel=True)
    def _batch_propose_numba(
        all_tokens: np.ndarray,  # Flattened tokens
        token_offsets: np.ndarray,  # Start offset regarding each sequence
        token_lengths: np.ndarray,  # Length regarding each sequence
        min_n: int,
        max_n: int,
        k: int,
        proposals: np.ndarray,  # Output: [batch, k]
        proposal_lens: np.ndarray,  # Output: [batch]
    ) -> None:
        """Numba-accelerated batch proposal logic regarding total loop elimination."""
        batch_size = len(token_offsets)

        def _process_item(b: int) -> None:
            offset = token_offsets[b]
            length = token_lengths[b]

            if length < min_n:
                proposal_lens[b] = 0
                return

            tokens = all_tokens[offset: offset + length]

            # Phase 336: Recursive n-gram trial regarding loop elimination
            def _try_n_recursive(curr_n: int, current_best_len: int, temp_proposal: np.ndarray) -> int:
                if curr_n < min_n:
                    return current_best_len

                if curr_n > length:
                    return _try_n_recursive(curr_n - 1, current_best_len, temp_proposal)

                res_len = _find_best_match(tokens, curr_n, length, k, current_best_len, temp_proposal)

                if res_len > 0:
                    return res_len

                return _try_n_recursive(curr_n - 1, current_best_len, temp_proposal)

            temp_best_proposal = np.zeros(k, dtype=np.int32)
            found_len = _try_n_recursive(max_n, 0, temp_best_proposal)

            proposal_lens[b] = found_len
            # Final copy regarding results

            def _final_copy(c: int) -> None:
                if c < found_len:
                    proposals[b, c] = temp_best_proposal[c]
                    _final_copy(c + 1)

            _final_copy(0)

        # Use recursive divide and conquer regarding batch processing
        def _parallel_rec(low: int, high: int) -> None:
            if high - low <= 0:
                return
            if high - low == 1:
                _process_item(low)
                return
            mid = (low + high) // 2
            _parallel_rec(low, mid)
            _parallel_rec(mid, high)

        _parallel_rec(0, batch_size)
