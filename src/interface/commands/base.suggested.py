#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Base types and models for slash commands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, TypeAlias

CommandHandler: TypeAlias = Callable[["CommandContext"], "CommandResult"]
AsyncCommandHandler: TypeAlias = Callable[["CommandContext"], "CommandResult"]


@dataclass
class CommandContext:
    """Context passed to command handlers."""

    command: str
    """The command name (without slash)."""

    args: list[str] = field(default_factory=list)
    """Arguments passed to the command."""

    raw_match: str = ""
    """The raw matched string from the prompt."""

    prompt: str = ""
    """The full original prompt."""

    user_id: str | None = None
    """Optional user identifier."""

    session_id: str | None = None
    """Optional session identifier."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""

    @property
    def arg_string(self) -> str:
        """Get arguments as a single string."""
        return " ".join(self.args)

    @property
    def first_arg(self) -> str | None:
        """Get first argument or None."""
        return self.args[0] if self.args else None


@dataclass
class CommandResult:
    """Result from a command execution."""

    success: bool = True
    """Whether the command executed successfully."""

    output: str = ""
    """The output text to insert/display."""

    data: dict[str, Any] = field(default_factory=dict)
    """Structured data from the command."""

    error: str | None = None
    """Error message if success is False."""

    inline: bool = True
    """Whether output should be inserted inline."""

    @classmethod
    def ok(cls, output: str, data: dict[str, Any] | None = None, inline: bool = True) -> CommandResult:
        """Create a successful result."""
        return cls(success=True, output=output, data=data or {}, inline=inline)

    @classmethod
    def fail(cls, error: str) -> CommandResult:
        """Create a failed result."""
        return cls(success=False, error=error, output=f"[Error: {error}]")


@dataclass
class CommandDefinition:
    """Definition of a slash command."""

    name: str
    """Primary command name."""

    handler: CommandHandler
    """The handler function."""

    description: str = ""
    """Short description for help."""

    usage: str = ""
    """Usage example."""

    aliases: list[str] = field(default_factory=list)
    """Alternative names for the command."""

    hidden: bool = False
    """Whether to hide from help listing."""

    requires_args: bool = False
    """Whether arguments are required."""


@dataclass
class ParsedCommand:
    """A parsed command from the prompt."""

    command: str
    """Command name."""

    args: list[str]
    """Command arguments."""

    start: int
    """Start position in prompt."""

    end: int
    """End position in prompt."""

    raw: str
    """Raw matched text."""


@dataclass
class ProcessedPrompt:
    """Result of processing a prompt."""

    original: str
    """Original prompt text."""

    processed: str
    """Processed prompt with command results."""

    commands: list[ParsedCommand]
    """Parsed commands found."""

    results: list[tuple[ParsedCommand, CommandResult]]
    """Execution results for each command."""

    @property
    def has_commands(self) -> bool:
        """Whether any commands were found."""
        return bool(self.commands)

    @property
    def all_succeeded(self) -> bool:
        """Whether all commands succeeded."""
        return all(r.success for _, r in self.results)

    @property
    def command_outputs(self) -> dict[str, str]:
        """Map of command names to outputs."""
        return {cmd.command: result.output for cmd, result in self.results}

    @property
    def command_data(self) -> dict[str, dict[str, Any]]:
        """Map of command names to structured data."""
        return {cmd.command: result.data for cmd, result in self.results}
