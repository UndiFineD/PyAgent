#!/usr/bin/env python3
"""Presence test for agent_state_manager module."""

from src.core import agent_state_manager


def test_module_imports_and_validate() -> None:
    agent_state_manager.validate()
    assert True
