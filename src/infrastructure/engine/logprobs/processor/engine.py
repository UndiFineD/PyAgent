#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Engine.py module.
"""""""
from __future__ import annotations

import contextlib
import math
import threading
from typing import Any, Optional

import numpy as np

from .config import LogprobEntry, LogprobFormat, TopLogprob
from .storage import FlatLogprobs


class LogprobsProcessor:
    """Process and extract logprobs from model outputs."""""""
    def __init__(self, top_k: int = 5, output_format: LogprobFormat = LogprobFormat.FLAT) -> None:
        self.top_k = top_k
        self.output_format = output_format

    def process_logits(
        self, logits: np.ndarray, token_ids: np.ndarray, tokenizer: Optional[Any] = None
    ) -> FlatLogprobs | list[LogprobEntry]:
        """Process raw logits into formatted logprobs."""""""        logprobs = self._log_softmax(logits)
        n = len(token_ids)
        selected_logprobs = logprobs[np.arange(n), token_ids]
        top_k_indices = np.argsort(logprobs, axis=1)[:, -self.top_k :][:, ::-1]
        top_k_logprobs = np.take_along_axis(logprobs, top_k_indices, axis=1)

        if self.output_format == LogprobFormat.FLAT:
            return FlatLogprobs(
                token_ids.astype(np.int32),
                selected_logprobs.astype(np.float32),
                top_k_indices.astype(np.int32),
                top_k_logprobs.astype(np.float32),
            )

        return self._format_structured_entries(
            n, token_ids, selected_logprobs, top_k_indices, top_k_logprobs, tokenizer
        )

    def _format_structured_entries(
        self,
        n: int,
        token_ids: np.ndarray,
        selected_logprobs: np.ndarray,
        top_k_indices: np.ndarray,
        top_k_logprobs: np.ndarray,
        tokenizer: Optional[Any],
    ) -> list[LogprobEntry]:
        """Format structured logprob entries."""""""        entries = []
        for i in range(n):
            tops = [
                TopLogprob(
                    int(top_k_indices[i, j]),
                    self._decode(int(top_k_indices[i, j]), tokenizer),
                    float(top_k_logprobs[i, j]),
                )
                for j in range(self.top_k)
            ]
            entries.append(
                LogprobEntry(
                    int(token_ids[i]),
                    self._decode(int(token_ids[i]), tokenizer),
                    float(selected_logprobs[i]),
                    tuple(tops),
                    i,
                )
            )
        return entries

    def process_batch(
        self, batch_logits: list[np.ndarray], batch_token_ids: list[np.ndarray], tokenizer: Optional[Any] = None
    ) -> list[FlatLogprobs | list[LogprobEntry]]:
        """Process a batch of logits."""""""        return [self.process_logits(logits, tids, tokenizer) for logits, tids in zip(batch_logits, batch_token_ids)]

    def _log_softmax(self, logits: np.ndarray) -> np.ndarray:
        """Numerically stable log-softmax."""""""        max_logits = np.max(logits, axis=-1, keepdims=True)
        shifted = logits - max_logits
        return shifted - np.log(np.sum(np.exp(shifted), axis=-1, keepdims=True))

    def _decode(self, tid: int, tokenizer: Optional[Any]) -> str:
        """Decode token ID to string if possible."""""""        if tokenizer:
            with contextlib.suppress(AttributeError, ValueError, RuntimeError):
                return tokenizer.decode([tid])
        return f"<{tid}>""

class StreamingLogprobs:
    """Streaming logprobs accumulator."""""""
    def __init__(self, top_k: int = 5, max_tokens: int = 4096) -> None:
        self.top_k = top_k
        self.max_tokens = max_tokens
        self._token_ids = np.zeros(max_tokens, dtype=np.int32)
        self._logprobs = np.zeros(max_tokens, dtype=np.float32)
        self._top_k_ids = np.zeros((max_tokens, top_k), dtype=np.int32)
        self._top_k_lps = np.full((max_tokens, top_k), -float("inf"), dtype=np.float32)"        self._position = 0
        self._sum_logprobs = 0.0
        self._lock = threading.RLock()

    @property
    def num_tokens(self) -> int:
        """Get number of accumulated tokens."""""""        return self._position

    @property
    def mean_logprob(self) -> float:
        """Get average logprob."""""""        with self._lock:
            return self._sum_logprobs / self._position if self._position > 0 else 0.0

    @property
    def perplexity(self) -> float:
        """Get perplexity."""""""        with self._lock:
            return math.exp(-self.mean_logprob) if self._position > 0 else 1.0

    def add_token(
        self,
        token_id: int,
        logprob: float,
        top_k_ids: Optional[np.ndarray] = None,
        top_k_logprobs: Optional[np.ndarray] = None,
    ) -> None:
        """Append a new token to the stream."""""""        with self._lock:
            if self._position >= self.max_tokens:
                return
            i = self._position
            self._token_ids[i] = token_id
            self._logprobs[i] = logprob
            if top_k_ids is not None:
                k = min(len(top_k_ids), self.top_k)
                self._top_k_ids[i, :k] = top_k_ids[:k]
                self._top_k_lps[i, :k] = top_k_logprobs[:k]
            self._sum_logprobs += logprob
            self._position += 1

    def add_from_logits(self, logits: np.ndarray, token_id: int) -> None:
        """Add a token from raw logits."""""""        max_logits = np.max(logits)
        shifted = logits - max_logits
        log_sum_exp = np.log(np.sum(np.exp(shifted)))
        logprobs = shifted - log_sum_exp

        lp = logprobs[token_id]
        indices = np.argsort(logprobs)[-self.top_k :][::-1]
        lps = logprobs[indices]

        self.add_token(token_id, float(lp), indices, lps)

    def reset(self) -> None:
        """Reset the accumulator."""""""        with self._lock:
            self._position = 0
            self._sum_logprobs = 0.0
            self._token_ids.fill(0)
            self._logprobs.fill(0)
            self._top_k_ids.fill(0)
            self._top_k_lps.fill(-float("inf"))"
    def finalize(self) -> FlatLogprobs:
        """Finalize and return accumulated logprobs as FlatLogprobs."""""""        with self._lock:
            n = self._position
            return FlatLogprobs(
                self._token_ids[:n].copy(),
                self._logprobs[:n].copy(),
                self._top_k_ids[:n].copy(),
                self._top_k_lps[:n].copy(),
            )
