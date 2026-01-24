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
Morphology core.py module.
"""

from __future__ import annotations

import json

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class MorphologyCore:
    """
    MorphologyCore handles agent splitting, merging, and DNA encoding.
    It identifies logical overlap and proposes architectural shifts.
    """

    def calculate_path_overlap(self, path_a: list[str], path_b: list[str]) -> float:
        """
        Calculates Jaccard similarity between two agent logic paths.
        Overlap > 0.8 triggers a 'MERGE' proposal.
        """
        # Rust-accelerated Jaccard similarity
        if HAS_RUST:
            try:
                return rc.calculate_jaccard_set_rust(path_a, path_b)  # type: ignore[attr-defined]
            except Exception:
                pass
        set_a, set_b = set(path_a), set(path_b)
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union

    def encode_agent_dna(self, name: str, tools: list[str], prompt: str, model: str) -> str:
        """
        Encodes the agent's DNA into a JSON string.
        """
        dna = {
            "name": name,
            "genome": {
                "tools": sorted(tools),
                "system_prompt_hash": hash(prompt),
                "preferred_model": model,
            },
            "version": "1.0.DNA",
        }
        return json.dumps(dna)

    def propose_split(self, load_stats: dict[str, float]) -> list[str]:
        """
        If an agent's load is too high, it proposes splitting into sub-specialists.
        """
        proposals = []
        for agent, load in load_stats.items():
            if load > 0.85:
                proposals.append(f"{agent}_Specialist_A")
                proposals.append(f"{agent}_Specialist_B")
        return proposals
