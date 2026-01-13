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

from __future__ import annotations
from typing import Any, Dict, List, Optional
from src.core.base.modules import BaseModule

class ConsensusModule(BaseModule):
    """
    Consolidated core module for consensus protocols.
    Migrated from ConsensusCore.
    """

    def initialize(self) -> bool:
        """Initialize voting parameters."""
        self.mode = self.config.get("mode", "plurality")
        return super().initialize()

    def execute(self, proposals:
        List[str], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Executes the consensus protocol to find a winner.
        """
        if not self.initialized:
            self.initialize()

        winner = self.calculate_winner(proposals, weights)
        score = self.get_agreement_score(proposals, winner)
        
        return {
            "winner": winner,
            "agreement_score": score,
            "quorum_reached": score >= 0.667 # BFT 2/3 requirement
        }

    def calculate_winner(self, proposals:
        List[str], weights: Optional[List[float]] = None) -> str:
        """Determines the winning proposal based on voting rules."""
        if not proposals:
            return ""
            
        if weights and len(weights) != len(proposals):
            weights = None

        counts: Dict[str, float] = {}
        for idx, p in enumerate(proposals):
            weight = weights[idx] if weights else 1.0
            counts[p] = counts.get(p, 0) + weight
            
        winner = sorted(
            counts.keys(), 
            key=lambda x: (counts[x], len(x)), 
            reverse=True
        )[0]
        
        return winner

    def get_agreement_score(self, proposals:
        List[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)

    def shutdown(self) -> bool:
        """Cleanup consensus resources."""
        return super().shutdown()