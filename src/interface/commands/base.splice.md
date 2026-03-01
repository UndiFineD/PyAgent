# Class Breakdown: base

**File**: `src\interface\commands\base.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CommandContext`

**Line**: 29  
**Methods**: 2

Context passed to command handlers.

[TIP] **Suggested split**: Move to `commandcontext.py`

---

### 2. `CommandResult`

**Line**: 65  
**Methods**: 2

Result from a command execution.

[TIP] **Suggested split**: Move to `commandresult.py`

---

### 3. `CommandDefinition`

**Line**: 95  
**Methods**: 0

Definition of a slash command.

[TIP] **Suggested split**: Move to `commanddefinition.py`

---

### 4. `ParsedCommand`

**Line**: 121  
**Methods**: 0

A parsed command from the prompt.

[TIP] **Suggested split**: Move to `parsedcommand.py`

---

### 5. `ProcessedPrompt`

**Line**: 141  
**Methods**: 4

Result of processing a prompt.

[TIP] **Suggested split**: Move to `processedprompt.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
