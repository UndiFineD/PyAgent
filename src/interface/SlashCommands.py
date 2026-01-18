"""
SlashCommands - Chat prompt slash command parser and executor.

Provides inline command execution for prompts, supporting:
- /datetime, /date, /time - Server date/time info
- /stats - System statistics
- /tokens <text> - Token counting
- /memory - Memory usage
- /cache - Cache statistics
- /health - System health check
- /version - Version information
- /env [key] - Environment info
- /uptime - Process uptime
- /help - List available commands

Multiple commands can be in the same prompt:
    "Hello /datetime what is /stats the weather?"

Phase 24: Advanced Observability & Parsing
"""

from __future__ import annotations

import os
import platform
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Callable, ClassVar, Protocol, TypeAlias

# ============================================================================
# Types
# ============================================================================

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


# ============================================================================
# Command Registry
# ============================================================================

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
        return [
            cmd for cmd in self._commands.values()
            if include_hidden or not cmd.hidden
        ]
    
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

class SlashCommands:
    """
    Slash command parser and executor for chat prompts.
    
    Example:
        >>> slash = SlashCommands()
        >>> result = slash.process("What is /datetime the current time?")
        >>> print(result.processed_prompt)
        "What is [2026-01-17 10:30:00 UTC] the current time?"
    """
    
    # Global registry for built-in commands
    _global_registry: ClassVar[CommandRegistry] = CommandRegistry()
    
    # Process start time for uptime
    _start_time: ClassVar[float] = time.time()
    
    def __init__(
        self,
        *,
        registry: CommandRegistry | None = None,
        prefix: str = "/",
        include_builtins: bool = True,
    ) -> None:
        """
        Initialize SlashCommands.
        
        Args:
            registry: Custom command registry (uses global if None)
            prefix: Command prefix (default: "/")
            include_builtins: Whether to include built-in commands
        """
        self.registry = registry or (self._global_registry if include_builtins else CommandRegistry())
        self.prefix = prefix
        
        # Ensure builtins are registered
        if include_builtins:
            _register_builtins(self._global_registry)
    
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
        
        # List all commands
        commands = self.registry.list_commands()
        lines = ["Available commands:"]
        for cmd in sorted(commands, key=lambda c: c.name):
            desc = cmd.description or "No description"
            lines.append(f"  /{cmd.name} - {desc}")
        return "\n".join(lines)


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
        return len(self.commands) > 0
    
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


# ============================================================================
# Built-in Command Handlers
# ============================================================================

_builtins_registered = False


