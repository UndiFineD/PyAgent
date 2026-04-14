#!/usr/bin/env python3
"""Agent plugins for extending PyAgent's capabilities."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool

PLUGIN_DIR = Path(__file__).parent / "plugins"
PLUGIN_DIR.mkdir(exist_ok=True)


def _load_plugin(path: Path) -> str | None:
    """Load a single plugin file and return its module name if successful."""
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[arg-type]
        return name
    return None


def load_plugins() -> list[str]:
    """Load extra behaviours from the plugins directory."""
    return list(filter(None, map(_load_plugin, sorted(PLUGIN_DIR.glob("*.py")))))


def main(args: list[str] | None = None) -> int:
    """Main entry point for the agent_plugins tool."""
    parser = argparse.ArgumentParser(prog="agent_plugins")
    parser.add_argument("--list", action="store_true", help="List available plugin modules")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    parsed = parser.parse_args(args=args)
    plugins = load_plugins()

    if parsed.json:
        print(json.dumps({"plugins": plugins}, indent=2))
    else:
        print("\n".join(plugins))

    return 0


register_tool("agent_plugins", main, "Load and list custom agent plugins")
