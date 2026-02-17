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
# See the License for the specific language governing permissions and
# limitations under the License.


Config.py module.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SpecMethod(str, Enum):
    """Speculative decoding method.
    NGRAM = "ngram""    SUFFIX = "suffix""    DRAFT_MODEL = "draft_model""    EAGLE = "eagle""    MEDUSA = "medusa""

@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding.
    method: SpecMethod = SpecMethod.NGRAM
    num_speculative_tokens: int = 5

    # N-gram specific
    prompt_lookup_min: int = 3
    prompt_lookup_max: int = 5

    # Suffix specific
    max_tree_depth: int = 24
    max_cached_requests: int = 10000
    max_spec_factor: float = 1.0
    min_token_prob: float = 0.1

    # Draft model specific
    draft_model: str | None = None
    draft_tensor_parallel_size: int = 1

    # General
    disable_by_batch_size: int | None = None
    temperature: float = 0.0

    def should_disable(self, batch_size: int) -> bool:
        """Check if spec decoding should be disabled for batch size.        if self.disable_by_batch_size is None:
            return False
        return batch_size >= self.disable_by_batch_size


@dataclass
class DraftProposal:
    """A batch of draft tokens proposed by speculator.
    request_id: str
    token_ids: list[int]
    logprobs: list[float] | None = None
    parent_indices: list[int] | None = None  # For tree speculation

    @property
    def num_tokens(self) -> int:
        """Return number of tokens in draft.        return len(self.token_ids)

    def is_empty(self) -> bool:
        """Check if draft is empty.        return not self.token_ids


@dataclass
class VerificationResult:
    """Result of verifying draft tokens against target model.
    request_id: str
    num_draft_tokens: int
    num_accepted_tokens: int
    accepted_token_ids: list[int]
    rejected_at_position: int | None = None
    bonus_token_id: int | None = None  # Token sampled after rejection

    @property
    def acceptance_rate(self) -> float:
        """Calculate verification acceptance rate.        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens

    @property
    def all_accepted(self) -> bool:
        """Check if all draft tokens were accepted.        return self.num_accepted_tokens == self.num_draft_tokens


@dataclass
class SpecDecodingMetrics:
    """Metrics for speculative decoding performance.
    num_drafts: int = 0
    num_draft_tokens: int = 0
    num_accepted_tokens: int = 0
    num_rejected_tokens: int = 0
    accepted_per_position: list[int] = field(default_factory=list)

    # Timing
    proposal_time_ms: float = 0.0
    verification_time_ms: float = 0.0

    def __post_init__(self) -> None:
        if not self.accepted_per_position:
            self.accepted_per_position = []

    @classmethod
    def new(cls, num_spec_tokens: int) -> SpecDecodingMetrics:
        """Create new metrics with position tracking.        return cls(accepted_per_position=[0] * num_spec_tokens)

    def observe_draft(
        self,
        num_draft_tokens: int,
        num_accepted_tokens: int,
        accepted_positions: list[int] | None = None,
    ) -> None:
        """Record a draft verification result.        self.num_drafts += 1
        self.num_draft_tokens += num_draft_tokens
        self.num_accepted_tokens += num_accepted_tokens
        self.num_rejected_tokens += num_draft_tokens - num_accepted_tokens

        if accepted_positions:
            for pos in accepted_positions:
                if pos < len(self.accepted_per_position):
                    self.accepted_per_position[pos] += 1

    @property
    def acceptance_rate(self) -> float:
        """Calculate overall acceptance rate.        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens

    @property
    def avg_accepted_per_draft(self) -> float:
        """Calculate average accepted tokens per draft.        if self.num_drafts == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_drafts

    @property
    def position_acceptance_rates(self) -> list[float]:
        """Acceptance rate per draft position.        if self.num_drafts == 0:
            return [0.0] * len(self.accepted_per_position)
        return [count / self.num_drafts for count in self.accepted_per_position]

    def reset(self) -> None:
        """Reset all metrics.        self.num_drafts = 0
        self.num_draft_tokens = 0
        self.num_accepted_tokens = 0
        self.num_rejected_tokens = 0
        self.accepted_per_position = [0] * len(self.accepted_per_position)
        self.proposal_time_ms = 0.0
        self.verification_time_ms = 0.0

    def as_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary.        return {
            "num_drafts": self.num_drafts,"            "num_draft_tokens": self.num_draft_tokens,"            "num_accepted_tokens": self.num_accepted_tokens,"            "num_rejected_tokens": self.num_rejected_tokens,"            "acceptance_rate": self.acceptance_rate,"            "avg_accepted_per_draft": self.avg_accepted_per_draft,"            "position_acceptance_rates": self.position_acceptance_rates,"            "proposal_time_ms": self.proposal_time_ms,"            "verification_time_ms": self.verification_time_ms,"        }
