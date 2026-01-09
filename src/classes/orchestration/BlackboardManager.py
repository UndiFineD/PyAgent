#!/usr/bin/env python3

"""Shared central memory for opportunistic agent collaboration (Blackboard Pattern)."""

import logging
from typing import Dict, Any, List

from .BlackboardCore import BlackboardCore

class BlackboardManager:
    """
    Central repository for agents to post findings and look for data.
    Shell for BlackboardCore.
    """
    
    def __init__(self) -> None:
        self.core = BlackboardCore()

    def post(self, key: str, value: Any, agent_name: str):
        """Post data to the blackboard."""
        logging.info(f"Blackboard: Agent {agent_name} posted to {key}")
        self.core.process_post(key, value, agent_name)

    def get(self, key: str) -> Any:
        """Retrieve data from the blackboard."""
        return self.core.get_value(key)

    def list_keys(self) -> List[str]:
        """List all available keys on the blackboard."""
        return self.core.get_all_keys()
