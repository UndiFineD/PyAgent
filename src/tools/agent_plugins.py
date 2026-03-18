#!/usr/bin/env python3
"""Agent plugins for extending PyAgent's capabilities."""

from pathlib import Path
from typing import Any

PLUGIN_DIR = Path(__file__).parent / "plugins"
PLUGIN_DIR.mkdir(exist_ok=True)


def load_plugins() -> Any:
    """Load extra behaviours from the plugins directory.
    Currently a stub; real implementation would dynamically
    import modules and return a list of loaded plugin references.
    """
    return []
