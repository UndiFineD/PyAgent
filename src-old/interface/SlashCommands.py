"""
LLM_CONTEXT_START

## Source: src-old/interface/SlashCommands.description.md

# SlashCommands

**File**: `src\interface\SlashCommands.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 14 imports  
**Lines**: 42  
**Complexity**: 0 (simple)

## Overview

SlashCommands - Chat prompt slash command parser and executor.

Provides backward compatibility for the moved SlashCommands implementation.
Moved to src/interface/commands/

## Dependencies

**Imports** (14):
- `commands.CommandContext`
- `commands.CommandDefinition`
- `commands.CommandParser`
- `commands.CommandRegistry`
- `commands.CommandResult`
- `commands.ParsedCommand`
- `commands.ProcessedPrompt`
- `commands.SlashCommands`
- `commands.command`
- `commands.execute_command`
- `commands.get_slash_commands`
- `commands.parse_commands`
- `commands.process_prompt`
- `commands.register_command`

---
*Auto-generated documentation*
## Source: src-old/interface/SlashCommands.improvements.md

# Improvements for SlashCommands

**File**: `src\interface\SlashCommands.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 42 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SlashCommands_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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
