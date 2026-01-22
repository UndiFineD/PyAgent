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

<<<<<<< HEAD
"""
Core logic for multi-agent voting and consensus.
Supports weighted voting and tie-breaking algorithms.
"""

from __future__ import annotations

from typing import Dict, List, Optional

=======
from __future__ import annotations
from typing import List, Optional, Any, Dict
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ConsensusCore(BaseCore):
    """
    Standardized logic for multi-agent voting and consensus.
    Supports weighted voting and tie-breaking.
    """

<<<<<<< HEAD
    def __init__(self, name: str = "ConsensusCore", repo_root: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=repo_root)

    def calculate_winner(self, proposals: List[str], weights: Optional[List[float]] = None) -> str:
        """Determines the winning proposal based on voting rules."""
        if rc and hasattr(rc, "calculate_consensus_winner"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.calculate_consensus_winner(proposals, weights)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
=======
    def __init__(self, name: str = "ConsensusCore", root_path: Optional[str] = None) -> None:
        super().__init__(name=name, root_path=root_path)

    def calculate_winner(self, proposals: List[str], weights: Optional[List[float]] = None) -> str:
        """Determines the winning proposal based on voting rules."""
        if rc and hasattr(rc, "calculate_consensus_winner"):
            try:
                return rc.calculate_consensus_winner(proposals, weights)
            except Exception:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                pass

        if not proposals:
            return ""

        if weights and len(weights) != len(proposals):
            weights = None

        counts: Dict[str, float] = {}
        for idx, p in enumerate(proposals):
            weight = weights[idx] if weights else 1.0
            counts[p] = counts.get(p, 0.0) + weight

        # Strategy: Most weighted, then longest as tie-breaker (consistency)
        winner = sorted(counts.keys(), key=lambda x: (counts[x], len(x)), reverse=True)[0]
        return winner

    def get_agreement_score(self, proposals: List[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)
