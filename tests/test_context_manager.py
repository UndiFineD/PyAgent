#!/usr/bin/env python
"""Tests for the ContextManager class."""

import asyncio
import importlib
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, cast


class ContextManagerProtocol(Protocol):
    """Protocol for ContextManager behavior used by these tests."""

    async def push(self, text: str) -> None:
        """Push text into the context."""

    def snapshot(self) -> str:
        """Return the current context snapshot."""


def _load_context_manager_factory() -> Callable[..., ContextManagerProtocol]:
    """Load ContextManager dynamically to avoid requiring import stubs for context_manager."""
    context_module = importlib.import_module("context_manager")
    return cast(Callable[..., ContextManagerProtocol], context_module.ContextManager)


def test_context_manager_basic(tmp_path: Path) -> None:
    """Test basic push and snapshot functionality of ContextManager."""
    _ = tmp_path
    context_manager_factory = _load_context_manager_factory()

    async def inner() -> None:
        """Test pushing text and taking a snapshot."""
        cm = context_manager_factory(max_tokens=10)
        await cm.push("hello world")
        assert cm.snapshot() == "hello world"

    asyncio.run(inner())


def test_context_manager_windowing(tmp_path: Path) -> None:
    """Test the windowing behavior of ContextManager."""
    _ = tmp_path
    context_manager_factory = _load_context_manager_factory()

    async def inner() -> None:
        """Test that ContextManager prunes old segments when max_tokens is exceeded."""
        cm = context_manager_factory(max_tokens=3)  # count words as tokens
        await cm.push("one")
        await cm.push("two")
        await cm.push("three")
        await cm.push("four")
        # after pushing fourth word with max_tokens=3, oldest segment should be pruned
        assert cm.snapshot() == "two" + "three" + "four"

    asyncio.run(inner())
