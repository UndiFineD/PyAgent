"""
SlashCommands - Modular command system for chat prompts.

Commands are organized in the `commands/` subdirectory and auto-discovered.
Each command module should use the @register decorator to register handlers.

Example command module (commands/greet.py):
    from src.interface.slash_commands import register, CommandContext, CommandResult

    @register("greet", description="Greet someone", aliases=["hi", "hello"])
    def cmd_greet(ctx: CommandContext) -> CommandResult:
        return CommandResult.ok(f"[Hello, {ctx.first_arg or 'world'}!]")

Phase 24: Advanced Observability & Parsing
"""

from src.interface.slash_commands.core import (
    SlashCommands,
    CommandContext,
    CommandResult,
    CommandDefinition,
    CommandRegistry,
    ParsedCommand,
    ProcessedPrompt,
    parse_commands,
)
from src.interface.slash_commands.registry import (
    get_global_registry,
    register,
    register_command,
    command,
)
from src.interface.slash_commands.loader import (
    load_commands,
    discover_command_modules,
    reload_commands,
)

# Convenience functions
from src.interface.slash_commands.api import (
    get_slash_commands,
    process_prompt,
    execute_command,
)

__all__ = [
    # Core classes
    "SlashCommands",
    "CommandContext",
    "CommandResult",
    "CommandDefinition",
    "CommandRegistry",
    "ParsedCommand",
    "ProcessedPrompt",
    # Parsing
    "parse_commands",
    # Registry
    "get_global_registry",
    "register",
    "register_command",
    "command",
    # Loader
    "load_commands",
    "discover_command_modules",
    "reload_commands",
    # API
    "get_slash_commands",
    "process_prompt",
    "execute_command",
]
