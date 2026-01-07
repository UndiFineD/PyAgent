#!/usr/bin/env python3

"""Auto-extracted class from agent_strategies.py"""

from __future__ import annotations

from .AgentStrategy import AgentStrategy

try:
    from . import BackendFunction
except ImportError:
    from src.classes.strategies import BackendFunction

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import logging

class ChainOfThoughtStrategy(AgentStrategy):
    """Chain-of-Thought strategy: Prompt -> Reasoning -> Response."""

    def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        # Step 1: Reasoning
        reasoning_prompt = (
            f"{prompt}\n\nContext:\n{context}\n\n"
            "Think step-by-step about how to solve this. "
            "List the changes needed and the reasoning behind them."
        )
        reasoning = backend_call(reasoning_prompt, system_prompt, history)
        logging.info(f"Chain of Thought Reasoning:\n{reasoning}")

        # Step 2: Execution
        execution_prompt = (
            f"{prompt}\n\nContext:\n{context}\n\n"
            f"Based on the following reasoning:\n{reasoning}\n\n"
            "Please implement the changes. Output ONLY the final code/content."
        )
        
        # We append the reasoning to the history for the second call if history exists
        new_history = list(history) if history else []
        new_history.append({"role": "assistant", "content": reasoning})
        
        return backend_call(execution_prompt, system_prompt, new_history)
