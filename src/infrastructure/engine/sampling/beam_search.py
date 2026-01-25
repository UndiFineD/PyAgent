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
"""
Beam search implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np

from .base import HAS_RUST, Sampler, _log_softmax
from .params import SamplingParams, SamplingState

try:
    from rust_core import beam_score_rust
except ImportError:
    pass


@dataclass
class BeamSearchConfig:
    """Configuration for beam search."""

    beam_width: int = 4
    length_penalty: float = 1.0
    early_stopping: bool = True
    max_tokens: int = 100


@dataclass
class BeamHypothesis:
    """A hypothesis in beam search."""

    token_ids: List[int] = field(default_factory=list)
    score: float = 0.0
    finished: bool = False

    @property
    def length(self) -> int:
        """Get the length of the hypothesis."""
        return len(self.token_ids)

    def normalized_score(self, length_penalty: float = 1.0) -> float:
        """Get the score normalized by length."""
        if self.length == 0:
            return self.score
        if HAS_RUST:
            return beam_score_rust(self.score, self.length, length_penalty)
        return self.score / (self.length**length_penalty)

    def extend(self, token_id: int, log_prob: float) -> "BeamHypothesis":
        """Extend hypothesis with a new token."""
        return BeamHypothesis(
            token_ids=self.token_ids + [token_id],
            score=self.score + log_prob,
            finished=False,
        )

    def finish(self) -> "BeamHypothesis":
        """Mark the hypothesis as finished."""
        return BeamHypothesis(
            token_ids=self.token_ids,
            score=self.score,
            finished=True,
        )


class BeamSearchSampler(Sampler):
    """Beam search sampler."""

    def __init__(self, config: Optional[BeamSearchConfig] = None):
        """Initialize beam search."""
        self.config = config or BeamSearchConfig()
        self._beams: List[BeamHypothesis] = []
        self._finished_beams: List[BeamHypothesis] = []

    def reset(self) -> None:
        """Reset beam search state."""
        self._beams = [BeamHypothesis()]
        self._finished_beams = []

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Process logits."""
        return logits

    def step(
        self,
        logits: np.ndarray,
        eos_token_id: Optional[int] = None,
    ) -> List[BeamHypothesis]:
        """Perform one beam search step."""
        if not self._beams:
            self.reset()
        log_probs = _log_softmax(logits)
        candidates: List[Tuple[float, int, BeamHypothesis]] = []

        for beam_idx, beam in enumerate(self._beams):
            if beam.finished:
                continue
            beam_log_probs = log_probs[beam_idx] if len(log_probs) > beam_idx else log_probs[0]
            top_k = min(self.config.beam_width * 2, len(beam_log_probs))
            top_indices = np.argpartition(beam_log_probs, -top_k)[-top_k:]

            for token_id in top_indices:
                log_prob = float(beam_log_probs[token_id])
                new_beam = beam.extend(token_id, log_prob)
                if eos_token_id is not None and token_id == eos_token_id:
                    self._finished_beams.append(new_beam.finish())
                else:
                    score = new_beam.normalized_score(self.config.length_penalty)
                    candidates.append((score, len(candidates), new_beam))

        candidates.sort(key=lambda x: -x[0])
        self._beams = [c[2] for c in candidates[: self.config.beam_width]]
        return self._beams

    def get_best_hypothesis(self) -> Optional[BeamHypothesis]:
        """Get the highest scoring hypothesis."""
        all_beams = self._finished_beams + self._beams
        if not all_beams:
            return None
        return sorted(all_beams, key=lambda b: b.normalized_score(self.config.length_penalty), reverse=True)[0]

    def is_finished(self) -> bool:
        """Check if beam search is finished."""
        if self.config.early_stopping:
            return all(b.finished for b in self._beams)
        return len(self._finished_beams) >= self.config.beam_width
