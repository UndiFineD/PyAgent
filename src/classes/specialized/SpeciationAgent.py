#!/usr/bin/env python3

import logging
import os
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool
from pathlib import Path

class SpeciationAgent(BaseAgent):
    """
    Agent responsible for 'speciation' - creating specialized derivatives of existing agents.
    It analyzes task success and generates new agent classes with optimized system prompts.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Speciation Agent. "
            "Your goal is to foster agent evolution by identifying niche capabilities "
            "and synthesizing new, specialized agent types from existing 'Base' agents."
        )

    @as_tool
    def evolve_specialized_agent(self, base_agent_name: str, niche_domain: str) -> str:
        """
        Creates a new agent class file that specializes in a specific niche.
        e.g., 'CoderAgent' -> 'ReactSpecialistAgent'
        """
        logging.info(f"SpeciationAgent: Evolving specialization for {base_agent_name} in {niche_domain}")
        
        new_agent_name = f"{niche_domain.replace(' ', '')}{base_agent_name}"
        output_path = f"src/classes/specialized/{new_agent_name}.py"
        
        # Generation Logic
        prompt = (
            f"Create a Python class definition for '{new_agent_name}' that inherits from '{base_agent_name}'. "
            f"The specialization niche is: {niche_domain}.\n"
            "Include an optimized __init__ with a specialized _system_prompt.\n"
            "Return ONLY the Python code."
        )
        
        specialized_code = self.think(prompt)
        
        # In a real scenario, we'd save this to a file and register it.
        # For now, we simulate the 'speciation' by logging the creation.
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(specialized_code)
            
        return f"Successfully speciated {new_agent_name} at {output_path}"
