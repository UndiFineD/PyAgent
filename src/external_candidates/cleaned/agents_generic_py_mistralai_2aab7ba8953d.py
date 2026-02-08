# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_agents.py\livekit.py\agents.py\llm.py\provider_format.py\mistralai_2aab7ba8953d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\llm\_provider_format\mistralai.py

from __future__ import annotations

from typing import Literal

from livekit.agents import llm

from .openai import to_chat_ctx as openai_to_chat_ctx


def to_chat_ctx(
    chat_ctx: llm.ChatContext, *, inject_dummy_user_message: bool = True
) -> tuple[list[dict], Literal[None]]:
    messages, _ = openai_to_chat_ctx(chat_ctx, inject_dummy_user_message=inject_dummy_user_message)

    if inject_dummy_user_message and (not messages or messages[-1]["role"] not in ["user", "tool"]):
        messages.append({"role": "user", "content": ""})

    return messages, None
