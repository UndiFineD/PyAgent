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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Convenience functions for LM Studio.
"""

import logging
from typing import Iterator

logger = logging.getLogger(__name__)


def lmstudio_chat(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
    **kwargs,
) -> str:
    """Convenience function for quick LM Studio chat."""
    try:
        import lmstudio

        llm = lmstudio.llm(model) if model else lmstudio.llm()
        chat = lmstudio.Chat(system_prompt)
        chat.add_user_message(prompt)

        result = llm.respond(chat)
        return str(result)

    except Exception as e:
        logger.error(f"lmstudio_chat error: {e}")
        return ""


def lmstudio_stream(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
) -> Iterator[str]:
    """Convenience function for streaming LM Studio chat."""
    try:
        import lmstudio

        llm = lmstudio.llm(model) if model else lmstudio.llm()
        chat = lmstudio.Chat(system_prompt)
        chat.add_user_message(prompt)

        for fragment in llm.respond_stream(chat):
            yield str(fragment)

    except Exception as e:
        logger.error(f"lmstudio_stream error: {e}")


async def lmstudio_chat_async(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
    host: str = "localhost:1234",
) -> str:
    """Async convenience function for LM Studio chat."""
    try:
        import lmstudio

        async with lmstudio.AsyncClient(host) as client:
            llm = await client.llm.get(model) if model else await client.llm.get()

            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)

            result = await llm.respond(chat)
            return str(result)

    except Exception as e:
        logger.error(f"lmstudio_chat_async error: {e}")
        return ""
