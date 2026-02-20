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
"""
Evolutionary Prompt Agent - Genetic optimization of agent prompts

"""

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: EvolutionaryPromptAgent(file_path: str)
- Initialize population: initialize_population(seed_prompt: str) -> str
- Record fitness: record_fitness(prompt_index: int, score: float) -> str
- Evolve generation: evolve_generation() -> dict[str, Any]
- Retrieve best prompt: get_best_prompt() -> str
- (Intended) update deployed agents' prompts: update_all_agent_prompts() -> dict[str, Any]'
WHAT IT DOES:
Implements an evolutionary/genetic approach to optimize system prompts by maintaining a population of prompt variations, recording fitness scores from task performance, and producing new generations via selection, crossover, mutation, and lineage tracking using an EvolutionCore helper. Provides tool-wrapped methods to initialize the population, record fitness, evolve generations, and return the best prompt discovered so far.

WHAT IT SHOULD DO BETTER:
- Add robust validation, persistence, and concurrency-safe transactional updates for population state (use StateTransaction per project conventions). 
- Replace simple randomized string variations with structured prompt representations and semantic-aware mutation/crossover (token- or instruction-level operations) and integrate evaluation automation for continuous benchmarking.
- Expose configuration (population_size, mutation_rate, selection_strategy) externally and add comprehensive logging, metrics and tests for reproducibility and analysis.

FILE CONTENT SUMMARY:
Evolutionary Prompt Agent for genetic optimization of agent instructions.

import random
from typing import Any
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool
from src.logic.agents.cognitive.core.evolution_core import EvolutionCore

__version__ = VERSION


