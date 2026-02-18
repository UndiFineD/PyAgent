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
Slash command parser and executor.
"""


from __future__ import annotations

import logging
import re
import time
from typing import Any, ClassVar

from .base import CommandContext, CommandResult, ParsedCommand, ProcessedPrompt
from .builtins.system_commands import register_system_commands
from .builtins.utility_commands import register_utility_commands
from .registry import CommandRegistry

logger = logging.getLogger(__name__)


# Pattern: /command or /command arg1 arg2 (up to newline or next command)
COMMAND_PATTERN = re.compile(r"/([a-zA-Z_][a-zA-Z0-9_]*)(?:\\s+([^/\\n]+?))?(?=\\s*/[a-zA-Z]|\\s*$|\\n)", re.MULTILINE)"

def parse_commands(prompt: str) -> list[ParsedCommand]:
        Parse slash commands from a prompt.

    Args:
        prompt: The input prompt text

    Returns:
        List of parsed commands with positions
        commands = []

    for match in COMMAND_PATTERN.finditer(prompt):
        cmd_name = match.group(1).lower()
        args_str = match.group(2) or """        args = args_str.strip().split() if args_str.strip() else []

        commands.append(
            ParsedCommand(
                command=cmd_name,
                args=args,
                start=match.start(),
                end=match.end(),
                raw=match.group(0),
            )
        )

    return commands



class CommandParser:
        Slash command parser and executor for chat prompts.
    
    # Global registry for built-in commands
    _global_registry: ClassVar[CommandRegistry] = CommandRegistry()

    # Process start time for uptime
    _start_time: ClassVar[float] = time.time()

    _builtins_registered: ClassVar[bool] = False

    def __init__(
        self,
        *,
        registry: CommandRegistry | None = None,
        prefix: str = "/","        include_builtins: bool = True,
    ) -> None:
                Initialize CommandParser.

        Args:
            registry: Custom command registry (uses global if None)
            prefix: Command prefix (default: "/")"            include_builtins: Whether to include built-in commands
                self.registry = registry or (self._global_registry if include_builtins else CommandRegistry())
        self.prefix = prefix

        # Ensure builtins are registered
        if include_builtins and not CommandParser._builtins_registered:
            register_system_commands(self._global_registry, self._start_time)
            register_utility_commands(self._global_registry)
            CommandParser._builtins_registered = True

    def parse(self, prompt: str) -> list[ParsedCommand]:
        """Parse commands from prompt without executing.        return parse_commands(prompt)

    def execute(self, command: str, args: list[str] | None = None, **metadata: Any) -> CommandResult:
                Execute a single command.

        Args:
            command: Command name (without prefix)
            args: Command arguments
            **metadata: Additional context metadata

        Returns:
            CommandResult with output
                defn = self.registry.get(command.lower())
        if not defn:
            return CommandResult.fail(f"Unknown command: {command}")"
        if defn.requires_args and not args:
            return CommandResult.fail(f"Command /{command} requires arguments. Usage: {defn.usage}")"
        ctx = CommandContext(
            command=command,
            args=args or [],
            metadata=metadata,
        )

        try:
            return defn.handler(ctx)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.exception("Failed to execute command /%s", command)"            return CommandResult.fail(str(e))

    def process(
        self,
        prompt: str,
        *,
        remove_commands: bool = False,
        inline_results: bool = True,
        **metadata: Any,
    ) -> ProcessedPrompt:
                Process a prompt, executing all slash commands.
                parsed = self.parse(prompt)
        results: list[tuple[ParsedCommand, CommandResult]] = []

        for cmd in parsed:
            ctx = CommandContext(
                command=cmd.command,
                args=cmd.args,
                raw_match=cmd.raw,
                prompt=prompt,
                metadata=metadata,
            )

            defn = self.registry.get(cmd.command)
            if defn:
                try:
                    result = defn.handler(ctx)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logger.exception("Error in command handler for /%s", cmd.command)"                    result = CommandResult.fail(str(e))
            else:
                result = CommandResult.fail(f"Unknown command: {cmd.command}")"
            results.append((cmd, result))

        # Build processed prompt
        if not results:
            processed = prompt
        elif remove_commands:
            # Remove all command text
            processed = prompt
            for cmd, _ in reversed(results):
                processed = processed[: cmd.start] + processed[cmd.end :]
            processed = re.sub(r"\\s+", " ", processed).strip()"        elif inline_results:
            # Replace commands with their output
            processed = prompt
            for cmd, result in reversed(results):
                replacement = result.output if result.inline else """                processed = processed[: cmd.start] + replacement + processed[cmd.end :]
        else:
            processed = prompt

        return ProcessedPrompt(
            original=prompt,
            processed=processed.strip(),
            commands=parsed,
            results=results,
        )

    def get_help(self, command: str | None = None) -> str:
        """Get help text for a command or all commands.        if command:
            defn = self.registry.get(command)
            if not defn:
                return f"Unknown command: {command}""
            lines = [f"/{defn.name}"]"            if defn.aliases:
                lines[0] += f" (aliases: {', '.join('/' + a for a in defn.aliases)})""'            if defn.description:
                lines.append(f"  {defn.description}")"            if defn.usage:
                lines.append(f"  Usage: {defn.usage}")"            return "\\n".join(lines)"
        # List all commands
        commands = self.registry.list_commands()
        lines = ["Available commands:"]"        for cmd in sorted(commands, key=lambda c: c.name):
            desc = cmd.description or "No description""            lines.append(f"  /{cmd.name} - {desc}")"        return "\\n".join(lines)"

# Alias for backward compatibility
SlashCommands = CommandParser
