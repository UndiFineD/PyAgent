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

"""Tests for src/context_manager/window.py — ContextWindow and ContextSegment."""

from __future__ import annotations

import pytest

from context_manager.window import ContextSegment, ContextWindow

# ---------------------------------------------------------------------------
# ContextSegment
# ---------------------------------------------------------------------------


def test_segment_token_count_basic() -> None:
    seg = ContextSegment(text="hello world foo")
    assert seg.token_count == 3


def test_segment_token_count_empty() -> None:
    seg = ContextSegment(text="")
    assert seg.token_count == 0


def test_segment_to_dict_contains_expected_keys() -> None:
    seg = ContextSegment(text="hello", label="user", priority=2, metadata={"turn": 1})
    d = seg.to_dict()
    assert d["text"] == "hello"
    assert d["label"] == "user"
    assert d["priority"] == 2
    assert d["token_count"] == 1
    assert d["metadata"] == {"turn": 1}
    assert "created_at" in d


def test_segment_default_label_and_priority() -> None:
    seg = ContextSegment(text="x")
    assert seg.label == "text"
    assert seg.priority == 1


# ---------------------------------------------------------------------------
# ContextWindow — basic operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_window_push_and_snapshot() -> None:
    win = ContextWindow(max_tokens=100)
    await win.push("hello ", label="user")
    await win.push("world", label="assistant")
    assert win.snapshot() == "hello world"


@pytest.mark.asyncio
async def test_window_token_count() -> None:
    win = ContextWindow(max_tokens=100)
    await win.push("one two three")
    await win.push("four five")
    assert win.token_count == 5


@pytest.mark.asyncio
async def test_window_clear() -> None:
    win = ContextWindow(max_tokens=100)
    await win.push("data")
    win.clear()
    assert win.token_count == 0
    assert win.snapshot() == ""


@pytest.mark.asyncio
async def test_window_push_returns_segment() -> None:
    win = ContextWindow(max_tokens=100)
    seg = await win.push("abc", label="system", priority=5)
    assert isinstance(seg, ContextSegment)
    assert seg.text == "abc"
    assert seg.label == "system"
    assert seg.priority == 5


@pytest.mark.asyncio
async def test_window_to_dict() -> None:
    win = ContextWindow(max_tokens=50)
    await win.push("test content", label="user")
    d = win.to_dict()
    assert d["max_tokens"] == 50
    assert d["token_count"] == 2
    assert len(d["segments"]) == 1


# ---------------------------------------------------------------------------
# ContextWindow — pruning
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_window_prunes_oldest_when_over_budget() -> None:
    """Equal priority → prune oldest first."""
    win = ContextWindow(max_tokens=4)
    await win.push("one two", priority=1)  # 2 tokens
    await win.push("three four", priority=1)  # 2 tokens — total = 4, OK
    await win.push("five six", priority=1)  # 2 tokens — total = 6, must prune

    # Should have pruned "one two" (oldest)
    remaining = [s.text for s in win.segments]
    assert "one two" not in remaining
    assert win.token_count <= 4


@pytest.mark.asyncio
async def test_window_prunes_low_priority_first() -> None:
    """Lower priority segments are pruned before older high-priority ones."""
    win = ContextWindow(max_tokens=4)
    await win.push("system context", priority=10)  # 2 tokens, high pri
    await win.push("user message", priority=1)  # 2 tokens, low pri — total = 4
    await win.push("new data", priority=5)  # 2 tokens — total = 6, must prune

    remaining_texts = [s.text for s in win.segments]
    # Low-priority "user message" should be pruned, not the high-priority system context
    assert "user message" not in remaining_texts
    assert "system context" in remaining_texts


@pytest.mark.asyncio
async def test_window_never_exceeds_max_tokens() -> None:
    win = ContextWindow(max_tokens=5)
    for word in ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta"]:
        await win.push(word)
    assert win.token_count <= 5


@pytest.mark.asyncio
async def test_window_metadata_preserved() -> None:
    win = ContextWindow(max_tokens=100)
    seg = await win.push("hello", metadata={"agent": "coder", "turn": 3})
    assert seg.metadata["agent"] == "coder"
    assert seg.metadata["turn"] == 3


@pytest.mark.asyncio
async def test_window_segments_oldest_first() -> None:
    win = ContextWindow(max_tokens=100)
    await win.push("first")
    await win.push("second")
    await win.push("third")
    texts = [s.text for s in win.segments]
    assert texts == ["first", "second", "third"]
