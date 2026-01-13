
from __future__ import annotations
from typing import Dict, List
import json

class MorphologyCore:
    """
    MorphologyCore handles agent splitting, merging, and DNA encoding.
    It identifies logical overlap and proposes architectural shifts.
    """

    def calculate_path_overlap(self, path_a: List[str], path_b: List[str]) -> float:
        """
        Calculates Jaccard similarity between two agent logic paths.
        Overlap > 0.8 triggers a 'MERGE' proposal.
        """
        set_a, set_b = set(path_a), set(path_b)
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union

    def encode_agent_dna(self, name: str, tools: List[str], prompt: str, model: str) -> str:
        """
        Encodes the agent's DNA into a JSON string.
        """
        dna = {
            "name": name,
            "genome": {
                "tools": sorted(tools),
                "system_prompt_hash": hash(prompt),
                "preferred_model": model
            },
            "version": "1.0.DNA"
        }
        return json.dumps(dna)

    def propose_split(self, load_stats: Dict[str, float]) -> List[str]:
        """
        If an agent's load is too high, it proposes splitting into sub-specialists.
        """
        proposals = []
        for agent, load in load_stats.items():
            if load > 0.85:
                proposals.append(f"{agent}_Specialist_A")
                proposals.append(f"{agent}_Specialist_B")
        return proposals