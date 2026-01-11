#!/usr/bin/env python3

"""Auto-extracted class from agent_strategies.py"""

from __future__ import annotations

from .AgentStrategy import AgentStrategy

try:
    from . import BackendFunction
except ImportError:
    from src.logic.strategies import BackendFunction

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import logging

class ReflexionStrategy(AgentStrategy):
    """Reflexion strategy: Draft -> Critique -> Revise."""

    def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        # Step 1: Draft
        draft = backend_call(f"{prompt}\n\nContext:\n{context}", system_prompt, history)
        
        # Step 2: Critique
        critique_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            "Critique this implementation. Identify any bugs, missing requirements, "
            "or style issues. Be harsh but constructive."
        )
        critique = backend_call(critique_prompt, "You are a senior code reviewer.", [])
        logging.info(f"Reflexion Critique:\n{critique}")

        # Step 3: Revise
        revision_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            f"Critique:\n{critique}\n\n"
            "Please rewrite the implementation to address the critique. "
            "Output ONLY the final code/content."
        )
        
        return backend_call(revision_prompt, system_prompt, history)
