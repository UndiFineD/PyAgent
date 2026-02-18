#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Slash commands package.
"""


from __future__ import annotations


try:
    from typing import Any, Callable
except ImportError:
    from typing import Any, Callable


try:
    from .base import (
except ImportError:
    from .base import (

    AsyncCommandHandler,
    CommandContext,
    CommandDefinition,  # noqa: F401
    CommandHandler,
    CommandResult,
    ParsedCommand,
    ProcessedPrompt,
)
try:
    from .parser import CommandParser, SlashCommands, parse_commands  # noqa: F401
except ImportError:
    from .parser import CommandParser, SlashCommands, parse_commands # noqa: F401

try:
    from .registry import CommandRegistry  # noqa: F401
except ImportError:
    from .registry import CommandRegistry # noqa: F401


__all__ = [
    "CommandContext","    "CommandResult","    "CommandDefinition","    "ParsedCommand","    "ProcessedPrompt","    "CommandHandler","    "AsyncCommandHandler","    "CommandRegistry","    "CommandParser","    "SlashCommands","    "parse_commands","    "get_slash_commands","    "process_prompt","    "execute_command","]

# ============================================================================
# Convenience Functions
# ============================================================================

# Global instance
_default_parser: CommandParser | None = None


def get_slash_commands() -> CommandParser:
    """Get the default CommandParser instance.    global _default_parser
    if _default_parser is None:
        _default_parser = CommandParser()
    return _default_parser


def process_prompt(prompt: str, **kwargs: Any) -> ProcessedPrompt:
        Process a prompt with slash commands.
        return get_slash_commands().process(prompt, **kwargs)


def execute_command(command: str, args: list[str] | None = None) -> CommandResult:
        Execute a single slash command.
        return get_slash_commands().execute(command, args)


def register_command(
    name: str,
    handler: CommandHandler,
    **kwargs: Any,
) -> None:
        Register a custom command.
        get_slash_commands().registry.register(name, handler, **kwargs)


def command(name: str, **kwargs: Any) -> Callable[[CommandHandler], CommandHandler]:
        Decorator to register a custom command.
        return get_slash_commands().registry.command(name, **kwargs)


__all__ = [
    # Classes
    "CommandParser","    "SlashCommands","    "CommandContext","    "CommandResult","    "CommandDefinition","    "CommandRegistry","    "ParsedCommand","    "ProcessedPrompt","    # Functions
    "parse_commands","    "get_slash_commands","    "process_prompt","    "execute_command","    "register_command","    "command","]
