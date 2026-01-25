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
Base classes and utilities for sampling.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from .params import SamplingParams, SamplingState

# Try to import Rust accelerations
try:
    from rust_core import (beam_score_rust, compute_penalties_rust,
                           gumbel_sample_rust, top_k_mask_rust,
                           top_p_mask_rust)

    HAS_RUST = True
except ImportError:
    top_k_mask_rust = None
    top_p_mask_rust = None
    gumbel_sample_rust = None
    beam_score_rust = None
    compute_penalties_rust = None
    HAS_RUST = False

__all__ = [
    "Sampler",
    "HAS_RUST",
    "top_k_mask_rust",
    "top_p_mask_rust",
    "gumbel_sample_rust",
    "beam_score_rust",
    "compute_penalties_rust",
]


class Sampler(ABC):
    """
    Abstract base class for sampling strategies.
    """

    @abstractmethod
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """
        Transform or filter logits.
        """

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """
        Sample token IDs from logits.
        """
        processed = self.forward(logits, params, state)
        return self._sample_from_logits(processed, state)

    def _sample_from_logits(
        self,
        logits: np.ndarray,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Sample token IDs from processed logits using softmax + multinomial."""
        probs = _softmax(logits)
        batch_size = probs.shape[0]
        samples = np.zeros(batch_size, dtype=np.int64)

        for i in range(batch_size):
            if state and state.rng:
                samples[i] = state.rng.choice(len(probs[i]), p=probs[i])
            else:
                samples[i] = np.random.choice(len(probs[i]), p=probs[i])

        return samples


def _softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp_logits = np.exp(shifted)
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def _log_softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable log softmax."""
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=-1, keepdims=True))


def _sample_from_probs(
    probs: np.ndarray,
    state: Optional[SamplingState] = None,
) -> np.ndarray:
    """Sample token IDs from probability distribution."""
    batch_size = probs.shape[0]
    samples = np.zeros(batch_size, dtype=np.int64)

    for i in range(batch_size):
        if state and state.rng:
            samples[i] = state.rng.choice(len(probs[i]), p=probs[i])
        else:
            samples[i] = np.random.choice(len(probs[i]), p=probs[i])

    return samples
