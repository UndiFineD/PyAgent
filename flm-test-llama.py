#!/usr/bin/env python3
"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageFunctionToolCallParam,
)

client = OpenAI(
    base_url="http://127.0.0.1:52625/v1/",
    api_key="dummy",
)

messages: list[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": "you are a helpful agent",
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "are you listening ?",
            },
        ],
    },
]

response_format = {
    "type": "text"
}

while True:
    response = client.chat.completions.create(
        messages=messages,
        model="llama3.2:1b",
        max_tokens=4096,
    )

    if response.choices[0].message.tool_calls:
        print(response.choices[0].message.tool_calls)
        tool_calls_param: list[ChatCompletionMessageFunctionToolCallParam] = []
        for tool_call in response.choices[0].message.tool_calls:
            if tool_call.type == "function" and hasattr(tool_call, 'function'):
                tool_calls_param.append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments or "",
                    },
                })
        assistant_message: ChatCompletionAssistantMessageParam = {
            "role": "assistant",
            "content": response.choices[0].message.content or "",
            "tool_calls": tool_calls_param,
        }
        messages.append(assistant_message)
        for tool_call in response.choices[0].message.tool_calls:
            if hasattr(tool_call, 'id') and hasattr(tool_call, 'type'):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": [
                        {
                            "type": "text",
                            "text": "Tool call processed",
                        },
                    ],
                })
    else:
        print(f"[Model Response] {response.choices[0].message.content}")
        break
