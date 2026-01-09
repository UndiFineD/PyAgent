#!/usr/bin/env python3

import logging
import json
import random
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

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
        Performs selection, crossover, and mutation to create the next generation of prompts.
        """
        if not self.population:
            return {"error": "Population not initialized."}

        # 1. Selection (Tournament Selection)
        self.population.sort(key=lambda x: x["fitness"], reverse=True)
        winners = self.population[:self.population_size // 2]
        
        # 2. Crossover & Mutation
        new_population = []
        for i in range(self.population_size):
            parent1 = random.choice(winners)
            parent2 = random.choice(winners)
            
            # Crossover (Simplified: mix chunks of strings)
            p1_lines = parent1["prompt"].split("\n")
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
