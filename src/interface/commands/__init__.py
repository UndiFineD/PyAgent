"""
Slash commands package.
"""

from __future__ import annotations

from typing import Any, Callable

from .Base import (
    CommandContext,
    CommandResult,
    CommandDefinition,
    ParsedCommand,
    ProcessedPrompt,
    CommandHandler,
    AsyncCommandHandler
)
from .Registry import CommandRegistry
from .Parser import CommandParser, SlashCommands, parse_commands

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
