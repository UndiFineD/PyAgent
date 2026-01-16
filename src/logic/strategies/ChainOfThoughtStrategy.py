#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from __future__ import annotations
from src.core.base.Version import VERSION
from .AgentStrategy import AgentStrategy
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class ChainOfThoughtStrategy(AgentStrategy):
    """Chain-of-Thought strategy: Prompt -> Reasoning -> Response."""

    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        # Step 1: Reasoning
        reasoning_prompt = (
            f"{prompt}\n\nContext:\n{context}\n\n"
            "Think step-by-step about how to solve this. "
            "List the changes needed and the reasoning behind them."
        )
        reasoning = await backend_call(reasoning_prompt, system_prompt, history)
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

        return await backend_call(execution_prompt, system_prompt, new_history)
