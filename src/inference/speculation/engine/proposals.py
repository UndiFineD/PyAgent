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
"""Data structures for speculative decoding proposals and results."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

from .config import SpecMethod


@dataclass
class DraftProposal:
    """Represents a batch of draft token proposals."""

    # [batch_size, num_speculative_tokens]
    draft_token_ids: List[List[int]] = field(default_factory=list)

    # Optional: [batch_size, num_speculative_tokens, vocab_size]
    draft_logprobs: Optional[Any] = None

    # Number of tokens proposed per request
    num_proposed: List[int] = field(default_factory=list)

    # Proposal metadata
    proposal_time_ms: float = 0.0
    method_used: SpecMethod = SpecMethod.NGRAM


@dataclass
class VerificationResult:
    """Result of draft token verification."""

    # [batch_size] - number of accepted tokens per request
    num_accepted: List[int] = field(default_factory=list)

    # [batch_size, max_accepted] - accepted token IDs
    accepted_token_ids: List[List[int]] = field(default_factory=list)

    # Per-position acceptance statistics
    position_acceptance_rates: List[float] = field(default_factory=list)

    # Verification metadata
    verification_time_ms: float = 0.0
    total_proposed: int = 0
    total_accepted: int = 0

    @property
    def acceptance_rate(self) -> float:
        """Overall acceptance rate."""
        if self.total_proposed == 0:
            return 0.0
        return self.total_accepted / self.total_proposed


@dataclass
class SpecDecodingMetrics:
    """Metrics for speculative decoding performance."""

    num_draft_tokens: int = 0
    num_accepted_tokens: int = 0
    num_emitted_tokens: int = 0
    num_proposals: int = 0

    # Per-position statistics
    position_accepted: List[int] = field(default_factory=list)
    position_proposed: List[int] = field(default_factory=list)

    # Timing
    total_proposal_time_ms: float = 0.0
    total_verification_time_ms: float = 0.0

    @property
    def acceptance_rate(self) -> float:
<<<<<<< HEAD
        if self.num_draft_tokens == 0:
=======
        """Calculate the acceptance rate of draft tokens."""
        if not self.num_draft_tokens:
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens

    @property
    def draft_efficiency(self) -> float:
        """Tokens emitted per draft token (higher is better)."""
        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_emitted_tokens / self.num_draft_tokens

    def position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate for a specific position."""
        if position >= len(self.position_proposed) or self.position_proposed[position] == 0:
            return 0.0
        return self.position_accepted[position] / self.position_proposed[position]

    def update(self, verification_result: VerificationResult) -> None:
        """Update metrics from a verification result."""
        self.num_draft_tokens += verification_result.total_proposed
        self.num_accepted_tokens += verification_result.total_accepted
        self.num_proposals += 1
        self.total_verification_time_ms += verification_result.verification_time_ms
