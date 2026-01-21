# SPDX-License-Identifier: Apache-2.0
"""
N-gram Accelerators - Numba and Rust-based high-performance matching.
"""

from __future__ import annotations

import numpy as np

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

# Try to import numba for JIT compilation
try:
    from numba import njit, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False


if HAS_NUMBA:
    @njit
    def _ngram_match_numba(
        tokens: np.ndarray,
        pattern: np.ndarray,
        max_matches: int = 100,
    ) -> np.ndarray:
        """Numba-accelerated n-gram matching."""
        n_tokens = len(tokens)
        n_pattern = len(pattern)
        matches = np.zeros(max_matches, dtype=np.int32)
        match_count = 0
        
        for i in range(n_tokens - n_pattern + 1):
            found = True
            for j in range(n_pattern):
                if tokens[i + j] != pattern[j]:
                    found = False
                    break
            if found:
                matches[match_count] = i
                match_count += 1
                if match_count >= max_matches:
                    break
        
        return matches[:match_count]
    
    @njit(parallel=True)
    def _batch_propose_numba(
        all_tokens: np.ndarray,       # Flattened tokens
        token_offsets: np.ndarray,    # Start offset for each sequence
        token_lengths: np.ndarray,    # Length of each sequence
        min_n: int,
        max_n: int,
        k: int,
        proposals: np.ndarray,        # Output: [batch, k]
        proposal_lens: np.ndarray,    # Output: [batch]
    ) -> None:
        """Numba-accelerated batch proposal."""
        batch_size = len(token_offsets)
        
        for b in prange(batch_size):
            offset = token_offsets[b]
            length = token_lengths[b]
            
            if length < min_n:
                proposal_lens[b] = 0
                continue
            
            tokens = all_tokens[offset:offset + length]
            
            # Simple greedy matching for now
            best_len = 0
            best_proposal = np.zeros(k, dtype=np.int32)
            
            for n in range(max_n, min_n - 1, -1):
                if n > length:
                    continue
                
                pattern = tokens[-(n-1):]
                
                # Find matches
                for i in range(length - n):
                    found = True
                    for j in range(n - 1):
                        if tokens[i + j] != pattern[j]:
                            found = False
                            break
                    
                    if found:
                        # Get continuation
                        cont_start = i + n - 1
                        cont_len = min(k, length - cont_start)
                        
                        if cont_len > best_len:
                            best_len = cont_len
                            for c in range(cont_len):
                                best_proposal[c] = tokens[cont_start + c]
                            break
                
                if best_len > 0:
                    break
            
            proposal_lens[b] = best_len
            for c in range(best_len):
                proposals[b, c] = best_proposal[c]
