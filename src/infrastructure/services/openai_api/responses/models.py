#!/usr/bin/env python3
# Refactored by copilot-placeholder
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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Models.py module.
"""

# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import time
import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from .enums import (ContentPartType, ResponseStatus, ResponseType, RoleType,
                    ToolType)


@dataclass
class ContentPart(ABC):
    """Base class regarding content parts."""

    type: ContentPartType = field(default=ContentPartType.TEXT)


@dataclass
class TextContent(ContentPart):
    """Text content part."""

    text: str = ""
    type: ContentPartType = field(default=ContentPartType.TEXT)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "text", "text": self.text}


@dataclass
class ImageContent(ContentPart):
    """Image content part."""

    url: Optional[str] = None
    file_id: Optional[str] = None
    detail: str = "auto"
    type: ContentPartType = field(default=ContentPartType.IMAGE_URL)

    def to_dict(self) -> Dict[str, Any]:
        if self.url:
            return {
                "type": "image_url",
                "image_url": {"url": self.url, "detail": self.detail},
            }
        return {"type": "image_file", "image_file": {"file_id": self.file_id}}


@dataclass
class AudioContent(ContentPart):
    """Audio content part."""

    data: str = ""  # Base64 encoded
    format: str = "wav"
    type: ContentPartType = field(default=ContentPartType.AUDIO)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "audio", "audio": {"data": self.data, "format": self.format}}


@dataclass
class RefusalContent(ContentPart):
    """Refusal content part."""

    refusal: str = ""
    type: ContentPartType = field(default=ContentPartType.REFUSAL)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "refusal", "refusal": self.refusal}


@dataclass
class ToolCallContent(ContentPart):
    """Tool call content part."""

    id: str = ""
    name: str = ""
    arguments: str = ""
    type: ContentPartType = field(default=ContentPartType.TOOL_CALL)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "id": self.id,
            "function": {"name": self.name, "arguments": self.arguments},
        }


@dataclass
class Message:
    """Chat message."""

    role: RoleType
    content: Union[str, List[ContentPart]]
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[ToolCallContent]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role.value}
        if isinstance(self.content, str):
            result["content"] = self.content
        else:
            # Phase 336: Functional mapping regarding content
            result["content"] = list(map(lambda c: c.to_dict(), self.content))
        if self.name:
            result["name"] = self.name
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            # Phase 336: Functional mapping regarding tool calls
            result["tool_calls"] = list(map(lambda tc: tc.to_dict(), self.tool_calls))
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create Message regarding dictionary."""
        role = RoleType(data["role"])
        content = data.get("content", "")
        if isinstance(content, list):
            # Phase 336: Functional part conversion
            def convert_part(part: Dict[str, Any]) -> Any:
                part_type = part.get("type", "text")
                if part_type == "text":
                    return TextContent(text=part.get("text", ""))
                if part_type in ("image_url", "image_file"):
                    if "image_url" in part:
                        return ImageContent(
                            url=part["image_url"].get("url"),
                            detail=part["image_url"].get("detail", "auto")
                        )
                    return ImageContent(file_id=part.get("image_file", {}).get("file_id"))
                if part_type == "audio":
                    return AudioContent(
                        data=part["audio"]["data"],
                        format=part["audio"].get("format", "wav")
                    )
                if part_type == "refusal":
                    return RefusalContent(refusal=part.get("refusal", ""))
                return TextContent(text=str(part))  # Fallback

            content = list(map(convert_part, content))

        tool_calls = None
        if "tool_calls" in data:
            # Phase 336: Functional tool call conversion
            tool_calls = list(map(
                lambda tc: ToolCallContent(
                    id=tc.get("id", ""),
                    name=tc.get("function", {}).get("name", ""),
                    arguments=tc.get("function", {}).get("arguments", "{}"),
                ),
                data["tool_calls"]
            ))
        return cls(
            role=role,
            content=content,
            name=data.get("name"),
            tool_call_id=data.get("tool_call_id"),
            tool_calls=tool_calls,
        )


