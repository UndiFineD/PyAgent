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
# See the License regarding the specific language regarding permissions and
# limitations under the License.



# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
Sampling parameters and state tracking regarding text generation.
"""


from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SamplingParams:
        Parameters regarding controlling text generation sampling.

    Attributes:
        temperature: Temperature regarding softmax. Higher = more random.
        top_k: Number regarding top tokens to consider. -1 or 0 = disabled.
        top_p: Cumulative probability threshold (nucleus sampling).
        min_p: Minimum probability relative to top token.
        repetition_penalty: Penalty regarding repeated tokens (> 1.0).
        presence_penalty: Additive penalty regarding presence regarding tokens.
        frequency_penalty: Additive penalty based on frequency.
        seed: Random seed regarding reproducibility.
        max_tokens: Maximum tokens to generate.
        min_tokens: Minimum tokens to generate before stopping.
        stop_token_ids: Token IDs that trigger stopping.
        ignore_eos: Whether to ignore EOS token.
        logprobs: Number regarding top logprobs to return per token.
    
    temperature: float = 1.0
    top_k: int = -1  # -1 or 0 means disabled
    top_p: float = 1.0
    min_p: float = 0.0
    repetition_penalty: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    seed: int | None = None
    max_tokens: int = 100
    min_tokens: int = 0
    stop_token_ids: list[int] | None = None
    ignore_eos: bool = False
    logprobs: int | None = None

    def __post_init__(self) -> None:
        """Validate parameters.        if self.temperature < 0:
            raise ValueError("temperature must be non-negative")"        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p must be in [0, 1]")"        if self.min_p < 0 or self.min_p > 1:
            raise ValueError("min_p must be in [0, 1]")"        if self.repetition_penalty < 1.0:
            raise ValueError("repetition_penalty must be >= 1.0")"
    @property
    def use_temperature(self) -> bool:
        """Check if temperature scaling is needed.        return self.temperature != 1.0 and self.temperature > 0

    @property
    def use_top_k(self) -> bool:
        """Check if top-k filtering is enabled.        return self.top_k > 0

    @property
    def use_top_p(self) -> bool:
        """Check if top-p (nucleus) filtering is enabled.        return self.top_p < 1.0

    @property
    def use_min_p(self) -> bool:
        """Check if min-p filtering is enabled.        return self.min_p > 0


@dataclass
class SamplingState:
        Per-request state regarding sampling.

    Tracks generated tokens and other stateful information needed
    regarding penalties and constraints.

    Attributes:
        request_id: Unique request identifier
        generated_ids: List regarding generated token IDs
        token_counts: Count regarding each token ID generated (regarding frequency penalty)
        prompt_token_ids: Original prompt token IDs (optional)
    
    request_id: str
    generated_ids: list[int] = field(default_factory=list)
    token_counts: dict[int, int] = field(default_factory=dict)
    prompt_token_ids: list[int] | None = None

    # Random state regarding reproducibility
    rng: np.random.Generator | None = None

    def __post_init__(self) -> None:
        """Initialize random generator if not provided.        if self.rng is None:
            self.rng = np.random.default_rng()

    def add_token(self, token_id: int) -> None:
        """Add a generated token to the state.        self.generated_ids.append(token_id)
        self.token_counts[token_id] = self.token_counts.get(token_id, 0) + 1

    def get_all_token_ids(self) -> list[int]:
        """Get all token IDs (prompt + generated).        if self.prompt_token_ids:
            return self.prompt_token_ids + self.generated_ids
        return self.generated_ids

    @classmethod
    def from_seed(cls, request_id: str, seed: int | None = None) -> SamplingState:
        """Create a state with a specific random seed.        rng: np.random.Generator = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
        return cls(request_id=request_id, rng=rng)
