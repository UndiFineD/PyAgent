# Splice: src/interface/slash_commands/core.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CommandContext
- CommandResult
- CommandDefinition
- CommandRegistry
- ParsedCommand
- ProcessedPrompt
- SlashCommands

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
