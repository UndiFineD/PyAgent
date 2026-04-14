#!/usr/bin/env python
"""Tests for context management components."""

import importlib
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, cast

import pytest


class ContextManagerProtocol(Protocol):
    """Protocol for context manager object used in this test."""

    def push(self, *args: object, **kwargs: object) -> object:
        """Push content into the context manager."""


class SkillsRegistryProtocol(Protocol):
    """Protocol for skills registry object used in this test."""

    async def list_skills(self) -> list[str]:
        """Return discovered skills."""


@pytest.mark.asyncio
async def test_context_components_exist(tmp_path: Path) -> None:
    """Ensure ContextManager and SkillsRegistry can be imported and basic API exists."""
    context_module = importlib.import_module("context_manager")
    skills_module = importlib.import_module("skills_registry")

    context_manager_factory = cast(Callable[..., ContextManagerProtocol], context_module.ContextManager)
    skills_registry_factory = cast(Callable[[Path], SkillsRegistryProtocol], skills_module.SkillsRegistry)

    cm = context_manager_factory(max_tokens=5)
    assert hasattr(cm, "push")
    registry = skills_registry_factory(tmp_path / "skills")
    skills = await registry.list_skills()
    assert isinstance(skills, list)
