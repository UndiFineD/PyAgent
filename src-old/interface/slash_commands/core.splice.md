# Class Breakdown: core

**File**: `src\interface\slash_commands\core.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CommandContext`

**Line**: 35  
**Methods**: 3

Context passed to command handlers.

[TIP] **Suggested split**: Move to `commandcontext.py`

---

### 2. `CommandResult`

**Line**: 76  
**Methods**: 2

Result from a command execution.

[TIP] **Suggested split**: Move to `commandresult.py`

---

### 3. `CommandDefinition`

**Line**: 106  
**Methods**: 0

Definition of a slash command.

[TIP] **Suggested split**: Move to `commanddefinition.py`

---

### 4. `CommandRegistry`

**Line**: 142  
**Methods**: 12

Registry for slash commands.

[TIP] **Suggested split**: Move to `commandregistry.py`

---

### 5. `ParsedCommand`

**Line**: 298  
**Methods**: 0

A parsed command from the prompt.

[TIP] **Suggested split**: Move to `parsedcommand.py`

---

### 6. `ProcessedPrompt`

**Line**: 353  
**Methods**: 4

Result of processing a prompt.

[TIP] **Suggested split**: Move to `processedprompt.py`

---

### 7. `SlashCommands`

**Line**: 389  
**Methods**: 5

Slash command parser and executor for chat prompts.

Example:
    >>> slash = SlashCommands()
    >>> result = slash.process("What is /datetime the current time?")
    >>> print(result.processed_promp...

[TIP] **Suggested split**: Move to `slashcommands.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
