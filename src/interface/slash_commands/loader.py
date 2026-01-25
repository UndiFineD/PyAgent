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

"""
Command loader - discovers and loads command modules.
"""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interface.slash_commands.core import CommandRegistry

# Track loaded modules
_loaded_modules: set[str] = set()
_COMMANDS_LOADED = False


def get_commands_dir() -> Path:
    """Get the commands directory path."""
    return Path(__file__).parent / "commands"


def discover_command_modules() -> list[str]:
    """
    Discover all command modules in the commands directory.

    Returns:
        List of module names (without .py extension)
    """
    commands_dir = get_commands_dir()

    if not commands_dir.exists():
        return []

    modules = []
    for file in commands_dir.iterdir():
        if file.is_file() and file.suffix == ".py" and not file.name.startswith("_"):
            modules.append(file.stem)

    return sorted(modules)


def load_module(module_name: str) -> bool:
    """
    Load a single command module.

    Args:
        module_name: Name of the module (without .py)

    Returns:
        True if loaded successfully
    """
    full_module_name = f"src.interface.slash_commands.commands.{module_name}"

    if full_module_name in _loaded_modules:
        return True

    try:
        importlib.import_module(full_module_name)
        _loaded_modules.add(full_module_name)
        return True
    except ImportError as e:
        print(f"Warning: Failed to load command module '{module_name}': {e}")
        return False
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Warning: Error loading command module '{module_name}': {e}")
        return False


def unload_module(module_name: str) -> bool:
    """
    Unload a command module (removes from loaded set).

    Note: This doesn't actually unload from sys.modules,
    but prevents it from being reloaded.

    Args:
        module_name: Name of the module

    Returns:
        True if was loaded
    """
    full_module_name = f"src.interface.slash_commands.commands.{module_name}"

    if full_module_name in _loaded_modules:
        _loaded_modules.discard(full_module_name)
        return True
    return False


def load_commands(registry: "CommandRegistry | None" = None) -> int:
    """
    Load all command modules from the commands directory.

    Args:
        registry: Optional registry (not used directly, modules register themselves)

    Returns:
        Number of modules loaded
    """
    global _COMMANDS_LOADED  # pylint: disable=global-statement

    if _COMMANDS_LOADED:
        return len(_loaded_modules)

    _ = registry  # Explicitly mark as unused

    modules = discover_command_modules()
    loaded = 0

    for module_name in modules:
        if load_module(module_name):
            loaded += 1

    _COMMANDS_LOADED = True
    return loaded


def reload_commands() -> int:
    """
    Reload all command modules.

    Returns:
        Number of modules reloaded
    """
    global _COMMANDS_LOADED  # pylint: disable=global-statement

    # Clear loaded state
    _loaded_modules.clear()
    _COMMANDS_LOADED = False

    # Reload
    return load_commands()


def is_loaded(module_name: str) -> bool:
    """Check if a module is loaded."""
    full_module_name = f"src.interface.slash_commands.commands.{module_name}"
    return full_module_name in _loaded_modules


def get_loaded_modules() -> list[str]:
    """Get list of loaded module names."""
    prefix = "src.interface.slash_commands.commands."
    return [m.replace(prefix, "") for m in _loaded_modules]
