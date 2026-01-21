"""
Core classes for SlashCommands system.

Contains the fundamental types and parsing logic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, TypeAlias

# ============================================================================
# Types
# ============================================================================

CommandHandler: TypeAlias = Callable[["CommandContext"], "CommandResult"]


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
    
    @property
    def rest_args(self) -> list[str]:
        """Get all arguments except the first."""
        return self.args[1:]


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
    
    category: str = "general"
    """Command category for grouping."""
    
    enabled: bool = True
    """Whether the command is enabled."""


# ============================================================================
# Command Registry
# ============================================================================

class CommandRegistry:
    """Registry for slash commands."""
    
    def __init__(self) -> None:
        self._commands: dict[str, CommandDefinition] = {}
        self._aliases: dict[str, str] = {}
        self._disabled: set[str] = set()
    
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
        category: str = "general",
        enabled: bool = True,
    ) -> CommandDefinition:
        """Register a command."""
        defn = CommandDefinition(
            name=name,
            handler=handler,
            description=description,
            usage=usage,
            aliases=aliases or [],
            hidden=hidden,
            requires_args=requires_args,
            category=category,
            enabled=enabled,
        )
        self._commands[name] = defn
        
        # Register aliases
        for alias in defn.aliases:
            self._aliases[alias] = name
        
        return defn
    
    def unregister(self, name: str) -> bool:
        """Unregister a command by name."""
        if name not in self._commands:
            return False
        
        defn = self._commands.pop(name)
        
        # Remove aliases
        for alias in defn.aliases:
            self._aliases.pop(alias, None)
        
        return True
    
    def get(self, name: str) -> CommandDefinition | None:
        """Get a command by name or alias."""
        # Check aliases first
        if name in self._aliases:
            name = self._aliases[name]
        
        defn = self._commands.get(name)
        if defn and defn.enabled and name not in self._disabled:
            return defn
        return None
    
    def get_all(self, name: str) -> CommandDefinition | None:
        """Get a command even if disabled."""
        if name in self._aliases:
            name = self._aliases[name]
        return self._commands.get(name)
    
    def enable(self, name: str) -> bool:
        """Enable a command."""
        self._disabled.discard(name)
        if name in self._commands:
            self._commands[name].enabled = True
            return True
        return False
    
    def disable(self, name: str) -> bool:
        """Disable a command."""
        if name in self._commands:
            self._disabled.add(name)
            return True
        return False
    
    def is_enabled(self, name: str) -> bool:
        """Check if a command is enabled."""
        return name in self._commands and name not in self._disabled
    
    def list_commands(
        self,
        include_hidden: bool = False,
        include_disabled: bool = False,
        category: str | None = None,
    ) -> list[CommandDefinition]:
        """List registered commands."""
        result = []
        for cmd in self._commands.values():
            if not include_hidden and cmd.hidden:
                continue
            if not include_disabled and (not cmd.enabled or cmd.name in self._disabled):
                continue
            if category and cmd.category != category:
                continue
            result.append(cmd)
        return result
    
    def list_categories(self) -> list[str]:
        """List all command categories."""
        return sorted(set(cmd.category for cmd in self._commands.values()))
    
    def command(
        self,
        name: str,
        *,
        description: str = "",
        usage: str = "",
        aliases: list[str] | None = None,
        hidden: bool = False,
        requires_args: bool = False,
        category: str = "general",
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
                category=category,
            )
            return handler
        return decorator
    
    def clear(self) -> None:
        """Clear all registered commands."""
        self._commands.clear()
        self._aliases.clear()
        self._disabled.clear()


# ============================================================================
# Slash Command Parser
# ============================================================================

# Pattern: /command or /command arg1 arg2 (up to newline or next command)
COMMAND_PATTERN = re.compile(
    r'/([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+([^/\n]+?))?(?=\s*/[a-zA-Z]|\s*$|\n)',
    re.MULTILINE
)


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


def parse_commands(prompt: str) -> list[ParsedCommand]:
    """
    Parse slash commands from a prompt.
    
    Args:
        prompt: The input prompt text
        
    Returns:
        List of parsed commands with positions
    """
    commands = []
    
    for match in COMMAND_PATTERN.finditer(prompt):
        cmd_name = match.group(1).lower()
        args_str = match.group(2) or ""
        args = args_str.strip().split() if args_str.strip() else []
        
        commands.append(ParsedCommand(
            command=cmd_name,
            args=args,
            start=match.start(),
            end=match.end(),
            raw=match.group(0),
        ))
    
    return commands


# ============================================================================
# SlashCommands Class
# ============================================================================

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


class SlashCommands:
    """
    Slash command parser and executor for chat prompts.
    
    Example:
        >>> slash = SlashCommands()
        >>> result = slash.process("What is /datetime the current time?")
        >>> print(result.processed_prompt)
        "What is [2026-01-17 10:30:00 UTC] the current time?"
    """
    
    def __init__(
        self,
        *,
        registry: CommandRegistry | None = None,
        prefix: str = "/",
        auto_load: bool = True,
    ) -> None:
        """
        Initialize SlashCommands.
        
        Args:
            registry: Custom command registry (creates new if None)
            prefix: Command prefix (default: "/")
            auto_load: Whether to auto-load built-in commands
        """
        from src.interface.slash_commands.registry import get_global_registry
        
        self.registry = registry or get_global_registry()
        self.prefix = prefix
        
        if auto_load:
            from src.interface.slash_commands.loader import load_commands
            load_commands(self.registry)
    
    def parse(self, prompt: str) -> list[ParsedCommand]:
        """Parse commands from prompt without executing."""
        return parse_commands(prompt)
    
    def execute(self, command: str, args: list[str] | None = None, **metadata: Any) -> CommandResult:
        """
        Execute a single command.
        
        Args:
            command: Command name (without prefix)
            args: Command arguments
            **metadata: Additional context metadata
            
        Returns:
            CommandResult with output
        """
        defn = self.registry.get(command.lower())
        if not defn:
            return CommandResult.fail(f"Unknown command: {command}")
        
        if defn.requires_args and not args:
            return CommandResult.fail(f"Command /{command} requires arguments. Usage: {defn.usage}")
        
        ctx = CommandContext(
            command=command,
            args=args or [],
            metadata=metadata,
        )
        
        try:
            return defn.handler(ctx)
        except Exception as e:
            return CommandResult.fail(str(e))
    
    def process(
        self,
        prompt: str,
        *,
        remove_commands: bool = False,
        inline_results: bool = True,
        **metadata: Any,
    ) -> ProcessedPrompt:
        """
        Process a prompt, executing all slash commands.
        
        Args:
            prompt: The input prompt
            remove_commands: Remove commands from output (vs inline results)
            inline_results: Insert results inline at command positions
            **metadata: Additional context for handlers
            
        Returns:
            ProcessedPrompt with results and modified text
        """
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
                except Exception as e:
                    result = CommandResult.fail(str(e))
            else:
                result = CommandResult.fail(f"Unknown command: {cmd.command}")
            
            results.append((cmd, result))
        
        # Build processed prompt
        if not results:
            processed = prompt
        elif remove_commands:
            # Remove all command text
            processed = prompt
            for cmd, _ in reversed(results):  # Reverse to preserve positions
                processed = processed[:cmd.start] + processed[cmd.end:]
            processed = re.sub(r'\s+', ' ', processed).strip()
        elif inline_results:
            # Replace commands with their output
            processed = prompt
            for cmd, result in reversed(results):
                replacement = result.output if result.inline else ""
                processed = processed[:cmd.start] + replacement + processed[cmd.end:]
        else:
            processed = prompt
        
        return ProcessedPrompt(
            original=prompt,
            processed=processed.strip(),
            commands=parsed,
            results=results,
        )
    
    def get_help(self, command: str | None = None) -> str:
        """Get help text for a command or all commands."""
        if command:
            defn = self.registry.get(command)
            if not defn:
                return f"Unknown command: {command}"
            
            lines = [f"/{defn.name}"]
            if defn.aliases:
                lines[0] += f" (aliases: {', '.join('/' + a for a in defn.aliases)})"
            if defn.description:
                lines.append(f"  {defn.description}")
            if defn.usage:
                lines.append(f"  Usage: {defn.usage}")
            return "\n".join(lines)
        
        # List all commands by category
        categories = self.registry.list_categories()
        lines = ["Available commands:"]
        
        for cat in categories:
            commands = self.registry.list_commands(category=cat)
            if commands:
                lines.append(f"\n[{cat.title()}]")
                for cmd in sorted(commands, key=lambda c: c.name):
                    desc = cmd.description or "No description"
                    lines.append(f"  /{cmd.name} - {desc}")
        
        return "\n".join(lines)
