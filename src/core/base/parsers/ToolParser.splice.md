# Class Breakdown: ToolParser

**File**: `src\core\base\parsers\ToolParser.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolCall`

**Line**: 25  
**Methods**: 1

Represents a single tool/function call.

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 2. `ExtractedToolCalls`

**Line**: 43  
**Methods**: 1

Result of tool call extraction.

[TIP] **Suggested split**: Move to `extractedtoolcalls.py`

---

### 3. `StreamingToolCallDelta`

**Line**: 57  
**Methods**: 0

Delta update for streaming tool call extraction.

[TIP] **Suggested split**: Move to `streamingtoolcalldelta.py`

---

### 4. `ToolParser`

**Line**: 65  
**Inherits**: ABC  
**Methods**: 5

Abstract base class for tool call parsers.

Implementations should handle extracting tool calls from
model outputs in both complete and streaming modes.

[TIP] **Suggested split**: Move to `toolparser.py`

---

### 5. `JSONToolParser`

**Line**: 145  
**Inherits**: ToolParser  
**Methods**: 3

Parser for JSON-formatted tool calls.

Handles outputs like:
[{"name": "function_name", "arguments": {"arg1": "value1"}}]

[TIP] **Suggested split**: Move to `jsontoolparser.py`

---

### 6. `XMLToolParser`

**Line**: 280  
**Inherits**: ToolParser  
**Methods**: 2

Parser for XML-formatted tool calls.

Handles outputs like:
<tool_call>
    <name>function_name</name>
    <arguments>{"arg1": "value1"}</arguments>
</tool_call>

[TIP] **Suggested split**: Move to `xmltoolparser.py`

---

### 7. `ToolParserManager`

**Line**: 372  
**Methods**: 5

Central registry for ToolParser implementations.

Supports both eager and lazy registration.

[TIP] **Suggested split**: Move to `toolparsermanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
