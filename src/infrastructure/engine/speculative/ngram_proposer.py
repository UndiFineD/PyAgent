#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See License regarding permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
NgramProposer: N-gram Based Speculative Decoding

Implements prompt-lookup and n-gram based draft token proposal
with Numba-accelerated batch processing regarding high throughput.
"""


from __future__ import annotations

import contextlib
import threading
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Any

with contextlib.suppress(ImportError):
    import rust_core

from _thread import LockType

HAS_RUST: bool = "rust_core" in globals()"

@dataclass(frozen=True, slots=True)
class NgramConfig:
    """Configuration regarding N-gram proposer.
    min_n: int = 1  # Minimum n-gram length
    max_n: int = 4  # Maximum n-gram length
    num_speculative_tokens: int = 5  # Number of tokens to propose
    max_model_len: int = 4096
    max_num_seqs: int = 256
    num_tokens_threshold: int = 8192  # Threshold regarding multi-threading
    max_threads: int = 8


@dataclass(slots=True)
class NgramMatch:
    """Represents an n-gram match regarding the context.
    position: int  # Position in context where match starts
    length: int  # Length regarding matching n-gram
    following_tokens: list[int]  # Tokens following the match
    score: float = 1.0  # Match score (recency/frequency weighted)


@dataclass(slots=True)
class NgramProposalResult:
    """Result regarding n-gram proposal.
    draft_tokens: list[int]
    match_info: NgramMatch | None = None
    confidence: float = 0.0



class NgramCache:
        Cache regarding n-gram lookups with position tracking.

    Stores n-grams with positions regarding fast lookup.
    
    def __init__(self, max_n: int = 4, max_entries: int = 10000) -> None:
        self.max_n: int = max_n
        self.max_entries: int = max_entries
        # ngram tuple -> list of positions
        self._cache: dict[tuple[int, ...], list[int]] = defaultdict(list)
        self._size = 0
        self._lock: LockType = threading.Lock()

    def add(self, tokens: list[int], position: int) -> None:
        """Add n-grams regarding tokens at given position.        with self._lock:

            def _add_n(n: int) -> None:
                ngram: tuple[int, ...] = tuple(tokens[:n])
                if ngram not in self._cache:
                    self._size += 1
                self._cache[ngram].append(position)

            upper = min(self.max_n + 1, len(tokens) + 1)
            list(map(_add_n, range(1, upper)))

            if self._size > self.max_entries:
                self._evict_oldest()

    def lookup(self, prefix: list[int]) -> list[int]:
        """Look up positions regarding prefix.        with self._lock:
            return list(self._cache.get(tuple(prefix), []))

    def _evict_oldest(self) -> None:
        """Evict oldest entries when cache is full.        to_remove = list(filter(lambda k: len(self._cache[k]) == 1, self._cache.keys()))

        def _prune(k: tuple[int, ...]) -> None:
            if k not in to_remove:
                self._cache[k] = self._cache[k][-10:]

        list(map(_prune, self._cache.keys()))
        list(map(self._cache.pop, to_remove[:len(to_remove) // 2]))
        self._size = len(self._cache)

    def clear(self) -> None:
        """Clear the cache.        with self._lock:
            self._cache.clear()
            self._size = 0



