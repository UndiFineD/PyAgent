# Class Breakdown: tool_registry

**File**: `src\infrastructure\tools\registry\tool_registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolParserRegistry`

**Line**: 28  
**Methods**: 7

Registry for tool parsers.

Features:
- Parser registration by type
- Auto-detection of parser type
- Model name to parser mapping

[TIP] **Suggested split**: Move to `toolparserregistry.py`

---

### 2. `StreamingToolParser`

**Line**: 121  
**Methods**: 5

High-level streaming tool parser.

Features:
- Auto-detects parser type
- Maintains streaming state
- Yields tool calls as they complete

[TIP] **Suggested split**: Move to `streamingtoolparser.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
