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
"""Allowlist-validated plugin loader.

Plugins are plain Python modules.  Only modules whose names appear in the
caller-supplied *allowed* list may be loaded.  This prevents arbitrary
module injection.

Usage example::

    from src.tools.plugin_loader import load_plugin, discover_plugins

    # Discover available plugins under a directory
    available = discover_plugins("src/tools/plugins")

    # Load one by allowlisted name
    plugin = load_plugin("my_plugin", allowed=available)
    plugin.run()
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from types import ModuleType
from typing import Any

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def discover_plugins(plugin_dir: str) -> list[str]:
    """Return a sorted list of plugin names found in *plugin_dir*.

    A plugin is any ``.py`` file (excluding ``__init__.py`` and files starting
    with ``_``).

    Parameters
    ----------
    plugin_dir:
        Directory to scan for plugin modules.

    Returns
    -------
    list[str]
        Sorted plugin names (without the ``.py`` extension).

    """
    if not os.path.isdir(plugin_dir):
        return []

    names: list[str] = [
        entry.name[:-3]
        for entry in os.scandir(plugin_dir)
        if entry.is_file() and entry.name.endswith(".py") and not entry.name.startswith("_")
    ]
    return sorted(names)


def load_plugin(name: str, allowed: list[str], plugin_dir: str | None = None) -> ModuleType:
    """Load a plugin module by name after validating it against an allowlist.

    Parameters
    ----------
    name:
        Plugin module name (no path separators or package dots allowed).
    allowed:
        Explicit allowlist of permitted plugin names.  The plugin is rejected
        unless *name* appears in this list.
    plugin_dir:
        Optional directory to load the plugin from.  When provided the plugin
        file is resolved from this directory.  When omitted the module must
        already be importable via ``sys.path``.

    Returns
    -------
    ModuleType
        The loaded plugin module.

    Raises
    ------
    ValueError
        If *name* is not in *allowed*, contains path separators, or contains
        package-level dots (to prevent directory traversal / injection).
    ImportError
        If the module cannot be found or fails to import.

    """
    # Validate the name is a simple identifier — prevents traversal and injection
    if not name or os.sep in name or "/" in name or "\\" in name or name.startswith("."):
        raise ValueError(f"Invalid plugin name: {name!r}. Must be a plain identifier.")
    if "." in name:
        raise ValueError(
            f"Plugin name {name!r} contains dots. Use a simple module name, not a package path."
        )

    if name not in allowed:
        raise ValueError(
            f"Plugin {name!r} is not in the allowed list. "
            f"Allowed plugins: {sorted(allowed)}"
        )

    if plugin_dir is not None:
        plugin_path = os.path.join(plugin_dir, f"{name}.py")
        if not os.path.isfile(plugin_path):
            raise ImportError(f"Plugin file not found: {plugin_path}")

        spec = importlib.util.spec_from_file_location(name, plugin_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create spec for plugin: {plugin_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules.setdefault(name, module)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module

    # Fallback: import via sys.path (module must already be importable)
    return importlib.import_module(name)


def get_plugin_attr(name: str, allowed: list[str], attr: str, plugin_dir: str | None = None) -> Any:
    """Load a plugin and return one of its attributes.

    Convenience wrapper around :func:`load_plugin`.

    Parameters
    ----------
    name:
        Plugin module name.
    allowed:
        Allowlist for :func:`load_plugin`.
    attr:
        Attribute name to retrieve from the loaded module.
    plugin_dir:
        Optional plugin directory.

    Returns
    -------
    Any
        The attribute value.

    Raises
    ------
    AttributeError
        If the attribute does not exist on the loaded module.

    """
    module = load_plugin(name, allowed=allowed, plugin_dir=plugin_dir)
    if not hasattr(module, attr):
        raise AttributeError(f"Plugin {name!r} has no attribute {attr!r}")
    return getattr(module, attr)


def main(args: list[str] | None = None) -> int:
    """List or run a plugin from the CLI."""
    import argparse

    parser = argparse.ArgumentParser(prog="plugin_loader", description="List or invoke PyAgent plugins.")
    sub = parser.add_subparsers(dest="command", required=True)

    ls = sub.add_parser("list", help="List available plugins in a directory")
    ls.add_argument("--dir", default="src/tools/plugins", help="Plugin directory to scan")

    run = sub.add_parser("run", help="Run a plugin's main() function")
    run.add_argument("name", help="Plugin name")
    run.add_argument("--dir", default="src/tools/plugins", help="Plugin directory")
    run.add_argument("--allow", nargs="+", help="Allowlist (defaults to all discovered plugins)")

    parsed = parser.parse_args(args=args)

    if parsed.command == "list":
        plugins = discover_plugins(parsed.dir)
        if not plugins:
            print(f"No plugins found in: {parsed.dir}")
        else:
            print("\n".join(plugins))
        return 0

    if parsed.command == "run":
        plugin_dir = parsed.dir
        available = discover_plugins(plugin_dir)
        allowed = parsed.allow if parsed.allow else available

        try:
            module = load_plugin(parsed.name, allowed=allowed, plugin_dir=plugin_dir)
        except (ValueError, ImportError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        if hasattr(module, "main") and callable(module.main):
            return module.main() or 0
        print(f"Plugin {parsed.name!r} has no callable main()")
        return 1

    return 0


register_tool("plugin_loader", main, "List and invoke allowlist-validated plugins")


if __name__ == "__main__":
    sys.exit(main())
