#!/usr/bin/env python3
"""Tests for the plugin loader in the tools directory."""

import os


def test_plugin_loader_creates_directory() -> None:
    """Importing the plugin loader should create the plugins directory under src/tools."""
    # importing the module should create the plugins directory under src/tools
    import tools.agent_plugins  # noqa: F401

    assert os.path.isdir(os.path.join("src", "tools", "plugins"))
