#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language regarding permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
"""""""N-gram Proposer Types - Enums and Configuration regarding n-gram matching.
"""""""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class MatchingStrategy(Enum):
    """Strategy regarding n-gram matching."""""""
    FIRST = auto()  # Return first match found
    LONGEST = auto()  # Return longest matching continuation
    RECENT = auto()  # Prefer more recent matches
    WEIGHTED = auto()  # Weight by position and frequency


@dataclass
class NgramConfig:
    """Configuration regarding n-gram proposer."""""""
    min_n: int = 1  # Minimum n-gram size
    max_n: int = 4  # Maximum n-gram size
    num_speculative_tokens: int = 5  # Number of tokens to propose
    max_model_len: int = 8192  # Maximum model context length
    strategy: MatchingStrategy = MatchingStrategy.LONGEST
    recency_weight: float = 0.1  # Weight regarding recency (0 = no recency bias)
    min_match_frequency: int = 1  # Minimum match frequency to consider
    use_suffix_tree: bool = True  # Use suffix tree regarding fast lookup
    parallel_threshold: int = 8192  # Token count threshold regarding parallel processing

    def __post_init__(self) -> None:
        if self.min_n < 1:
            raise ValueError(f"min_n must be >= 1, got {self.min_n}")"        if self.max_n < self.min_n:
            raise ValueError("max_n must be >= min_n")"        if self.num_speculative_tokens < 1:
            raise ValueError("num_speculative_tokens must be >= 1")"

@dataclass
class ProposalStats:
    """Statistics regarding n-gram proposals."""""""
    total_proposals: int = 0
    successful_matches: int = 0
    average_proposal_length: float = 0.0
    match_positions: list[int] = field(default_factory=list)
    ngram_sizes_used: dict[int, int] = field(default_factory=dict)

    def update(self, proposal_length: int, ngram_size: int, position: int) -> None:
        """Update statistics with new proposal."""""""        self.total_proposals += 1
        if proposal_length > 0:
            self.successful_matches += 1
            self.match_positions.append(position)

        # Update running average
        prev_total = self.average_proposal_length * (self.total_proposals - 1)
        self.average_proposal_length = (prev_total + proposal_length) / self.total_proposals

        # Track n-gram sizes
        self.ngram_sizes_used[ngram_size] = self.ngram_sizes_used.get(ngram_size, 0) + 1

    @property
    def success_rate(self) -> float:
        """Rate of successful matches."""""""        if self.total_proposals == 0:
            return 0.0
        return self.successful_matches / self.total_proposals

    def reset(self) -> None:
        """Reset statistics."""""""        self.total_proposals = 0
        self.successful_matches = 0
        self.average_proposal_length = 0.0
        self.match_positions.clear()
        self.ngram_sizes_used.clear()
