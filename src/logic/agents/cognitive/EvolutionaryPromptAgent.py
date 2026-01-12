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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import logging
import json
import random
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.agents.cognitive.core.EvolutionCore import EvolutionCore

class EvolutionaryPromptAgent(BaseAgent):
    """
    Agent that implements genetic algorithms to 'breed' and evolve system prompts.
    It tracks fitness scores based on task performance and performs crossover/mutation.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.population: List[Dict[str, Any]] = []
        self.generation = 0
        self.population_size = 10
        self.core = EvolutionCore()
        self._system_prompt = (
            "You are the Evolutionary Prompt Agent. "
            "Your mission is to optimize agent performance by evolving system prompts. "
            "You use fitness scores, mutation, and crossover to generate superior agent instructions."
        )

    @as_tool
    def initialize_population(self, seed_prompt: str) -> str:
        """
        Creates an initial population of variations of a seed prompt.
        """
        self.population = []
        for i in range(self.population_size):
            # Create a variation (mocked with simple string additions for initialization)
            variation = seed_prompt + f"\n[Variation {i}: Focus on specific detail {random.randint(1,100)}]"
            self.population.append({
                "prompt": variation,
                "fitness": 0.0,
                "history": []
            })
        self.generation = 1
        return f"Initialized population of {self.population_size} prompts for evolution."

    @as_tool
    def record_fitness(self, prompt_index: int, score: float) -> str:
        """
        Records the performance score (fitness) of a specific prompt in the population.
        """
        if 0 <= prompt_index < len(self.population):
            self.population[prompt_index]["fitness"] = score
            self.population[prompt_index]["history"].append(score)
            return f"Recorded fitness of {score} for prompt {prompt_index}."
        return "Invalid prompt index."

    @as_tool
    def evolve_generation(self) -> Dict[str, Any]:
        """
        Performs selection, crossover, and mutation to create next generation (Phase 182).
        """
        if not self.population:
            return {"error": "Population not initialized."}

        # 1. Selection
        self.population.sort(key=lambda x: x.get("fitness", 0), reverse=True)
        winners = self.population[:self.population_size // 2]
        
        new_population = []
        for i in range(self.population_size):
            parent1 = random.choice(winners)
            parent2 = random.choice(winners)
            
            # Crossover & Mutation using Core
            child_prompt = self.core.prompt_crossover(parent1["prompt"], parent2["prompt"])
            child_prompt = self.core.mutate_prompt(child_prompt)
            
            # Lineage Tracking
            sha = self.core.calculate_prompt_sha(child_prompt)
            new_population.append({
                "prompt": child_prompt,
                "sha": sha,
                "parents": [parent1.get("sha"), parent2.get("sha")],
                "fitness": 0.0,
                "generation": self.generation + 1
            })
            
        self.population = new_population
        self.generation += 1
        return {"generation": self.generation, "top_fitness": winners[0].get("fitness")}
            p2_lines = parent2["prompt"].split("\n")
            crossover_point = len(p1_lines) // 2
            child_prompt = "\n".join(p1_lines[:crossover_point] + p2_lines[crossover_point:])
            
            # Mutation (Randomly append a new constraint or adjective)
            if random.random() < 0.2:
                mutations = ["Be extremely concise.", "Use modern Python idioms.", "Prioritize security above all.", "Explain every step."]
                child_prompt += f"\n[Mutation: {random.choice(mutations)}]"
                
            new_population.append({
                "prompt": child_prompt,
                "fitness": 0.0,
                "history": []
            })
            
        self.population = new_population
        self.generation += 1
        
        return {
            "generation": self.generation,
            "best_fitness_last_gen": winners[0]["fitness"],
            "new_population_size": len(self.population)
        }

    @as_tool
    def get_best_prompt(self) -> str:
        """
        Returns the prompt with the highest fitness found so far.
        """
        if not self.population:
            return "No population initialized."
        best = max(self.population, key=lambda x: x["fitness"])
        return best["prompt"]
