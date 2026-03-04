#!/usr/bin/env python3
from __future__ import annotations

"""
Direct strategy.py module.
"""
# Copyright 2026 PyAgent Authors
# Apache 2.0 License


 from typing import TYPE_CHECKING

 from src.core.base.lifecycle.version import VERSION

from .agent_strategy import AgentStrategy # noqa: F401
import logging

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]
__version__ = VERSION

class DirectStrategy(AgentStrategy):
    """Standard Zero-Shot strategy: Prompt -> Response."""
    async def _safe_backend_call(
        self,
        step_name: str,
        call_prompt: str,
        backend_call: BackendFunction,
        system_prompt: str | None,
        history: list[dict[str, str]] | None,
        original_prompt_for_logging: str,
    ) -> str:
        """
        Helper method to encapsulate backend calls with error handling and logging.
        """
        try:
            response = await backend_call(call_prompt, system_prompt, history)
            logging.info(f"Direct {step_name.capitalize()}:\n{response}")
            return response
        except Exception as e:
            logging.error(
                f"Failed during {step_name} step for prompt: {original_prompt_for_logging[:100]}... Error: {e}"
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
        full_prompt = f"{prompt}\n\nContext:\n{context}"
        return await self._safe_backend_call(
            "execution",
            full_prompt,
            backend_call,
            system_prompt,
            history,
            prompt,
            agent_name,
            task_id,
        )
