"""
Global command registry and registration utilities.
"""

from __future__ import annotations

from typing import Any, Callable

from src.interface.slash_commands.core import (
    CommandHandler,
    CommandRegistry,
    CommandDefinition,
)

# ============================================================================
# Global Registry
# ============================================================================

_global_registry: CommandRegistry | None = None


def get_global_registry() -> CommandRegistry:
    """Get the global command registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = CommandRegistry()
    return _global_registry


def reset_global_registry() -> None:
    """Reset the global registry (for testing)."""
    global _global_registry
    if _global_registry:
        _global_registry.clear()
    _global_registry = None


# ============================================================================
# Registration Functions
# ============================================================================

def register(
    name: str,
    *,
    description: str = "",
    usage: str = "",
    aliases: list[str] | None = None,
    hidden: bool = False,
    requires_args: bool = False,
    category: str = "general",
) -> Callable[[CommandHandler], CommandHandler]:
    """
    Decorator to register a command with the global registry.

    Example:
        @register("greet", description="Greet someone", aliases=["hi"])
        def cmd_greet(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok(f"Hello, {ctx.first_arg or 'world'}!")
    """
    def decorator(handler: CommandHandler) -> CommandHandler:
        get_global_registry().register(
            name,
            handler,
            description=description,
            usage=usage,
            aliases=aliases,
            hidden=hidden,
            requires_args=requires_args,
            category=category,
        )
        return handler
    return decorator


def register_command(
    name: str,
    handler: CommandHandler,
    **kwargs: Any,
) -> CommandDefinition:
    """
    Register a command function with the global registry.

    Args:
        name: Command name
        handler: Handler function
        **kwargs: Additional command options

    Returns:
        The command definition
    """
    return get_global_registry().register(name, handler, **kwargs)


def command(name: str, **kwargs: Any) -> Callable[[CommandHandler], CommandHandler]:
    """Alias for register() decorator."""
    return register(name, **kwargs)


def unregister(name: str) -> bool:
    """Remove a command from the global registry."""
    return get_global_registry().unregister(name)


def enable_command(name: str) -> bool:
    """Enable a command."""
    return get_global_registry().enable(name)


def disable_command(name: str) -> bool:
    """Disable a command."""
    return get_global_registry().disable(name)


def list_commands(
    include_hidden: bool = False,
    include_disabled: bool = False,
    category: str | None = None,
) -> list[CommandDefinition]:
    """List all registered commands."""
    return get_global_registry().list_commands(
        include_hidden=include_hidden,
        include_disabled=include_disabled,
        category=category,
    )
