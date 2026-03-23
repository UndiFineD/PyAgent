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

"""Tests for src/chat/streaming.py — async SSE streaming helpers."""

from __future__ import annotations

import json

import pytest

from chat.streaming import (
    StreamingChatSession,
    collect,
    stream_to_sse,
    word_chunks,
)


# ---------------------------------------------------------------------------
# word_chunks
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_word_chunks_yields_each_word() -> None:
    chunks: list[str] = []
    async for c in word_chunks("hello world foo"):
        chunks.append(c)
    assert "".join(chunks) == "hello world foo"


@pytest.mark.asyncio
async def test_word_chunks_empty_string() -> None:
    chunks: list[str] = []
    async for c in word_chunks(""):
        chunks.append(c)
    assert chunks == []


@pytest.mark.asyncio
async def test_word_chunks_single_word() -> None:
    result = await collect(word_chunks("hello"))
    assert result == "hello"


@pytest.mark.asyncio
async def test_word_chunks_preserves_leading_spaces() -> None:
    """Second and subsequent words should be prefixed with a space."""
    chunks: list[str] = []
    async for c in word_chunks("a b c"):
        chunks.append(c)
    # first chunk has no leading space; rest do
    assert chunks[0] == "a"
    assert chunks[1] == " b"
    assert chunks[2] == " c"


# ---------------------------------------------------------------------------
# collect
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_collect_joins_all_chunks() -> None:
    async def gen():
        yield "foo"
        yield " "
        yield "bar"

    result = await collect(gen())
    assert result == "foo bar"


@pytest.mark.asyncio
async def test_collect_empty_stream() -> None:
    async def gen():
        return
        yield  # make it an async generator

    result = await collect(gen())
    assert result == ""


# ---------------------------------------------------------------------------
# stream_to_sse
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stream_to_sse_emits_token_events() -> None:
    events: list[str] = []
    async for ev in stream_to_sse(word_chunks("hi there")):
        events.append(ev)

    # Last event should be the done sentinel
    assert "[DONE]" in events[-1]
    assert "done" in events[-1]

    # Non-final events carry tokens
    for ev in events[:-1]:
        assert "event: token" in ev
        body = [line for line in ev.splitlines() if line.startswith("data:")]
        assert body, "no data: line found"
        payload = json.loads(body[0][len("data: "):])
        assert "token" in payload


@pytest.mark.asyncio
async def test_stream_to_sse_custom_event_names() -> None:
    events: list[str] = []
    async for ev in stream_to_sse(word_chunks("x"), event="chunk", done_event="end"):
        events.append(ev)

    token_events = [e for e in events if "event: chunk" in e]
    done_events = [e for e in events if "event: end" in e]
    assert token_events
    assert len(done_events) == 1


@pytest.mark.asyncio
async def test_stream_to_sse_sequential_ids() -> None:
    events: list[str] = []
    async for ev in stream_to_sse(word_chunks("a b c")):
        events.append(ev)

    # token events should have sequential ids: 0, 1, 2
    token_events = [e for e in events if "event: token" in e]
    for i, ev in enumerate(token_events):
        assert f"id: {i}" in ev


# ---------------------------------------------------------------------------
# StreamingChatSession
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_session_accumulates_full_text() -> None:
    session = StreamingChatSession("room-1")
    chunks: list[str] = []
    async for c in session.stream(word_chunks("PyAgent rocks")):
        chunks.append(c)

    assert session.is_finished
    assert session.full_text == "PyAgent rocks"
    assert "".join(chunks) == "PyAgent rocks"


@pytest.mark.asyncio
async def test_session_clear_resets_state() -> None:
    session = StreamingChatSession("room-2")
    async for _ in session.stream(word_chunks("test")):
        pass

    session.clear()
    assert not session.is_finished
    assert session.full_text == ""


@pytest.mark.asyncio
async def test_session_not_finished_mid_stream() -> None:
    session = StreamingChatSession("room-3")
    saw_in_progress = False

    async def check_progress():
        nonlocal saw_in_progress
        async for _ in session.stream(word_chunks("a b c d")):
            if not session.is_finished:
                saw_in_progress = True

    await check_progress()
    assert saw_in_progress
    assert session.is_finished


@pytest.mark.asyncio
async def test_session_to_dict() -> None:
    session = StreamingChatSession("my-room")
    async for _ in session.stream(word_chunks("hello world")):
        pass

    d = session.to_dict()
    assert d["room_name"] == "my-room"
    assert d["is_finished"] is True
    assert d["chunk_count"] == 2
    assert d["full_text"] == "hello world"


@pytest.mark.asyncio
async def test_session_multiple_streams() -> None:
    """Each call to stream() should reset and re-accumulate."""
    session = StreamingChatSession("room-4")

    async for _ in session.stream(word_chunks("first run")):
        pass
    assert session.full_text == "first run"

    async for _ in session.stream(word_chunks("second run")):
        pass
    assert session.full_text == "second run"
