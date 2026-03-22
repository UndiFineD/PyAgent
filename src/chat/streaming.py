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

"""Streaming chat — async token-by-token text generator and SSE formatter.

Provides utilities for streaming LLM responses through Server-Sent Events
(SSE) so the frontend can display tokens as they arrive.  Works with any
async generator that yields text chunks.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any


# ---------------------------------------------------------------------------
# Token streaming helpers
# ---------------------------------------------------------------------------


async def word_chunks(text: str, delay: float = 0.0) -> AsyncGenerator[str, None]:
    """Yield the words in *text* one at a time, optionally with a *delay*.

    This is primarily useful for testing and demos where you want to simulate
    a streaming response from an LLM without actually calling one.

    Parameters
    ----------
    text:
        Full text to stream word-by-word.
    delay:
        Seconds to ``asyncio.sleep`` between each word (0 = no delay).
    """
    words = text.split()
    for i, word in enumerate(words):
        chunk = word if i == 0 else " " + word
        if delay > 0:
            await asyncio.sleep(delay)
        yield chunk


async def collect(stream: AsyncIterator[str]) -> str:
    """Consume an async text stream and return the concatenated result."""
    parts: list[str] = []
    async for chunk in stream:
        parts.append(chunk)
    return "".join(parts)


# ---------------------------------------------------------------------------
# SSE formatting
# ---------------------------------------------------------------------------


def _sse_event(data: str, event: str | None = None, id: str | None = None) -> str:
    """Format a single Server-Sent Event as a string.

    Parameters
    ----------
    data:
        The ``data:`` field payload.
    event:
        Optional ``event:`` field name.
    id:
        Optional ``id:`` field value for reconnection.
    """
    lines: list[str] = []
    if id is not None:
        lines.append(f"id: {id}")
    if event is not None:
        lines.append(f"event: {event}")
    for line in data.splitlines():
        lines.append(f"data: {line}")
    lines.append("")  # blank line terminates the event
    lines.append("")
    return "\n".join(lines)


async def stream_to_sse(
    stream: AsyncIterator[str],
    *,
    event: str = "token",
    done_event: str = "done",
) -> AsyncGenerator[str, None]:
    """Wrap a text stream as an SSE event stream.

    Each text chunk is emitted as a ``token`` event.  When the stream is
    exhausted a final ``done`` event is sent with ``data: [DONE]``.

    Parameters
    ----------
    stream:
        Async iterator producing text chunks.
    event:
        SSE event name for each chunk (default ``"token"``).
    done_event:
        SSE event name for the final sentinel (default ``"done"``).
    """
    idx = 0
    async for chunk in stream:
        payload = json.dumps({"token": chunk})
        yield _sse_event(payload, event=event, id=str(idx))
        idx += 1
    yield _sse_event("[DONE]", event=done_event)


# ---------------------------------------------------------------------------
# StreamingChatSession
# ---------------------------------------------------------------------------


class StreamingChatSession:
    """A stateful session that manages streaming agent responses.

    The session accumulates the full response as chunks arrive so the caller
    can inspect the complete text after streaming finishes.

    Parameters
    ----------
    room_name:
        Identifier for the chat room this session belongs to.
    """

    def __init__(self, room_name: str) -> None:
        self.room_name = room_name
        self._chunks: list[str] = []
        self._finished = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_finished(self) -> bool:
        """True once the stream has been fully consumed."""
        return self._finished

    @property
    def full_text(self) -> str:
        """The accumulated response text up to the current point."""
        return "".join(self._chunks)

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------

    async def stream(self, source: AsyncIterator[str]) -> AsyncGenerator[str, None]:
        """Stream *source*, accumulating chunks and yielding each one.

        Parameters
        ----------
        source:
            Async iterator of text chunks (e.g. from an LLM adapter).
        """
        self._chunks = []
        self._finished = False
        async for chunk in source:
            self._chunks.append(chunk)
            yield chunk
        self._finished = True

    def clear(self) -> None:
        """Reset the session state."""
        self._chunks = []
        self._finished = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize the session state for inspection / logging."""
        return {
            "room_name": self.room_name,
            "is_finished": self._finished,
            "chunk_count": len(self._chunks),
            "full_text": self.full_text,
        }
