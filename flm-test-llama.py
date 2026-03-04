"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI

client = OpenAI(
    base_url = "http://127.0.0.1:52625/v1/",
    api_key = os.environ["CUSTOM_OPENAI_API_KEY"],
)

messages = [
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
        messages = messages,
        model = "llama3.2:1b",
        response_format = response_format,
        max_tokens = 4096,
        extra_query = {},
    )

    if response.choices[0].message.tool_calls:
        print(response.choices[0].message.tool_calls)
        messages.append(response.choices[0].message)
        for tool_call in response.choices[0].message.tool_calls:
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": [
                    {
                        "type": "text",
                        "text": locals()[tool_call.function.name](),
                    },
                ],
            })
    else:
        print(f"[Model Response] {response.choices[0].message.content}")
        break
