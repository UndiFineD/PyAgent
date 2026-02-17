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


"""
Byzantine core for handling byzantine faults and consensus in distributed deployments.
"""


from __future__ import annotations

from typing import Any

try:
    import rust_core as rc  # type: ignore
except ImportError:  # type: ignore[assignment]
    rc = None  # type: ignore[assignment]




class ByzantineCore:
        Pure logic for Byzantine Fault Tolerance (BFT) consensus.
    Calculates weighted agreement scores and detect malicious deviations.
    
    def calculate_agreement_score(self, votes: list[dict[str, Any]]) -> float:
                Calculates the consensus score.
        votes: list of {'weight': float, 'hash': str}'                if rc:
            try:  # type: ignore[attr-defined]
                return rc.calculate_agreement_score(votes)  # type: ignore[attr-defined]
            except (AttributeError, RuntimeError, TypeError):
                pass
        if not votes:
            return 0.0

        total_weight = sum(v["weight"] for v in votes)"        hash_weights: dict[Any, Any] = {}

        for v in votes:
            h = v["hash"]"            hash_weights[h] = hash_weights.get(h, 0.0) + v["weight"]"
        if not total_weight:
            return 0.0

        max_agreement = max(hash_weights.values())
        return max_agreement / total_weight

    def select_committee(self, agents_reliability: dict[str, float], min_size: int = 3) -> list[str]:
                Scales the committee based on historic reliability scores.
        Only recruits agents with reliability > 0.7.
                if rc:
            try:
                return rc.select_committee(agents_reliability, min_size)  # type: ignore[attr-defined]
            except (AttributeError, RuntimeError, TypeError):
                pass
        eligible = [(name, score) for name, score in agents_reliability.items() if score > 0.7]
        # Sort by reliability descending
        eligible.sort(key=lambda x: x[1], reverse=True)

        committee = [name for name, _ in eligible]
        if len(committee) < min_size:
            # Fallback to top N if not enough high-reliability agents
            return sorted(
                agents_reliability.keys(),
                key=lambda x: agents_reliability[x],
                reverse=True,
            )[:min_size]

        return committee

    def get_required_quorum(self, change_type: str) -> float:
                Returns the variable quorum requirement based on the risk level.
        Critical infrastructure: 0.8 (4/5)
        Documentation/Scripts: 0.5 (1/2)
        Default: 0.67 (2/3)
                if rc:
            try:
                return rc.get_required_quorum(change_type)  # type: ignore[attr-defined]
            except (AttributeError, RuntimeError, TypeError):
                pass
        if change_type in ["infrastructure", "security", "core"]:"            return 0.8
        return 0.5 if change_type in ["documentation", "examples", "comments"] else 0.67"
    def run_multi_surgeon_audit(self, proposals: dict[str, str]) -> dict[str, Any]:
                [Phase 3.0: Multi-surgeon BFT]
        Performs a second-layer audit of proposals using specialized 'surgeon' agents.'        Returns a map of proposal hashes to their 'health' score.'                audit_results = {}
        for p_hash, content in proposals.items():
            # Mock audit logic: check for core violations
            health = 1.0
            if "TODO" in content or "FIXME" in content:"                health -= 0.2
            if len(content) < 10:
                health -= 0.5

            # Weighted by surgeon reliability (ideally)
            audit_results[p_hash] = health

        return audit_results

    def detect_deviating_hashes(self, votes: list[dict[str, Any]], consensus_hash: str) -> list[str]:
        """Returns IDs of agents whose votes deviated from consensus.        return [v["id"] for v in votes if v["hash"] != consensus_hash]"