#!/usr/bin/env python3

"""Auto-extracted class from agent_strategies.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import logging

try:
    from . import BackendFunction
except ImportError:
    from src.classes.strategies import BackendFunction

class AgentStrategy(ABC):
    """Abstract base class for agent execution strategies."""

    @abstractmethod
    def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Execute the strategy to generate a response.

        Args:
            prompt: The user's request or instruction.
            context: The current file content or context.
            backend_call: A callable to invoke the LLM.
            system_prompt: Optional system prompt.
            history: Optional conversation history.

        Returns:
            The final generated content.
        """
        pass
