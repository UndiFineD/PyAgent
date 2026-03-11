#!/usr/bin/env python3
"""Tests for the AgentRegistry class."""


def test_agent_registry_register_and_get() -> None:
    """Test that AgentRegistry can register and retrieve agents."""
    import importlib

    ar_mod = importlib.import_module("src.core.agent_registry")

    assert hasattr(ar_mod, "AgentRegistry"), "AgentRegistry missing"
    assert callable(getattr(ar_mod, "validate", None)), "validate missing"

    reg = ar_mod.AgentRegistry()
    reg.register("x", object())
    assert reg.get("x") is not None

    ar_mod.validate()
