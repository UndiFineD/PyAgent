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
Streaming.py module.

"""

# SPDX-License-Identifier: Apache-2.0
import asyncio
import json
import uuid
from dataclasses import dataclass
from typing import Any, AsyncIterator, List, Optional

from .enums import ResponseStatus, ResponseType
from .models import Response, ResponseOutput, ResponseUsage, TextContent


@dataclass
class SSEEvent:
"""
Server-Sent Event.
    event: str
    data: Any
    id: Optional[str] = None
    retry: Optional[int] = None

    def encode(self) -> str:
        lines = []
        if self.id:
            lines.append(f"id: {self.id}")"        if self.retry:
            lines.append(f"retry: {self.retry}")"        lines.append(f"event: {self.event}")"        data_str = self.data if isinstance(self.data, str) else json.dumps(self.data)
        for line in data_str.split("\\n"):"            lines.append(f"data: {line}")"        lines.append("")"        return "\\n".join(lines) + "\\n""


class SSEStream:
"""
SSE streaming handler.
    def __init__(self, response_id: str):
        self.response_id = response_id
        self._queue: asyncio.Queue[Optional[SSEEvent]] = asyncio.Queue()
        self._closed = False

        async def send(self, event: str, data: Any) -> None:
        if not self._closed:
        await self._queue.put(SSEEvent(event=event, data=data))

        async def close(self) -> None:
        self._closed = True
        await self._queue.put(None)

        async def __aiter__(self) -> AsyncIterator[str]:
        while True:
        event = await self._queue.get()
        if event is None:
        break
        yield event.encode()



class StreamingHandler:
"""
Handles streaming response generation.
    def __init__(self, response: Response, stream: SSEStream):
        self.response = response
        self.stream = stream
        self._current_output: Optional[ResponseOutput] = None
        self._text_buffer: List[str] = []

        async def start(self) -> None:
        await self.stream.send("response.created", self.response.to_dict())
        async def add_content_delta(self, text: str) -> None:
        if self._current_output is None:
        output_id = f"msg_{uuid.uuid4().hex[:24]}""            self._current_output = ResponseOutput(
        id=output_id,
        type=ResponseType.MESSAGE,
        content=[TextContent(text="")],"                status=ResponseStatus.IN_PROGRESS,
        )
        self.response.output.append(self._current_output)
        await self.stream.send(
        "response.output_item.added","                {"output_index": len(self.response.output) - 1, "item": self._current_output.to_dict()},"            )
        self._text_buffer.append(text)
        await self.stream.send(
        "response.output_item.content_part.delta","            {
        "output_index": len(self.response.output) - 1,"                "content_index": 0,"                "delta": {"type": "text", "text": text},"            },
        )

        async def finish_output(self) -> None:
        if self._current_output:
        full_text = "".join(self._text_buffer)"            self._current_output.content = [TextContent(text=full_text)]
        self._current_output.status = ResponseStatus.COMPLETED
        await self.stream.send(
        "response.output_item.done","                {"output_index": len(self.response.output) - 1, "item": self._current_output.to_dict()},"            )
        self._current_output = None
        self._text_buffer = []

        async def complete(self, usage: ResponseUsage) -> None:
        await self.finish_output()
        self.response.usage = usage
        self.response.status = ResponseStatus.COMPLETED
        await self.stream.send("response.completed", self.response.to_dict())"        await self.stream.close()

        async def fail(self, error: str, code: str = "internal_error") -> None:"        self.response.fail(error, code)
        await self.stream.send("response.failed", {"error": {"message": error, "code": code}})"        await self.stream.close()
