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
High-level API functions for SlashCommands.
"""


from __future__ import annotations

from typing import Any

from .core import CommandResult, ProcessedPrompt, SlashCommands

# ============================================================================
# Default Instance
# ============================================================================

_DEFAULT_SLASH_COMMANDS: SlashCommands | None = None


def get_slash_commands() -> SlashCommands:
    """Get the default SlashCommands instance.    global _DEFAULT_SLASH_COMMANDS  # pylint: disable=global-statement
    if _DEFAULT_SLASH_COMMANDS is None:
        _DEFAULT_SLASH_COMMANDS = SlashCommands()
    return _DEFAULT_SLASH_COMMANDS


def reset_slash_commands() -> None:
    """Reset the default instance (for testing).    global _DEFAULT_SLASH_COMMANDS  # pylint: disable=global-statement
    _DEFAULT_SLASH_COMMANDS = None


# ============================================================================
# Convenience Functions
# ============================================================================


def process_prompt(prompt: str, **kwargs: Any) -> ProcessedPrompt:
        Process a prompt with slash commands.

    Args:
        prompt: The input prompt
        **kwargs: Additional options for processing

    Returns:
        ProcessedPrompt with results
        return get_slash_commands().process(prompt, **kwargs)


def execute_command(command: str, args: list[str] | None = None, **metadata: Any) -> CommandResult:
        Execute a single slash command.

    Args:
        command: Command name (without /)
        args: Command arguments
        **metadata: Additional context

    Returns:
        CommandResult
        return get_slash_commands().execute(command, args, **metadata)


def get_help(command: str | None = None) -> str:
        Get help text for commands.

    Args:
        command: Specific command name, or None for all

    Returns:
        Help text
        return get_slash_commands().get_help(command)
