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
Reflexion strategy.py module.
"""
# Apache 2.0 License

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Optional

from src.core.base.lifecycle.version import VERSION

from .agent_strategy import AgentStrategy

if TYPE_CHECKING:
    from collections.abc import Callable

    BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class ReflexionStrategy(AgentStrategy):
    """Reflexion strategy: Draft -> Critique -> Revise."""

    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        # Step 1: Draft
        draft = await backend_call(f"{prompt}\n\nContext:\n{context}", system_prompt, history)

        # Step 2: Critique
        critique_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            "Critique this implementation. Identify any bugs, missing requirements, "
            "or style issues. Be harsh but constructive."
        )
        critique = await backend_call(critique_prompt, "You are a senior code reviewer.", [])
        logging.info(f"Reflexion Critique:\n{critique}")

        # Step 3: Revise
        revision_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            f"Critique:\n{critique}\n\n"
            "Please rewrite the implementation to address the critique. "
            "Output ONLY the final code/content."
        )
        return await backend_call(revision_prompt, system_prompt, history)
