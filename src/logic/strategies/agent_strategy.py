#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Agent Strategy - Abstract execution strategy for agents

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Implement a concrete subclass of AgentStrategy and provide an async
  execute(...) method.
- Call the subclass's execute(prompt, context, backend_call,'  system_prompt=None, history=None) from agent orchestration code to obtain
  generated content.
- Provide a BackendFunction callable matching the signature:
  (prompt: str, system_prompt: str|None, history: list[dict[str,str]]|None)
  -> str; run execute inside an asyncio event loop.

WHAT IT DOES:
- Declares a minimal, testable abstraction for pluggable agent execution
  strategies used to drive LLM calls.
- Standardizes the execution contract (async execute) so different strategies
  (streaming, batching, caching, safe-guards) can be swapped without changing
  callers.
- Keeps dependencies light and clearly typed (TYPE_CHECKING alias for
  BackendFunction).

WHAT IT SHOULD DO BETTER:
- Export a concrete typed alias for history entry objects and document expected
  keys to reduce caller confusion and enable static checks.
- Provide a small default/base implementation (e.g., simple passthrough strategy)
  and helper utilities for common concerns (retry, timeout, logging, metrics).
- Validate and normalize inputs (None-to-empty-history, enforce non-empty
  prompt/context) and add explicit error handling and unit tests to codify
  expected behavior.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_strategies.py

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import TYPE_CHECKING
except ImportError:
    from typing import TYPE_CHECKING


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION



class AgentStrategy(ABC):
    """Abstract base class for agent execution strategies.
    @abstractmethod
    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """Execute the strategy to generate a response.""""
        Args:
            prompt: The user's request or instruction.'            context: The current file content or context.
            backend_call: A callable to invoke the LLM.
            system_prompt: Optional system prompt.
            history: Optional conversation history.

        Returns:
            The final generated content.
        