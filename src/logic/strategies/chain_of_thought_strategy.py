#!/usr/bin/env python3
from __future__ import annotations

"""
Chain of thought strategy.py module.
"""
# Copyright 2026 PyAgent Authors
# Apache 2.0 License


import logging
from typing import TYPE_CHECKING

from src.core.base.lifecycle.version import VERSION

from .agent_strategy import AgentStrategy

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]
__version__ = VERSION # This line was moved out of the TYPE_CHECKING block for runtime access.

class ChainOfThoughtStrategy(AgentStrategy):
    """Chain-of-Thought strategy: Prompt -> Reasoning -> Response."""

    async def _safe_backend_call(
        self,
        step_name: str,
        call_prompt: str,
        backend_call: BackendFunction,
        system_prompt: str | None,
        history: list[dict[str, str]] | None,
        original_prompt_for_logging: str,
        agent_name: str,
        task_id: str,
    ) -> str:
        """
        Helper method to encapsulate backend calls with error handling and logging.
        """
        try:
            response = await backend_call(call_prompt, system_prompt, history)
            logging.info(f"[{agent_name} | {task_id}] Chain of Thought {step_name.capitalize()}:\n{response}")
            return response
        except Exception as e:
            logging.error(
                f"[{agent_name} | {task_id}] Failed during {step_name} step for prompt: {original_prompt_for_logging[:100]}... Error: {e}"
            )
            raise  # Re-raise or handle more gracefully based on desired behavior


    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
        agent_name: str = "UnknownAgent",
        task_id: str = "UnknownTask",
    ) -> str:
        """
        Executes the Chain-of-Thought strategy.

        This method first generates a reasoning prompt, sends it to the backend,
        and then uses the generated reasoning to formulate an execution prompt.
        The history is updated with the reasoning before the final execution call.

        Args:
            prompt: The main prompt for the task.
            context: Additional context relevant to the task.
            backend_call: An asynchronous callable function that interacts with
                          the LLM backend. It expects a prompt, an optional
                          system prompt, and an optional history.
            system_prompt: An optional system-level prompt to guide the LLM.
            history: An optional list of previous messages to maintain
                     conversational context.

        Returns:
            The final response from the LLM after the execution step.

        Raises:
            Exception: If an error occurs during either the reasoning or
                       execution steps of the backend call.
        """
        # Step 1: Reasoning
        reasoning_prompt = (
            f"{prompt}\n\n"
            f"Context:\n{context}\n\n"
            "Think step-by-step about how to solve this. "
            "List the changes needed and the reasoning behind them."
        )
        reasoning = await self._safe_backend_call(
            "reasoning", reasoning_prompt, backend_call, system_prompt, history, prompt,
            agent_name, task_id
        )

        # Step 2: Execution
        new_history = list(history) if history else []
        new_history.append({"role": "assistant", "content": reasoning})

        execution_prompt = (
            f"{prompt}\n\n"
            f"Context:\n{context}\n\n"
            f"Based on the following reasoning:\n{reasoning}\n\n"
            "Please implement the changes. Output ONLY the final code/content."
        )
        return await self._safe_backend_call(
            "execution", execution_prompt, backend_call, system_prompt, new_history, prompt,
            agent_name, task_id
        )
