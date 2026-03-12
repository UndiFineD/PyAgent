"""
LLM_CONTEXT_START

## Source: src-old/interface/commands/builtins/UtilityCommands.description.md

# UtilityCommands

**File**: `src\interface\commands\builtins\UtilityCommands.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 7 imports  
**Lines**: 97  
**Complexity**: 1 (simple)

## Overview

Utility commands for slash commands.

## Functions (1)

### `register_utility_commands(registry)`

Register utility-related built-in commands.

## Dependencies

**Imports** (7):
- `Base.CommandContext`
- `Base.CommandResult`
- `Registry.CommandRegistry`
- `__future__.annotations`
- `psutil`
- `src.observability.logging.EnhancedLogger.get_dedup_cache_info`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/interface/commands/builtins/UtilityCommands.improvements.md

# Improvements for UtilityCommands

**File**: `src\interface\commands\builtins\UtilityCommands.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 97 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `UtilityCommands_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations
from ..Registry import CommandRegistry

"""
Utility commands for slash commands.
"""


from typing import TYPE_CHECKING
from ..Base import CommandContext, CommandResult

def register_utility_commands(registry: CommandRegistry) -> None:
    """Register utility-related built-in commands."""

    @registry.command(
        "tokens",
        description="Count tokens in text",
        usage="/tokens <text>",
        aliases=["tok", "tokenize"],
        requires_args=True,
    )
    def cmd_tokens(ctx: CommandContext) -> CommandResult:
        text = ctx.arg_string
        words = len(text.split())
        chars = len(text)
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
        "cache",
        description="Cache statistics",
        usage="/cache",
        aliases=["caches"],
    )
    def cmd_cache(ctx: CommandContext) -> CommandResult:
        cache_stats = {}

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
