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

class DirectStrategy(AgentStrategy):
    """Standard Zero-Shot strategy: Prompt -> Response."""

    def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        full_prompt = f"{prompt}\n\nContext:\n{context}"
        return backend_call(full_prompt, system_prompt, history)
