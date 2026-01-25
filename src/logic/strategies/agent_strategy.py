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


"""Auto-extracted class from agent_strategies.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.core.base.lifecycle.version import VERSION

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class AgentStrategy(ABC):
    """Abstract base class for agent execution strategies."""

    @abstractmethod
    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
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
        ...
