#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Chain of thought strategy.py module.
"""
# Apache 2.0 License

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.core.base.lifecycle.version import VERSION

from .agent_strategy import AgentStrategy

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
