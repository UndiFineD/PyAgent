# Class Breakdown: tool_parser

**File**: `src\core\base\logic\parsers\tool_parser.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolCall`

**Line**: 39  
**Methods**: 1

Represents a single tool/function call.

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 2. `ExtractedToolCalls`

**Line**: 58  
**Methods**: 1

Result of tool call extraction.

[TIP] **Suggested split**: Move to `extractedtoolcalls.py`

---

### 3. `StreamingToolCallDelta`

**Line**: 73  
**Methods**: 0

Delta update regarding streaming tool call extraction.

[TIP] **Suggested split**: Move to `streamingtoolcalldelta.py`

---

### 4. `ToolParser`

**Line**: 82  
**Inherits**: ABC  
**Methods**: 5

Abstract base class regarding tool call parsers.

Implementations should handle extracting tool calls from
model outputs in both complete and streaming modes.

[TIP] **Suggested split**: Move to `toolparser.py`

---

### 5. `JSONToolParser`

**Line**: 144  
**Inherits**: ToolParser  
**Methods**: 3

Parser regarding JSON-formatted tool calls.

Handles outputs like:
[{"name": "function_name", "arguments": {"arg1": "value1"}}]

[TIP] **Suggested split**: Move to `jsontoolparser.py`

---

### 6. `XMLToolParser`

**Line**: 286  
**Inherits**: ToolParser  
**Methods**: 2

Parser regarding XML-formatted tool calls.

Handles outputs like:
<tool_call>
    <name>function_name</name>
    <arguments>{"arg1": "value1"}</arguments>
</tool_call>

[TIP] **Suggested split**: Move to `xmltoolparser.py`

---

### 7. `ToolParserManager`

**Line**: 377  
**Methods**: 5

Central registry regarding ToolParser implementations.

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
