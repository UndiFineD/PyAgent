
"""
Core logic for Evolutionary Hyper-Parameter Tuning (Phase 182).
Handles prompt crossover and lineage persistence.
"""

import hashlib
import random




class EvolutionCore:
    """Core logic for evolutionary algorithms in prompt engineering."""
    @staticmethod
    def prompt_crossover(prompt1: str, prompt2: str) -> str:
        """
        Combines two prompts by interweaving their logical blocks.
        """
        lines1 = prompt1.splitlines()
        lines2 = prompt2.splitlines()

        # Take halves or interweave
        mid1 = len(lines1) // 2
        mid2 = len(lines2) // 2

        child_lines = lines1[:mid1] + lines2[mid2:]
        return "\n".join(child_lines)

    @staticmethod
    def calculate_prompt_sha(prompt: str) -> str:
        """
        Returns a short SHA hash of the prompt for lineage tracking.
        """
        return hashlib.sha256(prompt.encode()).hexdigest()[:12]

    @staticmethod
    def mutate_prompt(prompt: str, mutation_rate: float = 0.1) -> str:
        """
        Randomly injects keywords or modifies tone.
        """
        modifiers = ["be more precise", "explain reasoning", "be concise", "check for security"]
        if random.random() < mutation_rate:
            return prompt + f"\n[Mutation: {random.choice(modifiers)}]"
        return prompt
