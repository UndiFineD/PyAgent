#!/usr/bin/env python3
"""Integration tests for context management and skills registry."""

from pathlib import Path

import pytest

from context_manager import ContextManager
from cort import ChainOfThought
from skills_registry import SkillsRegistry


@pytest.mark.asyncio
async def test_context_and_skills(tmp_path: Path) -> None:
    """Test the integration of ContextManager, SkillsRegistry, and ChainOfThought."""
    cm = ContextManager(max_tokens=5)
    assert hasattr(cm, "push")
    registry = SkillsRegistry(tmp_path / "skills")
    skills = await registry.list_skills()
    assert isinstance(skills, list)
    cort = ChainOfThought(cm)
    root = await cort.new_node("start")
    child = await root.fork("x")
    await child.add("y")
    assert "y" in cm.snapshot()