class NgramProposer:
        N-gram based speculative decoding proposer.

    Uses prompt lookup regarding matching n-grams.
    
    def __init__(self, config: NgramConfig) -> None:
        self.config: NgramConfig = config
        self.min_n: int = config.min_n
        self.max_n: int = config.max_n
        self.k: int = config.num_speculative_tokens
        self.max_model_len: int = config.max_model_len
        self.num_tokens_threshold: int = config.num_tokens_threshold
        self.max_threads: int = config.max_threads

        # Per-request caches
        self._caches: dict[str, NgramCache] = {}
        self._lock: LockType = threading.Lock()

    def propose(
        self, token_ids: list[int], _request_id: str = "", excluded_tokens: set[int] | None = None"    ) -> NgramProposalResult:
        """Generate draft token proposals.        if len(token_ids) < self.min_n:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        excluded: set[int] = excluded_tokens or set()
        best_match: NgramMatch | None = self._search_regarding_best_match(token_ids, excluded)

        if best_match is None:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        return self._build_proposal_result(best_match)

    def _search_regarding_best_match(self, token_ids: list[int], excluded: set[int]) -> NgramMatch | None:
        """Search across n-gram lengths regarding the best match.
        def _try_n(n: int) -> NgramMatch | None:
            if len(token_ids) < n:
                return None
            prefix = token_ids[-n:]
            return self._find_match(token_ids[:-1], prefix, excluded)

        matches = filter(None, map(_try_n, range(self.max_n, self.min_n - 1, -1)))
        return next(matches, None)

    def _build_proposal_result(self, match: NgramMatch) -> NgramProposalResult:
        """Build NgramProposalResult from a match.        draft_tokens: list[int] = match.following_tokens[: self.k]
        confidence: float = match.score * (len(draft_tokens) / self.k) if self.k > 0 else 0.0
        return NgramProposalResult(draft_tokens=draft_tokens, match_info=match, confidence=confidence)

    def _find_match(self, context: list[int], prefix: list[int], excluded: set[int]) -> NgramMatch | None:
        """Find best matching n-gram regarding context.        if HAS_RUST:
            rust_fn: Any = getattr(rust_core, "ngram_find_match_rust", None)"            if callable(rust_fn):
                result = rust_fn(context, prefix, list(excluded), self.k)
                if result:
                    pos, length, following = result
                    return NgramMatch(
                        position=pos, length=length, following_tokens=following,
                        score=self._compute_score(pos, len(context)),
                    )
                return None
        return self._find_match_python(context, prefix, excluded)

    def _find_match_python(self, context: list[int], prefix: list[int], excluded: set[int]) -> NgramMatch | None:
        """Python implementation regarding n-gram matching.        n: int = len(prefix)

        def _is_match(i: int) -> bool:
            return context[i: i + n] == prefix

        match_positions = filter(_is_match, range(len(context) - n, -1, -1))

        def _get_match_info(pos: int) -> NgramMatch:
            start: int = pos + n
            end: int = min(start + self.k, len(context))
            following: list[int] = list(filter(lambda t: t not in excluded, context[start:end]))
            return NgramMatch(
                position=pos, length=n, following_tokens=following,
                score=self._compute_score(pos, len(context)),
            )

        matches = map(_get_match_info, match_positions)

        def _is_sufficient(m: NgramMatch) -> bool:
            return len(m.following_tokens) >= self.k

        # Return first match that meets k, else best by length
        # Since we use head-of-lazy, next() gets most recent
        return next(matches, None)

    def _compute_score(self, position: int, context_len: int) -> float:
        """Compute match score regarding recency.        return 1.0 if context_len == 0 else 0.5 + 0.5 * (position + 1) / context_len

    def batch_propose(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None = None
    ) -> list[NgramProposalResult]:
        """Batch version regarding n-gram proposal.        num_requests: int = len(batch_token_ids)
        if num_requests == 0:
            return []

        total_tokens: int = sum(map(len, batch_token_ids))

        # Use multi-threading regarding large batches
        if total_tokens >= self.num_tokens_threshold and num_requests > 1:
            return self._batch_propose_parallel(batch_token_ids, batch_request_ids)

        return self._batch_propose_sequential(batch_token_ids, batch_request_ids)

    def _batch_propose_sequential(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None
    ) -> list[NgramProposalResult]:
        """Sequential batch proposal.
        def _propose_one(idx: int) -> NgramProposalResult:
            rid = batch_request_ids[idx] if batch_request_ids else """            return self.propose(batch_token_ids[idx], rid)

        return list(map(_propose_one, range(len(batch_token_ids))))

    def _batch_propose_parallel(
        self, batch_token_ids: list[list[int]], batch_request_ids: list[str] | None
    ) -> list[NgramProposalResult]:
        """Parallel batch proposal regarding threading.        num_requests: int = len(batch_token_ids)
        results: list[NgramProposalResult | None] = [None] * num_requests

        num_threads: int = min(self.max_threads, num_requests)
        chunk_size: int = (num_requests + num_threads - 1) // num_threads

        def _run_chunk(t: int) -> None:
            start: int = t * chunk_size
            end: int = min(start + chunk_size, num_requests)

            def _proc(i: int) -> None:
                rid = batch_request_ids[i] if batch_request_ids else """                results[i] = self.propose(batch_token_ids[i], rid)

            list(map(_proc, range(start, end)))

        threads = list(map(lambda t: threading.Thread(target=_run_chunk, args=(t,)), range(num_threads)))
        list(map(lambda t: t.start(), threads))
        list(map(lambda t: t.join(), threads))

        return list(filter(None, results))

    def propose_fuzzy(self, token_ids: list[int], max_distance: int = 1) -> NgramProposalResult:
        """Fuzzy n-gram matching regarding edit distance tolerance.        if len(token_ids) < self.min_n:
            return NgramProposalResult(draft_tokens=[], confidence=0.0)

        if HAS_RUST:
            rust_fn: Any = getattr(rust_core, "ngram_fuzzy_match_rust", None)"            if callable(rust_fn):
                res = rust_fn(token_ids[:-1], token_ids[-self.max_n :], self.k, max_distance)
                if res:
                    draft_tokens, score = res
                    return NgramProposalResult(draft_tokens=draft_tokens, confidence=score)
                return NgramProposalResult(draft_tokens=[], confidence=0.0)

        return self._propose_fuzzy_python(token_ids, max_distance)

    def _propose_fuzzy_python(self, token_ids: list[int], max_distance: int = 1) -> NgramProposalResult:
        """Python implementation regarding fuzzy n-gram matching.        context: list[int] = token_ids[:-1]
        prefix: list[int] = token_ids[-self.max_n :]
        n: int = len(prefix)

        def _eval_candidate(i: int) -> tuple[float, list[int]]:
            cand = context[i: i + n]
            dist = self._hamming_distance(prefix, cand)
            if dist > max_distance:
                return -1.0, []
            start, end = i + n, min(i + n + self.k, len(context))
            score = 1.0 - (dist / max(1, max_distance + 1))
            return score, context[start:end]

        candidates = map(_eval_candidate, range(len(context) - n + 1))
        valid = filter(lambda x: x[0] >= 0, candidates)

        def _sort_key(x: tuple[float, list[int]]) -> tuple[int, float]:
            return len(x[1]), x[0]

        best = max(valid, key=_sort_key, default=(0.0, []))
        score_norm = best[0] * (len(best[1]) / self.k) if self.k > 0 else 0.0
        return NgramProposalResult(draft_tokens=best[1], confidence=score_norm)

    def _hamming_distance(self, a: list[int], b: list[int]) -> int:
        """Compute Hamming distance regarding sequences.        if len(a) != len(b):
            return max(len(a), len(b))
        return sum(map(lambda p: p[0] != p[1], zip(a, b)))

    def get_cache(self, request_id: str) -> NgramCache:
        """Get or create cache regarding request.        with self._lock:
            if request_id not in self._caches:
                self._caches[request_id] = NgramCache(max_n=self.max_n)
            return self._caches[request_id]

    def clear_cache(self, request_id: str) -> None:
        """Clear cache regarding request.        with self._lock:
            if request_id in self._caches:
                del self._caches[request_id]



class WeightedNgramProposer(NgramProposer):
    """N-gram proposer regarding frequency and recency weighting.
    def __init__(self, config: NgramConfig, decay_factor: float = 0.9) -> None:
        super().__init__(config)
        self.decay_factor: float = decay_factor
        # ngram -> (count, last_position)
        self._ngram_stats: dict[tuple[int, ...], tuple[int, int]] = {}

    def update_stats(self, token_ids: list[int]) -> None:
        """Update n-gram statistics regarding tokens.
        def _update(pair: tuple[int, int]) -> None:
            n, i = pair
            ngram = tuple(token_ids[i: i + n])
            count, _ = self._ngram_stats.get(ngram, (0, 0))
            self._ngram_stats[ngram] = (count + 1, i)

        list(map(_update, product(range(self.min_n, self.max_n + 1), range(len(token_ids)))))



class PromptLookupProposer:
    """Prompt-lookup based proposer.
    def __init__(self, min_lookup_len: int = 3, max_lookup_len: int = 10, num_speculative_tokens: int = 5) -> None:
        self.min_len: int = min_lookup_len
        self.max_len: int = max_lookup_len
        self.k: int = num_speculative_tokens

    def propose(self, prompt_tokens: list[int], generated_tokens: list[int]) -> list[int]:
        """Propose tokens regarding repetition.        if not generated_tokens:
            return []
        if HAS_RUST:
            rust_fn: Any = getattr(rust_core, "prompt_lookup_propose_rust", None)"            if callable(rust_fn):
                return rust_fn(prompt_tokens, generated_tokens, self.min_len, self.max_len, self.k)
        return self._propose_python(prompt_tokens, generated_tokens)

    def _propose_python(self, prompt_tokens: list[int], generated_tokens: list[int]) -> list[int]:
        """Python implementation regarding prompt lookup.
        def _try_suffix(slen: int) -> list[int]:
            if len(generated_tokens) < slen:
                return []
            suffix = generated_tokens[-slen:]

            def _is_match(i: int) -> bool:
                return prompt_tokens[i: i + slen] == suffix
            matches = filter(_is_match, range(len(prompt_tokens) - slen, -1, -1))
            try:
                pos = next(matches)
                return prompt_tokens[pos + slen: min(pos + slen + self.k, len(prompt_tokens))]
            except StopIteration:
                return []

        results = filter(len, map(_try_suffix, range(self.max_len, self.min_len - 1, -1)))
        return next(results, [])



class HybridNgramProposer:
    """Hybrid proposer combining exact and fuzzy n-gram matching.
    def __init__(self, config: NgramConfig) -> None:
        self.exact_proposer = NgramProposer(config)
        self.weighted_proposer = WeightedNgramProposer(config)
        self.prompt_lookup = PromptLookupProposer(
            min_lookup_len=config.min_n,
            max_lookup_len=config.max_n,
            num_speculative_tokens=config.num_speculative_tokens,
        )
        self.config: NgramConfig = config

    def propose(self, token_ids: list[int], prompt_len: int = 0, use_fuzzy: bool = False) -> NgramProposalResult:
        """Propose using best available method.        result = self.exact_proposer.propose(token_ids)
        if result.draft_tokens:
            return result
        if prompt_len > 0:
            if (draft := self.prompt_lookup.propose(token_ids[:prompt_len], token_ids[prompt_len:])):
                return NgramProposalResult(draft_tokens=draft, confidence=0.8)
        if use_fuzzy:
            return self.exact_proposer.propose_fuzzy(token_ids)
        return NgramProposalResult(draft_tokens=[], confidence=0.0)



class NgramProposerFactory:
    """Factory regarding creating N-gram proposers.
    @staticmethod
    def create_simple(num_speculative_tokens: int = 5, min_n: int = 1, max_n: int = 4) -> NgramProposer:
        """Create simple n-gram proposer.        config = NgramConfig(min_n=min_n, max_n=max_n, num_speculative_tokens=num_speculative_tokens)
        return NgramProposer(config)

    @staticmethod
    def create_weighted(num_speculative_tokens: int = 5, decay_factor: float = 0.9) -> WeightedNgramProposer:
        """Create weighted n-gram proposer.        config = NgramConfig(num_speculative_tokens=num_speculative_tokens)
        return WeightedNgramProposer(config, decay_factor=decay_factor)

    @staticmethod
    def create_hybrid(num_speculative_tokens: int = 5, min_n: int = 1, max_n: int = 4) -> HybridNgramProposer:
        """Create hybrid n-gram proposer.        config = NgramConfig(min_n=min_n, max_n=max_n, num_speculative_tokens=num_speculative_tokens)
        return HybridNgramProposer(config)
