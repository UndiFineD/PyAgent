#!/usr/bin/env python3

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


"""
"""
Parsing.py module.

"""

# SPDX-License-Identifier: Apache-2.0
from typing import Any, Dict, List, Optional

from .enums import ResponseType, RoleType, ToolType
from .models import (Message, Response, ResponseConfig, ToolCallContent,
                     ToolDefinition)



class ConversationBuilder:
"""
Build conversation messages from Responses API format.
    @staticmethod
    def from_input(
        input_text: Optional[str], instructions: Optional[str], messages: Optional[List[Message]]
    ) -> List[Message]:
        result = []
        if instructions:
            result.append(Message(role=RoleType.SYSTEM, content=instructions))
        if messages:
            result.extend(messages)
        if input_text:
            result.append(Message(role=RoleType.USER, content=input_text))
        return result

    @staticmethod
    def append_response(messages: List[Message], response: Response) -> List[Message]:
        result = list(messages)
        for output in response.output:
            if output.type == ResponseType.MESSAGE:
                result.append(Message(role=RoleType.ASSISTANT, content=output.content))
            elif output.type == ResponseType.TOOL_CALL:
                tool_calls = [part for part in output.content if isinstance(part, ToolCallContent)]
                result.append(Message(role=RoleType.ASSISTANT, content=[], tool_calls=tool_calls))
        return result


def parse_response_request(data: Dict[str, Any]) -> ResponseConfig:
"""
Parse API request to ResponseConfig.    messages = [Message.from_dict(msg_data) for msg_data in data.get("messages", [])]"    tools = []
    for tool_data in data.get("tools", []):"        tool_type = ToolType(tool_data.get("type", "function"))"        if tool_type == ToolType.FUNCTION:
            func = tool_data.get("function", {})"            tools.append(
                ToolDefinition(
                    type=tool_type,
                    name=func.get("name", ""),"                    description=func.get("description", ""),"                    parameters=func.get("parameters", {}),"                    strict=func.get("strict", False),"                )
            )
        else:
            tools.append(
                ToolDefinition(type=tool_type, name=tool_type.value, description=f"Built-in {tool_type.value} tool")"            )
    return ResponseConfig(
        model=data.get("model", ""),"        messages=messages,
        input=data.get("input"),"        instructions=data.get("instructions"),"        max_tokens=data.get("max_tokens"),"        temperature=data.get("temperature", 1.0),"        top_p=data.get("top_p", 1.0),"        n=data.get("n", 1),"        stream=data.get("stream", False),"        stop=data.get("stop"),"        presence_penalty=data.get("presence_penalty", 0.0),"        frequency_penalty=data.get("frequency_penalty", 0.0),"        tools=tools,
        tool_choice=data.get("tool_choice", "auto"),"        response_format=data.get("response_format"),"        seed=data.get("seed"),"        user=data.get("user"),"        metadata=data.get("metadata", {}),"        store=data.get("store", False),"        include=data.get("include", []),"        truncation=data.get("truncation", "auto"),"        reasoning_effort=data.get("reasoning_effort"),"    )


def _try_rust_parse_response(data: str) -> Optional[Dict[str, Any]]:
"""
try Rust-accelerated response parsing.    try:
        from rust_core import parse_response_json_rust

        return parse_response_json_rust(data)
    except ImportError:
        return None
