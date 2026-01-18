"""
SlashCommands - Chat prompt slash command parser and executor.

Provides backward compatibility for the moved SlashCommands implementation.
Moved to src/interface/commands/
"""

from .commands import (
    CommandParser,
    SlashCommands,
    CommandContext,
    CommandResult,
    CommandDefinition,
    CommandRegistry,
    ParsedCommand,
    ProcessedPrompt,
    parse_commands,
    get_slash_commands,
    process_prompt,
    execute_command,
    register_command,
    command,
)

__all__ = [
    # Classes
    "SlashCommands",
    "CommandParser",
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
