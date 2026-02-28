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
Command registry for slash commands.
"""

from __future__ import annotations

from typing import Callable

from .base import CommandDefinition, CommandHandler


class CommandRegistry:
    """Registry for slash commands."""

    def __init__(self) -> None:
        self._commands: dict[str, CommandDefinition] = {}
        self._aliases: dict[str, str] = {}

    def register(
        self,
        name: str,
        handler: CommandHandler,
        *,
        description: str = "",
        usage: str = "",
        aliases: list[str] | None = None,
        hidden: bool = False,
        requires_args: bool = False,
    ) -> None:
        """Register a command."""
        defn = CommandDefinition(
            name=name,
            handler=handler,
            description=description,
            usage=usage,
            aliases=aliases or [],
            hidden=hidden,
            requires_args=requires_args,
        )
        self._commands[name] = defn

        # Register aliases
        for alias in defn.aliases:
            self._aliases[alias] = name

    def get(self, name: str) -> CommandDefinition | None:
        """Get a command by name or alias."""
        # Check aliases first
        if name in self._aliases:
            name = self._aliases[name]
        return self._commands.get(name)

    def list_commands(self, include_hidden: bool = False) -> list[CommandDefinition]:
        """List all registered commands."""
        return [cmd for cmd in self._commands.values() if include_hidden or not cmd.hidden]

    def command(
        self,
        name: str,
        *,
        description: str = "",
        usage: str = "",
        aliases: list[str] | None = None,
        hidden: bool = False,
        requires_args: bool = False,
    ) -> Callable[[CommandHandler], CommandHandler]:
        """Decorator to register a command."""

        def decorator(handler: CommandHandler) -> CommandHandler:
            self.register(
                name,
                handler,
                description=description,
                usage=usage,
                aliases=aliases,
                hidden=hidden,
                requires_args=requires_args,
            )
            return handler

        return decorator
