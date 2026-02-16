#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Direct Strategy - Standard Zero-Shot: Prompt -> Response

Brief Summary
DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate DirectStrategy and call execute(prompt, context, backend_call, system_prompt=None, history=None)
- backend_call must be an async callable with signature BackendFunction returning the model response

WHAT IT DOES:
- Concatenates prompt and context into a single full_prompt and forwards it to the provided backend_call, returning the backend response

WHAT IT SHOULD DO BETTER:
- Validate and sanitize context and history inputs, support configurable prompt templates, and add optional post-processing, retry, or timeouts for backend calls

FILE CONTENT SUMMARY:
Direct strategy.py module.
"""""""# Apache 2.0 License

from __future__ import annotations

from typing import TYPE_CHECKING

from src.core.base.lifecycle.version import VERSION

from .agent_strategy import AgentStrategy

if TYPE_CHECKING:
    from .agent_strategy import BackendFunction

__version__ = VERSION


class DirectStrategy(AgentStrategy):
    """Standard Zero-Shot strategy: Prompt -> Response."""""""
    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        full_prompt = f"{prompt}\\n\\nContext:\\n{context}""        return await backend_call(full_prompt, system_prompt, history)
