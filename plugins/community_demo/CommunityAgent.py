#!/usr/bin/env python3

"""
CommunityAgent: A mock community-submitted agent.
Demonstrates the Core/Shell pattern.
"""

from src.classes.base_agent import BaseAgent
from .CommunityCore import CommunityCore
import logging

class CommunityAgent(BaseAgent):
    """A flexible agent shell that uses CommunityCore for logic."""
    
    def __init__(self, path: str = None) -> None:
        super().__init__(path)
        self.name = "CommunityAgent"
        self.core = CommunityCore()
        logging.info(f"{self.name} initialized with CommunityCore.")

    def improve_content(self, content: str) -> str:
        """Implements the standard agent interface."""
        logging.info(f"{self.name} is processing content...")
        return self.core.process_data(content)

    def run(self, task: str) -> str:
        """Main execution loop for the agent."""
        return self.improve_content(task)
