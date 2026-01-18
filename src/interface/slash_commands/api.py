"""
High-level API functions for SlashCommands.
"""

from __future__ import annotations

from typing import Any

from src.interface.slash_commands.core import (
    SlashCommands,
    CommandResult,
    ProcessedPrompt,
)

# ============================================================================
# Default Instance
# ============================================================================

_default_slash_commands: SlashCommands | None = None


def get_slash_commands() -> SlashCommands:
    """Get the default SlashCommands instance."""
    global _default_slash_commands
    if _default_slash_commands is None:
        _default_slash_commands = SlashCommands()
    return _default_slash_commands


def reset_slash_commands() -> None:
    """Reset the default instance (for testing)."""
    global _default_slash_commands
    _default_slash_commands = None


# ============================================================================
# Convenience Functions
# ============================================================================

def process_prompt(prompt: str, **kwargs: Any) -> ProcessedPrompt:
    """
    Process a prompt with slash commands.
    
    Args:
        prompt: The input prompt
        **kwargs: Additional options for processing
        
    Returns:
        ProcessedPrompt with results
    """
    return get_slash_commands().process(prompt, **kwargs)


def execute_command(command: str, args: list[str] | None = None, **metadata: Any) -> CommandResult:
    """
    Execute a single slash command.
    
    Args:
        command: Command name (without /)
        args: Command arguments
        **metadata: Additional context
        
    Returns:
        CommandResult
    """
    return get_slash_commands().execute(command, args, **metadata)


def get_help(command: str | None = None) -> str:
    """
    Get help text for commands.
    
    Args:
        command: Specific command name, or None for all
        
    Returns:
        Help text
    """
    return get_slash_commands().get_help(command)
