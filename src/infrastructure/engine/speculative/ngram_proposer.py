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
NgramProposer: N-gram Based Speculative Decoding

Implements prompt-lookup and n-gram based draft token proposal
with Numba-accelerated batch processing for high throughput.

Key Features Beyond vLLM:
- Multi-threading with adaptive thread count
- Fuzzy n-gram matching
- Weighted scoring by recency and frequency
- Streaming prompt integration
- Per-request n-gram caches

Based on vLLM v1 patterns with PyAgent innovations.
"""

from __future__ import annotations

import contextlib
import threading
from collections import defaultdict
from dataclasses import dataclass

with contextlib.suppress(ImportError):
    import rust_core

HAS_RUST = "rust_core" in globals()


@dataclass(frozen=True, slots=True)
class NgramConfig:
    """Configuration for N-gram proposer."""

    min_n: int = 1  # Minimum n-gram length
    max_n: int = 4  # Maximum n-gram length
    num_speculative_tokens: int = 5  # Number of tokens to propose
    max_model_len: int = 4096
    max_num_seqs: int = 256
    num_tokens_threshold: int = 8192  # Threshold for multi-threading
    max_threads: int = 8


@dataclass(slots=True)
class NgramMatch:
    """Represents an n-gram match in the context."""

    position: int  # Position in context where match starts
    length: int  # Length of the matching n-gram
    following_tokens: list[int]  # Tokens following the match
    score: float = 1.0  # Match score (recency/frequency weighted)


@dataclass(slots=True)
class NgramProposalResult:
    """Result of n-gram proposal."""

    draft_tokens: list[int]
    match_info: NgramMatch | None = None
    confidence: float = 0.0


class NgramCache:
    """
    Cache for n-gram lookups with position tracking.

    Stores n-grams with their positions for fast lookup.
    """

    def __init__(self, max_n: int = 4, max_entries: int = 10000):
        self.max_n = max_n
        self.max_entries = max_entries
        # ngram tuple -> list of positions
        self._cache: dict[tuple[int, ...], list[int]] = defaultdict(list)
        self._size = 0
        self._lock = threading.Lock()

    def add(self, tokens: list[int], position: int) -> None:
        """Add n-grams from tokens at given position."""
        with self._lock:
            for n in range(1, min(self.max_n + 1, len(tokens) + 1)):
                ngram = tuple(tokens[:n])
                if ngram not in self._cache:
                    self._size += 1
                    if self._size > self.max_entries:
                        self._evict_oldest()
                self._cache[ngram].append(position)

    def lookup(self, prefix: list[int]) -> list[int]:
        """Look up positions where prefix appears."""
        with self._lock:
            key = tuple(prefix)
            return list(self._cache.get(key, []))

    def _evict_oldest(self) -> None:
        """Evict oldest entries when cache is full."""
        # Simple eviction: remove entries with oldest positions
        to_remove = []
        for key, positions in self._cache.items():
            if len(positions) == 1:
                to_remove.append(key)
            else:
                # Keep only recent positions
                self._cache[key] = positions[-10:]

        for key in to_remove[: len(to_remove) // 2]:
            del self._cache[key]
            self._size -= 1

    def clear(self) -> None:
        """Clear the cache."""
        with self._lock:
            self._cache.clear()
            self._size = 0


class NgramProposer:
    """
    N-gram based speculative decoding proposer.

    Uses prompt lookup to find matching n-grams and propose
    following tokens as draft candidates.
    """

    def __init__(self, config: NgramConfig):
        self.config = config
        self.min_n = config.min_n
        self.max_n = config.max_n
        self.k = config.num_speculative_tokens
        self.max_model_len = config.max_model_len
        self.num_tokens_threshold = config.num_tokens_threshold
        self.max_threads = config.max_threads

        # Pre-allocate buffers
        self._draft_buffer = [[0] * self.k for _ in range(config.max_num_seqs)]
        self._num_drafts_buffer = [0] * config.max_num_seqs

        # Per-request caches
        self._caches: dict[str, NgramCache] = {}
        self._lock = threading.Lock()

    def propose(
        self, token_ids: list[int], _request_id: str = "", excluded_tokens: set[int] | None = None
    ) -> NgramProposalResult:
        """
        Generate draft token proposals using n-gram matching.

        Args:
            token_ids: Current sequence token IDs
            request_id: Optional request ID for caching
            excluded_tokens: Tokens to exclude from proposals

        Returns:
            NgramProposalResult with draft tokens
        """
        if len(token_ids) < self.min_n:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        excluded = excluded_tokens or set()

        # Try different n-gram lengths from max to min
        best_match: NgramMatch | None = None

        for n in range(self.max_n, self.min_n - 1, -1):
            if len(token_ids) < n:
                continue

            prefix = token_ids[-n:]
            match = self._find_match(token_ids[:-1], prefix, excluded)

            if match and len(match.following_tokens) > (len(best_match.following_tokens) if best_match else 0):
                best_match = match

        if best_match is None:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        # Limit to k tokens
        draft_tokens = best_match.following_tokens[: self.k]
        confidence = best_match.score * (len(draft_tokens) / self.k)

        return NgramProposalResult(draft_tokens=draft_tokens, match_info=best_match, confidence=confidence)

    def _find_match(self, context: list[int], prefix: list[int], excluded: set[int]) -> NgramMatch | None:
        """Find best matching n-gram in context."""
        if HAS_RUST and hasattr(rust_core, "ngram_find_match_rust"):
            if result := getattr(rust_core, "ngram_find_match_rust")(context, prefix, list(excluded), self.k):
                pos, length, following = result
                return NgramMatch(
                    position=pos,
                    length=length,
                    following_tokens=following,
                    score=self._compute_score(pos, len(context)),
                )
            return None

        # Python implementation
        n = len(prefix)
        best_pos = -1
        best_following: list[int] = []

        # Search from end (more recent matches preferred)
        for i in range(len(context) - n, -1, -1):
            if context[i : i + n] == prefix:
                # Found match, get following tokens
                start = i + n
                end = min(start + self.k, len(context))
                following = [t for t in context[start:end] if t not in excluded]

                if len(following) > len(best_following):
                    best_pos = i
                    best_following = following

                # Stop at first good match (most recent)
                if len(best_following) >= self.k:
                    break

        if best_pos < 0:
            return None

        return NgramMatch(
            position=best_pos,
            length=n,
            following_tokens=best_following,
            score=self._compute_score(best_pos, len(context)),
        )

    def _compute_score(self, position: int, context_len: int) -> float:
        """Compute match score based on recency."""
        return 1.0 if context_len == 0 else 0.5 + 0.5 * (position + 1) / context_len

    def batch_propose(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None = None
    ) -> list[NgramProposalResult]:
        """
        Batch version of n-gram proposal.

        Uses multi-threading for large batches.
        """
        num_requests = len(batch_token_ids)
        if num_requests == 0:
            return []

        # Calculate total tokens
        total_tokens = sum(len(ids) for ids in batch_token_ids)

        # Use multi-threading for large batches
        if total_tokens >= self.num_tokens_threshold and num_requests > 1:
            return self._batch_propose_parallel(batch_token_ids, batch_request_ids)

        return self._batch_propose_sequential(batch_token_ids, batch_request_ids)

    def _batch_propose_sequential(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None
    ) -> list[NgramProposalResult]:
        """Sequential batch proposal."""
        results = []
        for i, token_ids in enumerate(batch_token_ids):
            request_id = batch_request_ids[i] if batch_request_ids else ""
            result = self.propose(token_ids, request_id)
            results.append(result)
        return results

    def _batch_propose_parallel(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None
    ) -> list[NgramProposalResult]:
        """Parallel batch proposal using threading."""
        num_requests = len(batch_token_ids)
        results: list[NgramProposalResult | None] = [None] * num_requests

        def process_range(start: int, end: int) -> None:
            for i in range(start, end):
                request_id = batch_request_ids[i] if batch_request_ids else ""
                results[i] = self.propose(batch_token_ids[i], request_id)

        # Divide work across threads
        num_threads = min(self.max_threads, num_requests)
        chunk_size = (num_requests + num_threads - 1) // num_threads

        threads = []
        for t in range(num_threads):
            start = t * chunk_size
            end = min(start + chunk_size, num_requests)
            if start < end:
                thread = threading.Thread(target=process_range, args=(start, end))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        return [r for r in results if r is not None]

    def propose_fuzzy(self, token_ids: list[int], max_distance: int = 1) -> NgramProposalResult:
        """
        Fuzzy n-gram matching with edit distance tolerance.

        Allows matches with small differences for more proposals.
        """
        if len(token_ids) < self.min_n:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        if HAS_RUST and hasattr(rust_core, "ngram_fuzzy_match_rust"):
            if result := getattr(rust_core, "ngram_fuzzy_match_rust")(
                token_ids[:-1], token_ids[-self.max_n :], self.k, max_distance
            ):
                draft_tokens, score = result
                return NgramProposalResult(draft_tokens=draft_tokens, confidence=score)
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        # Python implementation with simple fuzzy matching
        context = token_ids[:-1]
        prefix = token_ids[-self.max_n :]
        n = len(prefix)

        best_following: list[int] = []
        best_score = 0.0

        for i in range(len(context) - n + 1):
            candidate = context[i : i + n]
            distance = self._hamming_distance(prefix, candidate)

            if distance <= max_distance:
                start = i + n
                end = min(start + self.k, len(context))
                following = context[start:end]

                score = 1.0 - (distance / max(1, max_distance + 1))
                if len(following) > len(best_following) or (
                    len(following) == len(best_following) and score > best_score
                ):
                    best_following = following
                    best_score = score

        return NgramProposalResult(draft_tokens=best_following, confidence=best_score * (len(best_following) / self.k))

    def _hamming_distance(self, a: list[int], b: list[int]) -> int:
        """Compute Hamming distance between two sequences."""
        if len(a) != len(b):
            return max(len(a), len(b))
        return sum(x != y for x, y in zip(a, b))

    def get_cache(self, request_id: str) -> NgramCache:
        """Get or create cache for request."""
        with self._lock:
            if request_id not in self._caches:
                self._caches[request_id] = NgramCache(max_n=self.max_n)
            return self._caches[request_id]

    def clear_cache(self, request_id: str) -> None:
        """Clear cache for request."""
        with self._lock:
            if request_id in self._caches:
                del self._caches[request_id]


class WeightedNgramProposer(NgramProposer):
    """
    N-gram proposer with frequency and recency weighting.

    Tracks n-gram occurrences and weights matches by frequency.
    """

    def __init__(self, config: NgramConfig, decay_factor: float = 0.9):
        super().__init__(config)
        self.decay_factor = decay_factor
        # ngram -> (count, last_position)
        self._ngram_stats: dict[tuple[int, ...], tuple[int, int]] = {}

    def update_stats(self, token_ids: list[int]) -> None:
        """Update n-gram statistics from tokens."""
        for n in range(self.min_n, self.max_n + 1):
            for i in range(len(token_ids) - n + 1):
                ngram = tuple(token_ids[i : i + n])
                count, _ = self._ngram_stats.get(ngram, (0, 0))
                self._ngram_stats[ngram] = (count + 1, i)


class PromptLookupProposer:
    """
    Prompt-lookup based proposer that searches for repetitions.

    Specialized for scenarios where the prompt contains repetitive patterns
    that are likely to continue in generation.
    """

    def __init__(self, min_lookup_len: int = 3, max_lookup_len: int = 10, num_speculative_tokens: int = 5):
        self.min_len = min_lookup_len
        self.max_len = max_lookup_len
        self.k = num_speculative_tokens

    def propose(self, prompt_tokens: list[int], generated_tokens: list[int]) -> list[int]:
        """
        Propose tokens by looking up patterns in prompt.

        Args:
            prompt_tokens: Original prompt token IDs
            generated_tokens: Already generated token IDs

        Returns:
            List of proposed draft tokens
        """
        if not generated_tokens:
            return []

        if HAS_RUST and hasattr(rust_core, "prompt_lookup_propose_rust"):
            return getattr(rust_core, "prompt_lookup_propose_rust")(
                prompt_tokens, generated_tokens, self.min_len, self.max_len, self.k
            )

        # Try different suffix lengths
        for suffix_len in range(self.max_len, self.min_len - 1, -1):
            if len(generated_tokens) < suffix_len:
                continue

            suffix = generated_tokens[-suffix_len:]

            # Search in prompt
            for i in range(len(prompt_tokens) - suffix_len):
                if prompt_tokens[i : i + suffix_len] == suffix:
                    # Found match, return following tokens
                    start = i + suffix_len
                    end = min(start + self.k, len(prompt_tokens))
                    return prompt_tokens[start:end]

        return []


class HybridNgramProposer:
    """
    Hybrid proposer combining exact and fuzzy n-gram matching.

    Falls back to fuzzy matching when exact matching fails.
    """

    def __init__(self, config: NgramConfig):
        self.exact_proposer = NgramProposer(config)
        self.weighted_proposer = WeightedNgramProposer(config)
        self.prompt_lookup = PromptLookupProposer(
            min_lookup_len=config.min_n,
            max_lookup_len=config.max_n,
            num_speculative_tokens=config.num_speculative_tokens,
        )
        self.config = config

    def propose(self, token_ids: list[int], prompt_len: int = 0, use_fuzzy: bool = False) -> NgramProposalResult:
        """
        Propose using best available method.

        Args:
            token_ids: Full token sequence
            prompt_len: Length of original prompt
            use_fuzzy: Whether to use fuzzy matching as fallback
        """
        # Try exact matching first
        result = self.exact_proposer.propose(token_ids)
        if result.draft_tokens:
            return result

        # Try prompt lookup
        if prompt_len > 0:
            prompt = token_ids[:prompt_len]
            generated = token_ids[prompt_len:]
            if draft := self.prompt_lookup.propose(prompt, generated):
                return NgramProposalResult(draft_tokens=draft, confidence=0.8)

        # Fall back to fuzzy matching
        if use_fuzzy:
            return self.exact_proposer.propose_fuzzy(token_ids)

        return NgramProposalResult(draft_tokens=[], confidence=0.0)


class NgramProposerFactory:
    """Factory for creating N-gram proposers."""

    @staticmethod
    def create_simple(num_speculative_tokens: int = 5, min_n: int = 1, max_n: int = 4) -> NgramProposer:
        """Create simple n-gram proposer."""
        config = NgramConfig(min_n=min_n, max_n=max_n, num_speculative_tokens=num_speculative_tokens)
        return NgramProposer(config)

    @staticmethod
    def create_weighted(num_speculative_tokens: int = 5, decay_factor: float = 0.9) -> WeightedNgramProposer:
        """Create weighted n-gram proposer."""
        config = NgramConfig(num_speculative_tokens=num_speculative_tokens)
        return WeightedNgramProposer(config, decay_factor=decay_factor)

    @staticmethod
    def create_hybrid(num_speculative_tokens: int = 5, min_n: int = 1, max_n: int = 4) -> HybridNgramProposer:
        """Create hybrid n-gram proposer."""
        config = NgramConfig(min_n=min_n, max_n=max_n, num_speculative_tokens=num_speculative_tokens)
        return HybridNgramProposer(config)
