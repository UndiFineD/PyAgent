# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\llm.py\complete.py\openai_sdk_0536159d2038.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\complete\openai_sdk.py

import json

from time import perf_counter

from typing import Optional

from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall

from ...env import DEFAULT_CORE_CONFIG, LOG

from ...schema.llm import LLMResponse

from .clients import get_openai_async_client_instance


def convert_openai_tool_to_llm_tool(tool_body: ChatCompletionMessageToolCall) -> dict:
    return {
        "id": tool_body.id,
        "type": tool_body.type,
        "function": {
            "name": tool_body.function.name,
            "arguments": json.loads(tool_body.function.arguments),
        },
    }


async def openai_complete(
    prompt=None,
    model=None,
    system_prompt=None,
    history_messages=[],
    json_mode=False,
    max_tokens=1024,
    prompt_kwargs: Optional[dict] = None,
    tools=None,
    **kwargs,
) -> LLMResponse:
    prompt_kwargs = prompt_kwargs or {}

    prompt_id = prompt_kwargs.get("prompt_id", "...")

    openai_async_client = get_openai_async_client_instance()

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.extend(history_messages)

    if prompt:
        messages.append({"role": "user", "content": prompt})

    if not messages:
        raise ValueError("No messages provided")

    _start_s = perf_counter()

    response: ChatCompletion = await openai_async_client.chat.completions.create(
        model=model,
        messages=messages,
        timeout=DEFAULT_CORE_CONFIG.llm_response_timeout,
        max_tokens=max_tokens,
        tools=tools,
        **DEFAULT_CORE_CONFIG.llm_openai_completion_kwargs,
        **kwargs,
    )

    _end_s = perf_counter()

    cached_tokens = getattr(response.usage.prompt_tokens_details, "cached_tokens", None)

    LOG.info(
        f"LLM Complete: {prompt_id} {model}. "
        f"cached {cached_tokens}, input {response.usage.prompt_tokens}, total {response.usage.total_tokens}, "
        f"time {_end_s - _start_s:.4f}s"
    )

    # Only support tool calls

    _tu = (
        [convert_openai_tool_to_llm_tool(tool) for tool in response.choices[0].message.tool_calls]
        if response.choices[0].message.tool_calls
        else None
    )

    llm_response = LLMResponse(
        role=response.choices[0].message.role,
        raw_response=response,
        content=response.choices[0].message.content,
        tool_calls=_tu,
    )

    if json_mode:
        try:
            json_content = json.loads(response.choices[0].message.content)

        except json.JSONDecodeError:
            LOG.error(f"JSON decode error: {response.choices[0].message.content}")

            json_content = None

        llm_response.json_content = json_content

    return llm_response
