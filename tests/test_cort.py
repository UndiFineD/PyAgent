#!/usr/bin/env python
"""Test the ChainOfThought module."""

import pytest

from context_manager import ContextManager
from cort import ChainOfThought


@pytest.mark.asyncio
async def test_cort_simple_branching() -> None:
    """Ensure the ChainOfThought records context correctly while branching."""
    cm = ContextManager(max_tokens=10)
    cort = ChainOfThought(cm)
    root = await cort.new_node("start")
    child = await root.fork("step1")
    await child.add("detail")
    assert "detail" in cm.snapshot()