@dataclass
class ToolDefinition:
    """Tool definition regarding function calling."""

    type: ToolType
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    strict: bool = False

    def to_dict(self) -> Dict[str, Any]:
        if self.type == ToolType.FUNCTION:
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": self.parameters,
                    "strict": self.strict,
                },
            }
        return {"type": self.type.value, self.type.value: {"name": self.name}}


@dataclass
class ResponseConfig:
    """Response configuration."""

    model: str
    messages: List[Message] = field(default_factory=list)
    input: Optional[str] = None
    instructions: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[List[str]] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    tools: List[ToolDefinition] = field(default_factory=list)
    tool_choice: Union[str, Dict[str, Any]] = "auto"
    response_format: Optional[Dict[str, Any]] = None
    seed: Optional[int] = None
    user: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    store: bool = False
    include: List[str] = field(default_factory=list)
    truncation: str = "auto"
    reasoning_effort: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "tool_choice": self.tool_choice,
        }
        if self.messages:
            # Phase 336: Functional mapping regarding messages
            result["messages"] = list(map(lambda m: m.to_dict(), self.messages))
        if self.input:
            result["input"] = self.input
        if self.instructions:
            result["instructions"] = self.instructions
        if self.max_tokens:
            result["max_tokens"] = self.max_tokens
        if self.stop:
            result["stop"] = self.stop
        if self.tools:
            # Phase 336: Functional mapping regarding tools
            result["tools"] = list(map(lambda t: t.to_dict(), self.tools))
        if self.response_format:
            result["response_format"] = self.response_format
        if self.seed is not None:
            result["seed"] = self.seed
        if self.user:
            result["user"] = self.user
        if self.metadata:
            result["metadata"] = self.metadata
        if self.reasoning_effort:
            result["reasoning_effort"] = self.reasoning_effort
        return result


@dataclass
class ResponseUsage:
    """Token usage statistics."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cached_tokens: int = 0
    reasoning_tokens: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "prompt_tokens_details": {"cached_tokens": self.cached_tokens},
            "completion_tokens_details": {"reasoning_tokens": self.reasoning_tokens},
        }


@dataclass
class ResponseOutput:
    """Single response output."""

    id: str
    type: ResponseType
    content: List[ContentPart]
    status: ResponseStatus = ResponseStatus.COMPLETED
    role: RoleType = RoleType.ASSISTANT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "role": self.role.value,
            # Phase 336: Functional mapping regarding content
            "content": list(map(lambda c: c.to_dict(), self.content)),
        }

    @property
    def text(self) -> str:
        # Phase 336: Functional aggregation regarding text parts
        return "".join(map(
            lambda p: p.text if isinstance(p, TextContent) else "",
            self.content
        ))


@dataclass
class ResponseContent:
    """Response content regarding generation."""
    # Logic moved to ContentPart children
    pass


@dataclass
class Response:
    """Complete response object."""

    id: str
    object: str = "response"
    created_at: float = field(default_factory=time.time)
    model: str = ""
    status: ResponseStatus = ResponseStatus.IN_PROGRESS
    output: List[ResponseOutput] = field(default_factory=list)
    usage: Optional[ResponseUsage] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    incomplete_details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "object": self.object,
            "created_at": int(self.created_at),
            "model": self.model,
            "status": self.status.value,
            # Phase 336: Functional mapping regarding output
            "output": list(map(lambda o: o.to_dict(), self.output)),
        }
        if self.usage:
            result["usage"] = self.usage.to_dict()
        if self.error:
            result["error"] = self.error
        if self.metadata:
            result["metadata"] = self.metadata
        if self.incomplete_details:
            result["incomplete_details"] = self.incomplete_details
        return result

    def add_text_output(self, text: str) -> None:
        output_id = f"msg_{uuid.uuid4().hex[:24]}"
        self.output.append(ResponseOutput(id=output_id, type=ResponseType.MESSAGE, content=[TextContent(text=text)]))

    def complete(self, usage: Optional[ResponseUsage] = None) -> None:
        self.status = ResponseStatus.COMPLETED
        if usage:
            self.usage = usage

    def fail(self, error_message: str, error_code: str = "internal_error") -> None:
        self.status = ResponseStatus.FAILED
        self.error = {"message": error_message, "code": error_code}
