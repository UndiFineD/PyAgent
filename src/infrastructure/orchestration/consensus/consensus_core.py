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
ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.
"""

from __future__ import annotations
from typing import Any
from src.core.base.version import VERSION

try:
    import rust_core as rc
except (ImportError, AttributeError):
    rc: Any = None  # type: ignore[no-redef]

__version__ = VERSION


class ConsensusCore:
    """Pure logic core for consensus protocols."""

    def __init__(self, mode: str = "plurality") -> None:
        self.mode = mode

    def calculate_winner(
        self, proposals: list[str], weights: list[float] | None = None
    ) -> str:
        """
        Determines the winning proposal based on voting rules.
        Phase 119: Supports weighted voting based on agent reliability.
        """
        if rc:
            try:
                return rc.calculate_consensus_winner(proposals, weights)  # type: ignore[attr-defined]
            except (ImportError, AttributeError):
                pass

        if not proposals:
            return ""

        if weights and len(weights) != len(proposals):
            weights = None  # Fallback to unweighted if mismatch

        # Count identical proposals with weights
        counts: dict[str, float] = {}
        for idx, p in enumerate(proposals):
            weight = weights[idx] if weights else 1.0
            counts[p] = counts.get(p, 0) + weight

        # Strategy: Most weighted, then longest as tie-breaker
        winner = sorted(counts.keys(), key=lambda x: (counts[x], len(x)), reverse=True)[
            0
        ]

        return winner

    def get_agreement_score(self, proposals: list[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)
