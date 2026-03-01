# Class Breakdown: data_classes

**File**: `src\infrastructure\engine\reasoning\data_classes.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReasoningToken`

**Line**: 28  
**Methods**: 0

A single token with reasoning metadata.

[TIP] **Suggested split**: Move to `reasoningtoken.py`

---

### 2. `ThinkingBlock`

**Line**: 40  
**Methods**: 2

A complete thinking/reasoning block.

[TIP] **Suggested split**: Move to `thinkingblock.py`

---

### 3. `ToolCall`

**Line**: 61  
**Methods**: 1

A parsed tool/function call.

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 4. `ToolCallResult`

**Line**: 82  
**Methods**: 0

Result from tool execution.

[TIP] **Suggested split**: Move to `toolcallresult.py`

---

### 5. `ParseResult`

**Line**: 92  
**Methods**: 3

Result of parsing a generation stream.

[TIP] **Suggested split**: Move to `parseresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
