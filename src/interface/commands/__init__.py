#!/usr/bin/env python3
from __future__ import annotations
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
Slash commands package.
"""


from typing import Any, Callable

# Certain test modules import this package under the name
# `src.interface.commands` which breaks normal relative imports.  To avoid
# the resulting ModuleNotFoundError we bypass Python's import machinery and
# load the local files directly by path.  This loader works regardless of
# how the package is named on sys.path.
import importlib.util, os, sys

_pkg_dir = os.path.dirname(__file__)

def _load_local(module_name: str):
    """Dynamically load a submodule from the same directory.

    The returned module object is also inserted into sys.modules under both
    the true package name and the possibly prefixed ``src.`` variant so that
    subsequent imports behave normally.
    """
    path = os.path.join(_pkg_dir, f"{module_name}.py")
    # determine possible qualified names
    candidates = []
    if __name__.startswith("src."):
        candidates.append(f"{__name__}.{module_name}")
    candidates.append(f"interface.commands.{module_name}")
    spec = importlib.util.spec_from_file_location(candidates[0], path)
    mod = importlib.util.module_from_spec(spec)
    # register under all candidate names
    for name in candidates:
        sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

# load the pieces we need
_base_mod = _load_local("base")
# registry must come before parser because parser imports builtins which
# in turn perform relative imports back to the registry.  If registry isn't
# loaded yet the relative import will fail with ModuleNotFoundError.
_registry_mod = _load_local("registry")
_parser_mod = _load_local("parser")

AsyncCommandHandler = _base_mod.AsyncCommandHandler
CommandContext = _base_mod.CommandContext
CommandDefinition = _base_mod.CommandDefinition
CommandHandler = _base_mod.CommandHandler
CommandResult = _base_mod.CommandResult
ParsedCommand = _base_mod.ParsedCommand
ProcessedPrompt = _base_mod.ProcessedPrompt

CommandParser = _parser_mod.CommandParser
SlashCommands = _parser_mod.SlashCommands
parse_commands = _parser_mod.parse_commands

CommandRegistry = _registry_mod.CommandRegistry


__all__ = [
    "CommandContext",
    "CommandResult",
    "CommandDefinition",
    "ParsedCommand",
    "ProcessedPrompt",
    "CommandHandler",
    "AsyncCommandHandler",
    "CommandRegistry",
    "CommandParser",
    "SlashCommands",
    "parse_commands",
    "get_slash_commands",
    "process_prompt",
    "execute_command",
]

# ============================================================================
# Convenience Functions
# ============================================================================

# Global instance
_default_parser: CommandParser | None = None


def get_slash_commands() -> CommandParser:
    """Get the default CommandParser instance."""
    global _default_parser
    if _default_parser is None:
        _default_parser = CommandParser()
    return _default_parser


def process_prompt(prompt: str, **kwargs: Any) -> ProcessedPrompt:
    """
    Process a prompt with slash commands.
    """
    return get_slash_commands().process(prompt, **kwargs)


def execute_command(command: str, args: list[str] | None = None) -> CommandResult:
    """
    Execute a single slash command.
    """
    return get_slash_commands().execute(command, args)


def register_command(
    name: str,
    handler: CommandHandler,
    **kwargs: Any,
) -> None:
    """
    Register a custom command.
    """
    get_slash_commands().registry.register(name, handler, **kwargs)


def command(name: str, **kwargs: Any) -> Callable[[CommandHandler], CommandHandler]:
    """
    Decorator to register a custom command.
    """
    return get_slash_commands().registry.command(name, **kwargs)


__all__ = [
    # Classes
    "CommandParser",
    "SlashCommands",
    "CommandContext",
    "CommandResult",
    "CommandDefinition",
    "CommandRegistry",
    "ParsedCommand",
    "ProcessedPrompt",
    # Functions
    "parse_commands",
    "get_slash_commands",
    "process_prompt",
    "execute_command",
    "register_command",
    "command",
]
