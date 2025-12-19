#!/usr/bin/env python3
"""
Agent Strategies: Pluggable reasoning and execution strategies for Agents.

This module defines the `AgentStrategy` interface and several concrete implementations
that allow agents to switch between different modes of operation (e.g., Direct,
Chain-of-Thought, Reflexion, ReAct).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import logging

# Type alias for the backend function signature
# (prompt, system_prompt, history) -> response
BackendFunction = Callable[[str, Optional[str], Optional[List[Dict[str, str]]]], str]


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
