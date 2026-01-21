# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Beam search implementation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import numpy as np
from .params import SamplingParams, SamplingState
from .base import Sampler, HAS_RUST, _log_softmax

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
        return len(self.token_ids)

    def normalized_score(self, length_penalty: float = 1.0) -> float:
        if self.length == 0: return self.score
        if HAS_RUST: return beam_score_rust(self.score, self.length, length_penalty)
        return self.score / (self.length ** length_penalty)

    def extend(self, token_id: int, log_prob: float) -> "BeamHypothesis":
        return BeamHypothesis(
            token_ids=self.token_ids + [token_id],
            score=self.score + log_prob,
            finished=False,
        )

    def finish(self) -> "BeamHypothesis":
        return BeamHypothesis(
            token_ids=self.token_ids,
            score=self.score,
            finished=True,
        )


class BeamSearchSampler(Sampler):
    """Beam search sampler."""
    def __init__(self, config: Optional[BeamSearchConfig] = None):
        self.config = config or BeamSearchConfig()
        self._beams: List[BeamHypothesis] = []
        self._finished_beams: List[BeamHypothesis] = []

    def reset(self) -> None:
        self._beams = [BeamHypothesis()]
        self._finished_beams = []

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        return logits

    def step(
        self,
        logits: np.ndarray,
        eos_token_id: Optional[int] = None,
    ) -> List[BeamHypothesis]:
        if not self._beams: self.reset()
        log_probs = _log_softmax(logits)
        candidates: List[Tuple[float, int, BeamHypothesis]] = []
        
        for beam_idx, beam in enumerate(self._beams):
            if beam.finished: continue
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
        self._beams = [c[2] for c in candidates[:self.config.beam_width]]
        return self._beams

    def get_best_hypothesis(self) -> Optional[BeamHypothesis]:
        all_beams = self._finished_beams + self._beams
        if not all_beams: return None
        return sorted(all_beams, key=lambda b: b.normalized_score(self.config.length_penalty), reverse=True)[0]

    def is_finished(self) -> bool:
        if self.config.early_stopping: return all(b.finished for b in self._beams)
        return len(self._finished_beams) >= self.config.beam_width
