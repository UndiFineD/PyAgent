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
Storage.py module.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence

import numpy as np

from .config import LogprobEntry, TopLogprob


@dataclass
class FlatLogprobs:
    """GC-optimized flat logprobs storage."""

    token_ids: np.ndarray
    logprobs: np.ndarray
    top_k_token_ids: np.ndarray
    top_k_logprobs: np.ndarray
    _token_strs: Optional[List[str]] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        assert len(self.token_ids.shape) == 1
        assert len(self.logprobs.shape) == 1
        assert self.token_ids.shape[0] == self.logprobs.shape[0]
        if len(self.top_k_token_ids.shape) == 2:
            assert self.top_k_token_ids.shape[0] == self.token_ids.shape[0]
            assert self.top_k_logprobs.shape == self.top_k_token_ids.shape

    @property
    def num_tokens(self) -> int:
        """Get number of tokens."""
        return len(self.token_ids)

    @property
    def top_k(self) -> int:
        """Get number of top-k entries per token."""
        if len(self.top_k_token_ids.shape) == 2:
            return self.top_k_token_ids.shape[1]
        return 0

    @property
    def memory_bytes(self) -> int:
        """Estimate memory usage in bytes."""
        return self.token_ids.nbytes + self.logprobs.nbytes + self.top_k_token_ids.nbytes + self.top_k_logprobs.nbytes

    def slice(self, start: int, end: int) -> "FlatLogprobs":
        """Slice the logprobs."""
        return FlatLogprobs(
            self.token_ids[start:end],
            self.logprobs[start:end],
            self.top_k_token_ids[start:end],
            self.top_k_logprobs[start:end],
        )

    def append(self, other: "FlatLogprobs") -> "FlatLogprobs":
        """Concatenate with another FlatLogprobs instance."""
        return FlatLogprobs(
            np.concatenate([self.token_ids, other.token_ids]),
            np.concatenate([self.logprobs, other.logprobs]),
            np.concatenate([self.top_k_token_ids, other.top_k_token_ids]),
            np.concatenate([self.top_k_logprobs, other.top_k_logprobs]),
        )

    def mean_logprob(self) -> float:
        """Compute mean logprob."""
        return float(np.mean(self.logprobs)) if self.logprobs.size > 0 else 0.0

    def perplexity(self) -> float:
        """Compute perplexity."""
        return float(np.exp(-np.mean(self.logprobs))) if self.logprobs.size > 0 else 1.0

    @classmethod
    def empty(cls, top_k: int = 5) -> "FlatLogprobs":
        """Create an empty FlatLogprobs instance."""
        return cls(
            np.array([], dtype=np.int32),
            np.array([], dtype=np.float32),
            np.zeros((0, top_k), dtype=np.int32),
            np.zeros((0, top_k), dtype=np.float32),
        )

    @classmethod
    def from_entries(cls, entries: Sequence[LogprobEntry], top_k: int = 5) -> "FlatLogprobs":
        """Create from a sequence of LogprobEntry objects."""
        n = len(entries)
        token_ids = np.zeros(n, dtype=np.int32)
        logprobs = np.zeros(n, dtype=np.float32)
        top_k_ids = np.zeros((n, top_k), dtype=np.int32)
        top_k_lps = np.full((n, top_k), -float("inf"), dtype=np.float32)

        for i, entry in enumerate(entries):
            token_ids[i] = entry.token_id
            logprobs[i] = entry.logprob
            for j, top in enumerate(entry.top_logprobs[:top_k]):
                top_k_ids[i, j] = top.token_id
                top_k_lps[i, j] = top.logprob
        return cls(token_ids, logprobs, top_k_ids, top_k_lps)

    def to_entries(self, tokenizer: Optional[Any] = None) -> List[LogprobEntry]:
        """Convert back to list of LogprobEntry objects."""
        entries = []
        for i in range(self.num_tokens):
            top_logprobs = []
            for j in range(self.top_k):
                if self.top_k_logprobs[i, j] > -float("inf"):
                    tid = int(self.top_k_token_ids[i, j])
                    decoded = self._decode(tid, tokenizer)
                    top_logprobs.append(TopLogprob(tid, decoded, float(self.top_k_logprobs[i, j])))
            tid = int(self.token_ids[i])
            entries.append(
                LogprobEntry(tid, self._decode(tid, tokenizer), float(self.logprobs[i]), tuple(top_logprobs), i)
            )
        return entries

    def _decode(self, tid: int, tokenizer: Optional[Any]) -> str:
        """Decode token ID to string if possible."""
        if tokenizer:
            with contextlib.suppress(AttributeError, ValueError, RuntimeError):
                return tokenizer.decode([tid])
        return f"<{tid}>"

    def entropy_per_token(self) -> np.ndarray:
        """Compute Shannon entropy for each token distribution."""
        max_lps = np.max(self.top_k_logprobs, axis=1, keepdims=True)
        exp_lps = np.exp(self.top_k_logprobs - max_lps)
        probs = exp_lps / np.sum(exp_lps, axis=1, keepdims=True)
        log_probs = np.log(probs + 1e-10)
        return (-np.sum(probs * log_probs, axis=1)).astype(np.float32)