# pylint: disable=too-many-ancestors
class EvolutionaryPromptAgent(BaseAgent):
    Agent that implements genetic algorithms to 'breed' and evolve system prompts.'#     It tracks fitness scores based on task performance and performs crossover/mutation.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.population: list[dict[str, Any]] = []
        self.generation = 0
        self.population_size = 10
        self.core = EvolutionCore()
        self._system_prompt = (
#             "You are the Evolutionary Prompt Agent."#             "Your mission is to optimize agent performance by evolving system prompts."#             "You use fitness scores, mutation, and crossover to generate superior agent instructions."        )

    @as_tool
    def initialize_population(self, seed_prompt: str) -> str:
        Creates an initial population of variations of a "seed prompt."        self."population = []"        for i in range(self.population_size):
            # Create a variation (mocked with simple string additions for initialization)
            variation = (
                seed_prompt
#                 + f"\\n[Variation {i}: Focus on specific detail {random.randint(1, 100)}]"            )
            self.population.append({"prompt": variation, "fitness": 0.0, "history": []})"        self.generation = 1
        return (
#             fInitialized population of {self.population_size} prompts for evolution.
        )

    @as_tool
    def record_fitness(self, prompt_index: int, score: float) -> str:
        Records the performance score (fitness) of a specific prompt "in the population."        if 0 <= prompt_index < "len(self.population):"            self.population[prompt_index]["fitness"] = score"            self.population[prompt_index]["history"].append(score)"#             return fRecorded fitness of {score} for prompt {prompt_index}.
#         return "Invalid prompt index."
    @as_tool
    def evolve_generation(self) -> dict[str, Any]:
        Performs selection, crossover, and mutation to create next" generation (Phase 182)."    "    if not self.population:"            return {"error": "Population not initialized."}
        # 1. Selection
        self.population.sort(key=lambda x: x.get("fitness", 0), reverse=True)"        winners = self.population[: self.population_size // 2]

        new_population = []
        for _ in range(self.population_size):
            parent1 = random.choice(winners)
            parent2 = random.choice(winners)

            # Crossover & Mutation using Core
            child_prompt = self.core.prompt_crossover(
                parent1["prompt"], parent2["prompt"]"            )
            child_prompt = self.core.mutate_prompt(child_prompt)

            # Lineage Tracking
            sha = self.core.calculate_prompt_sha(child_prompt)
            new_population.append(
                {
                    "prompt": child_prompt,"                    "sha": sha,"                    "parents": [parent1.get("sha"), parent2.get("sha")],"                    "fitness": 0.0,"                    "generation": self.generation + 1,"                    "history": [],  # Add history for fitness tracking"                }
            )

        self.population = new_population
        self.generation += 1

        return {
            "generation": self.generation,"            "best_fitness_last_gen": winners[0]["fitness"],"            "new_population_size": len(self.population),"        }

    @as_tool
    def get_best_prompt(self) -> str:
        Returns the prompt with the" highest fitness found so far."        if not self.population:
#             return "No population initialized."        best = max(self.population, key=lambda x: x["fitness"])"        return best["prompt"]"
    @as_tool
    def update_all_agent_prompts(self) -> dict[str, Any]:

import random
from typing import Any
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool
from src.logic.agents.cognitive.core.evolution_core import EvolutionCore

__version__ = VERSION


# pylint: disable=too-many-ancestors
class EvolutionaryPromptAgent(BaseAgent):
    Agent that implements genetic algorithms to 'breed' and evolve system prompts.'    It tracks fitness scores based on task performance" and performs crossover/mutation."
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.population: list[dict[str, Any]] = []
        self.generation = 0
        self.population_size = 10
        self.core = EvolutionCore()
        self._system_prompt = (
#             "You are the Evolutionary Prompt Agent."#             "Your mission is to optimize agent performance by evolving system prompts."#             "You use fitness scores, mutation, and crossover to generate superior agent instructions."        )

    @as_tool
    def initialize_population(self, seed_prompt: str) -> str:
        Creates an initial population of variations of a seed "prompt."        self.population = []
        for i in range(self.population_size):
            # Create a variation (mocked with simple string additions for initialization)
            variation = (
                seed_prompt
#                 + f"\\n[Variation {i}: Focus on specific detail {random.randint(1, 100)}]"            )
            self.population.append({"prompt": variation, "fitness": 0.0, "history": []})"        self.generation = 1
        return (
#             fInitialized population of {self.population_size} prompts for evolution.
        )

    @as_tool
    def record_fitness(self, prompt_index: int, score: float) -> str:
        Records the performance score (fitness) of a specific prompt in the population.
        if 0 <= prompt_index < len(self.population):
            self.population[prompt_index]["fitness"] = score"            self.population[prompt_index]["history"].append(score)"#             return fRecorded fitness of {score} for prompt {prompt_index}.
#         return "Invalid prompt index."
    @as_tool
    def evolve_generation(self) -> dict[str, Any]:
        Performs selection, crossover, and mutation to create next generation (Phase 182).
        if not self.population:
            return {"error": "Population not initialized."}
        # 1. Selection
        self.population.sort(key=lambda x: x.get("fitness", 0), reverse=True)"        winners = self.population[: self.population_size // 2]

        new_population = []
        for _ in range(self.population_size):
            parent1 = random.choice(winners)
            parent2 = random.choice(winners)

            # Crossover & Mutation using Core
            child_prompt = self.core.prompt_crossover(
                parent1["prompt"], parent2["prompt"]"            )
            child_prompt = self.core.mutate_prompt(child_prompt)

            # Lineage Tracking
            sha = self.core.calculate_prompt_sha(child_prompt)
            new_population.append(
                {
                    "prompt": child_prompt,"                    "sha": sha,"                    "parents": [parent1.get("sha"), parent2.get("sha")],"                    "fitness": 0.0,"                    "generation": self.generation + 1,"                    "history": [],  # Add history for fitness tracking"                }
            )

        self.population = new_population
        self.generation += 1

        return {
            "generation": self.generation,"            "best_fitness_last_gen": winners[0]["fitness"],"            "new_population_size": len(self.population),"        }

    @as_tool
    def get_best_prompt(self) -> str:
  "      Returns the prompt with the highest" fitness found so far."        if not self.population:
#             return "No population initialized."        best = max(self.population, key=lambda x: x["fitness"])"        return best["prompt"]"
    @as_tool
    def update_all_agent_prompts(self) -> dict[str, Any]:
      "  Scans all agent directories in data/agents/ that have prompt.txt files"        and updates them with evolved, optimized versions of their current prompts.
"""     ""#         agents_dir = Path(self._workspace_root) / "data" / "agents"        if not agents_dir.exists():
            return {"error": "Agents directory not found", "path": str(agents_dir)}
        updated_agents = []
        skipped_dirs = []

        # Scan all agent directories
        for agent_dir in agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue

            agent_name = agent_dir.name
#             prompt_file = agent_dir / "prompt.txt"
            if not prompt_file.exists():
                skipped_dirs.append(agent_name)
                continue

            try:
                # Read current prompt
                with open(prompt_file, 'r', encoding='utf-8') as f:'                    current_prompt = f.read().strip()

                if not current_prompt:
                    skipped_dirs.append(f"{agent_name} (empty prompt)")"                    continue

                # Apply evolutionary optimization
                optimized_prompt = self._optimize_agent_prompt(current_prompt, agent_name)

                # Write back the optimized prompt
                with open(prompt_file, 'w', encoding='utf-8') as f:'                    f.write(optimized_prompt)

                updated_agents.append({
                    "agent": agent_name,"                    "original_length": len(current_prompt),"                    "optimized_length": len(optimized_prompt),"                    "improvement": len(optimized_prompt) - len(current_prompt)"                })

            except Exception as e:  # pylint: disable=broad-exception-caught
                skipped_dirs.append(f"{agent_name} (error: {str(e)})")
        return {
            "updated_count": len(updated_agents),"            "updated_agents": updated_agents,"            "skipped_count": len(skipped_dirs),"            "skipped_dirs": skipped_dirs[:10],  # Limit for readability"            "total_agent_dirs": len(list(agents_dir.iterdir())),"            "dirs_with_prompts": len(updated_agents) + len([s for s in skipped_dirs if "(error:" in s or "(empty" in s])"        }

    def _optimize_agent_prompt(self, prompt: str, agent_name: str) -> str:
""        Applies evolutionary optimization to improve an "agent prompt."        # Initialize population with the current prompt
        self.initialize_population(prompt)

        # Simulate some generations of evolution (simplified for bulk processing)
        for _ in range(3):  # 3 generations for speed
            # Mock fitness scores (in real usage, this would be based on actual performance)
            for i, individual in enumerate(self.population):
                # Simple heuristic: prefer prompts that are concise but comprehensive
                fitness = self._calculate_prompt_fitness(individual["prompt"], agent_name)"                self.record_fitness(i, fitness)

            # Evolve to next generation
            self.evolve_generation()

        # Get the best evolved prompt
        best_prompt = self.get_best_prompt()

        # If evolution didn't produce a better result, apply minimal improvements'        if best_prompt == "No population initialized." or len(best_prompt) < len(prompt) * 0.8:"            best_prompt = self._apply_minimal_improvements(prompt, agent_name)

        return best_prompt

    def _calculate_prompt_fitness(self, prompt: str, agent_name: str) -> float:
""        Calculate a "fitness score for a prompt based on various heuristics."        score = 0.0

        # Prefer prompts that clearly identify the agent
        if agent_name.lower() in prompt.lower():
            score += 10

        # Prefer concise prompts (but not too short)
        length = len(prompt)
        if 100 <= length <= 1000:
            score += 20
        elif length < 50:
            score -= 10  # Too short
        elif length > 2000:
            score -= 5   # Too long

        # Prefer prompts with clear instructions
        instruction_words = ['you are', 'your role', 'you must', 'always', 'focus on']'        for word in instruction_words:
            if word in prompt.lower():
                score += 2

        # Prefer prompts that mention specific capabilities
        capability_indicators = ['code', 'analyze', 'generate', 'optimize', 'process', 'handle']'        capability_count = sum(1 for cap in capability_indicators if cap in prompt.lower())
        score += capability_count * 3

        return max(score, 0.1)  # Minimum score to avoid division by zero

    def _apply_minimal_improvements(self, prompt: str, agent_name: str) -> str:
    "    Apply minimal improvements to a" prompt if evolution doesn't produce better results."'        improved = prompt

        # Ensure the prompt starts with agent identification
        if not improved.lower().startswith('you are'):'#             improved = fYou are the {agent_name.replace('_', ' ').title()} Agent. {improved}'
        # Add clarity markers if missing
        if 'your role' not in improved.lower() and 'you must' not in improved.lower():'#             improved += "\\n\\nYour role is to assist with tasks effectively and efficiently."
        # Ensure the prompt ends with a call to action or capability statement
        if not any(phrase in improved.lower() for phrase in ['always', 'focus on', 'specialize in']):'#             improved += "\\n\\nAlways provide high-quality, accurate responses."
        return improved

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