def _register_builtins(registry: CommandRegistry) -> None:
    """Register built-in commands."""
    global _builtins_registered
    if _builtins_registered:
        return
    _builtins_registered = True
    
    @registry.command(
        "datetime",
        description="Get current server date and time",
        usage="/datetime",
        aliases=["dt", "now"],
    )
    def cmd_datetime(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        local_now = datetime.now()
        
        return CommandResult.ok(
            output=f"[{now.strftime('%Y-%m-%d %H:%M:%S')} UTC]",
            data={
                "utc": now.isoformat(),
                "local": local_now.isoformat(),
                "timestamp": now.timestamp(),
                "timezone": time.tzname[0],
            },
        )
    
    @registry.command(
        "date",
        description="Get current server date",
        usage="/date",
    )
    def cmd_date(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        return CommandResult.ok(
            output=f"[{now.strftime('%Y-%m-%d')}]",
            data={"date": now.strftime('%Y-%m-%d'), "iso": now.date().isoformat()},
        )
    
    @registry.command(
        "time",
        description="Get current server time",
        usage="/time",
    )
    def cmd_time(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        return CommandResult.ok(
            output=f"[{now.strftime('%H:%M:%S')} UTC]",
            data={"time": now.strftime('%H:%M:%S'), "timezone": "UTC"},
        )
    
    @registry.command(
        "stats",
        description="Get system statistics",
        usage="/stats",
        aliases=["sys", "system"],
    )
    def cmd_stats(ctx: CommandContext) -> CommandResult:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        output = (
            f"[CPU: {cpu_percent:.1f}% | "
            f"RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB/{memory.total // (1024**3):.1f}GB) | "
            f"Disk: {disk.percent:.1f}%]"
        )
        
        return CommandResult.ok(
            output=output,
            data={
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "memory_total_gb": memory.total / (1024**3),
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / (1024**3),
                "disk_total_gb": disk.total / (1024**3),
            },
        )
    
    @registry.command(
        "memory",
        description="Get detailed memory usage",
        usage="/memory",
        aliases=["mem", "ram"],
    )
    def cmd_memory(ctx: CommandContext) -> CommandResult:
        import psutil
        
        memory = psutil.virtual_memory()
        process = psutil.Process()
        proc_mem = process.memory_info()
        
        output = (
            f"[System: {memory.used // (1024**2)}MB/{memory.total // (1024**2)}MB "
            f"({memory.percent:.1f}%) | "
            f"Process: {proc_mem.rss // (1024**2)}MB RSS]"
        )
        
        return CommandResult.ok(
            output=output,
            data={
                "system_used_mb": memory.used // (1024**2),
                "system_total_mb": memory.total // (1024**2),
                "system_percent": memory.percent,
                "system_available_mb": memory.available // (1024**2),
                "process_rss_mb": proc_mem.rss // (1024**2),
                "process_vms_mb": proc_mem.vms // (1024**2),
            },
        )
    
    @registry.command(
        "tokens",
        description="Count tokens in text",
        usage="/tokens <text>",
        aliases=["tok", "tokenize"],
        requires_args=True,
    )
    def cmd_tokens(ctx: CommandContext) -> CommandResult:
        text = ctx.arg_string
        
        # Simple token estimation (words + punctuation)
        # For accurate counts, would need tiktoken/tokenizers
        words = len(text.split())
        chars = len(text)
        
        # Rough estimate: ~4 chars per token for English
        estimated_tokens = max(1, chars // 4)
        
        return CommandResult.ok(
            output=f"[~{estimated_tokens} tokens, {words} words, {chars} chars]",
            data={
                "estimated_tokens": estimated_tokens,
                "words": words,
                "characters": chars,
                "text": text,
            },
        )
    
    @registry.command(
        "uptime",
        description="Get process uptime",
        usage="/uptime",
        aliases=["up"],
    )
    def cmd_uptime(ctx: CommandContext) -> CommandResult:
        uptime_seconds = time.time() - SlashCommands._start_time
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        if days > 0:
            uptime_str = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            uptime_str = f"{hours}h {minutes}m {seconds}s"
        else:
            uptime_str = f"{minutes}m {seconds}s"
        
        return CommandResult.ok(
            output=f"[Uptime: {uptime_str}]",
            data={
                "uptime_seconds": uptime_seconds,
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
            },
        )
    
    @registry.command(
        "version",
        description="Get version information",
        usage="/version",
        aliases=["ver", "v"],
    )
    def cmd_version(ctx: CommandContext) -> CommandResult:
        python_version = sys.version.split()[0]
        
        return CommandResult.ok(
            output=f"[Python {python_version} | {platform.system()} {platform.release()}]",
            data={
                "python_version": python_version,
                "python_full": sys.version,
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "machine": platform.machine(),
            },
        )
    
    @registry.command(
        "env",
        description="Get environment variable",
        usage="/env [VAR_NAME]",
        aliases=["environ"],
    )
    def cmd_env(ctx: CommandContext) -> CommandResult:
        if ctx.first_arg:
            value = os.environ.get(ctx.first_arg.upper())
            if value:
                # Truncate long values
                display = value[:50] + "..." if len(value) > 50 else value
                return CommandResult.ok(
                    output=f"[{ctx.first_arg.upper()}={display}]",
                    data={"key": ctx.first_arg.upper(), "value": value},
                )
            return CommandResult.ok(
                output=f"[{ctx.first_arg.upper()}: not set]",
                data={"key": ctx.first_arg.upper(), "value": None},
            )
        
        # List common env vars
        common_vars = ["PATH", "HOME", "USER", "SHELL", "VIRTUAL_ENV", "PYTHONPATH"]
        found = {k: os.environ.get(k, "not set")[:30] for k in common_vars if k in os.environ}
        
        return CommandResult.ok(
            output=f"[Env vars: {len(os.environ)} total]",
            data={"count": len(os.environ), "sample": found},
        )
    
    @registry.command(
        "health",
        description="System health check",
        usage="/health",
        aliases=["ping", "status"],
    )
    def cmd_health(ctx: CommandContext) -> CommandResult:
        import psutil
        
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        
        # Health scoring
        health_score = 100
        issues = []
        
        if cpu > 90:
            health_score -= 30
            issues.append("high CPU")
        elif cpu > 70:
            health_score -= 10
        
        if mem > 90:
            health_score -= 30
            issues.append("high memory")
        elif mem > 80:
            health_score -= 10
        
        status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"
        
        return CommandResult.ok(
            output=f"[Health: {status} ({health_score}/100)]",
            data={
                "status": status,
                "score": health_score,
                "cpu_percent": cpu,
                "memory_percent": mem,
                "issues": issues,
            },
        )
    
    @registry.command(
        "cache",
        description="Cache statistics",
        usage="/cache",
        aliases=["caches"],
    )
    def cmd_cache(ctx: CommandContext) -> CommandResult:
        # Collect LRU cache stats
        cache_stats = {}
        
        # Check for common caches
        try:
            from src.observability.logging.EnhancedLogger import get_dedup_cache_info
            cache_stats["logger_dedup"] = get_dedup_cache_info()
        except ImportError:
            pass
        
        total_entries = sum(
            info.get("currsize", 0) if isinstance(info, dict) else 0 
            for info in cache_stats.values()
        )
        
        return CommandResult.ok(
            output=f"[Caches: {len(cache_stats)} active, {total_entries} entries]",
            data={
                "caches": cache_stats,
                "total_entries": total_entries,
            },
        )
    
    @registry.command(
        "help",
        description="Show help for commands",
        usage="/help [command]",
        aliases=["h", "?"],
    )
    def cmd_help(ctx: CommandContext) -> CommandResult:
        if ctx.first_arg:
            defn = registry.get(ctx.first_arg)
            if not defn:
                return CommandResult.ok(output=f"[Unknown command: {ctx.first_arg}]")
            
            aliases_str = f" (aliases: {', '.join('/' + a for a in defn.aliases)})" if defn.aliases else ""
            output = f"[/{defn.name}{aliases_str}: {defn.description}]"
            if defn.usage:
                output = f"[Usage: {defn.usage}]"
            
            return CommandResult.ok(
                output=output,
                data={
                    "name": defn.name,
                    "description": defn.description,
                    "usage": defn.usage,
                    "aliases": defn.aliases,
                },
            )
        
        # List all commands
        commands = registry.list_commands()
        cmd_names = sorted([f"/{c.name}" for c in commands])
        
        return CommandResult.ok(
            output=f"[Commands: {', '.join(cmd_names)}]",
            data={"commands": [c.name for c in commands]},
            inline=False,
        )
    
    @registry.command(
        "gpu",
        description="GPU information",
        usage="/gpu",
        aliases=["cuda", "nvidia"],
    )
    def cmd_gpu(ctx: CommandContext) -> CommandResult:
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                current_device = torch.cuda.current_device()
                gpu_name = torch.cuda.get_device_name(current_device)
                gpu_memory = torch.cuda.get_device_properties(current_device).total_memory
                gpu_memory_gb = gpu_memory / (1024**3)
                
                return CommandResult.ok(
                    output=f"[GPU: {gpu_name} ({gpu_memory_gb:.1f}GB) x{gpu_count}]",
                    data={
                        "available": True,
                        "count": gpu_count,
                        "name": gpu_name,
                        "memory_gb": gpu_memory_gb,
                    },
                )
        except ImportError:
            pass
        
        return CommandResult.ok(
            output="[GPU: Not available]",
            data={"available": False},
        )
    
    @registry.command(
        "python",
        description="Python interpreter info",
        usage="/python",
        aliases=["py"],
    )
    def cmd_python(ctx: CommandContext) -> CommandResult:
        return CommandResult.ok(
            output=f"[Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} at {sys.executable}]",
            data={
                "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "executable": sys.executable,
                "prefix": sys.prefix,
                "platform": sys.platform,
            },
        )
    
    @registry.command(
        "cwd",
        description="Current working directory",
        usage="/cwd",
        aliases=["pwd", "dir"],
    )
    def cmd_cwd(ctx: CommandContext) -> CommandResult:
        cwd = os.getcwd()
        return CommandResult.ok(
            output=f"[CWD: {cwd}]",
            data={"cwd": cwd},
        )
    
    @registry.command(
        "uuid",
        description="Generate a UUID",
        usage="/uuid",
        aliases=["id", "guid"],
    )
    def cmd_uuid(ctx: CommandContext) -> CommandResult:
        import uuid
        new_uuid = str(uuid.uuid4())
        return CommandResult.ok(
            output=f"[{new_uuid}]",
            data={"uuid": new_uuid},
        )
    
    @registry.command(
        "random",
        description="Generate random number",
        usage="/random [max]",
        aliases=["rand", "rnd"],
    )
    def cmd_random(ctx: CommandContext) -> CommandResult:
        import random
        
        max_val = 100
        if ctx.first_arg:
            try:
                max_val = int(ctx.first_arg)
            except ValueError:
                pass
        
        value = random.randint(1, max_val)
        return CommandResult.ok(
            output=f"[{value}]",
            data={"value": value, "max": max_val},
        )


# ============================================================================
# Convenience Functions
# ============================================================================

# Global instance
_default_slash_commands: SlashCommands | None = None


def get_slash_commands() -> SlashCommands:
    """Get the default SlashCommands instance."""
    global _default_slash_commands
    if _default_slash_commands is None:
        _default_slash_commands = SlashCommands()
    return _default_slash_commands


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


def execute_command(command: str, args: list[str] | None = None) -> CommandResult:
    """
    Execute a single slash command.
    
    Args:
        command: Command name (without /)
        args: Command arguments
        
    Returns:
        CommandResult
    """
    return get_slash_commands().execute(command, args)


def register_command(
    name: str,
    handler: CommandHandler,
    **kwargs: Any,
) -> None:
    """
    Register a custom command.
    
    Args:
        name: Command name
        handler: Handler function
        **kwargs: Additional command options
    """
    get_slash_commands().registry.register(name, handler, **kwargs)


def command(name: str, **kwargs: Any) -> Callable[[CommandHandler], CommandHandler]:
    """
    Decorator to register a custom command.
    
    Example:
        @command("greet", description="Greet the user")
        def cmd_greet(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok(f"[Hello, {ctx.first_arg or 'world'}!]")
    """
    return get_slash_commands().registry.command(name, **kwargs)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Classes
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
