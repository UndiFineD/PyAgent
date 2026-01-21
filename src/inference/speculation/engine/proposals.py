# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Data structures for speculative decoding proposals and results."""

from dataclasses import dataclass, field
from typing import Any, List, Optional
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
        if not self.total_proposed:
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
        if not self.num_draft_tokens:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens

    @property
    def draft_efficiency(self) -> float:
        """Tokens emitted per draft token (higher is better)."""
        if not self.num_draft_tokens:
            return 0.0
        return self.num_emitted_tokens / self.num_draft_tokens

    def position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate for a specific position."""
        if position >= len(self.position_proposed) or not self.position_proposed[position]:
            return 0.0
        return self.position_accepted[position] / self.position_proposed[position]

    def update(self, verification_result: VerificationResult) -> None:
        """Update metrics from a verification result."""
        self.num_draft_tokens += verification_result.total_proposed
        self.num_accepted_tokens += verification_result.total_accepted
        self.num_proposals += 1
        self.total_verification_time_ms += verification_result.verification_time_ms
