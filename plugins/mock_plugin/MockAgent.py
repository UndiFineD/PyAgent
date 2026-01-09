#!/usr/bin/env python3

"""
MockAgent for a community-submitted plugin.
Demonstrates how to wrap a Core and interact with the Fleet.
"""

import logging
from src.classes.base_agent import BaseAgent
from .MockCore import MockCore

class MockAgent(BaseAgent):
    """A mock agent that shows community developers the recommended pattern."""
    
    def __init__(self, arg_path: str = "mock_config.json"):
        # We don't strictly need a real config file for this mock
        super().__init__(arg_path)
        self.core = MockCore(multiplier=1.5)
        logging.info("MockAgent initialized with MockCore.")

    def run(self, task: str) -> str:
        """Main entry point for agent logic."""
        logging.info(f"MockAgent handling task: {task}")
        processed = self.core.format_mock_response(task)
        
        # Accessing fleet-wide tools if registry is available
        # result = self.call_tool("SearchAgent", query="python patterns")
        
        return f"MockAgent processed your task: {processed}"

    def get_status(self) -> dict:
        return self.core.get_metadata()
