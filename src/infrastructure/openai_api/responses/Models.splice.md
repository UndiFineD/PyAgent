# Class Breakdown: Models

**File**: `src\infrastructure\openai_api\responses\Models.py`  
**Classes**: 12

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ContentPart`

**Line**: 11  
**Inherits**: ABC  
**Methods**: 0

Base class for content parts.

[TIP] **Suggested split**: Move to `contentpart.py`

---

### 2. `TextContent`

**Line**: 16  
**Inherits**: ContentPart  
**Methods**: 1

Text content part.

[TIP] **Suggested split**: Move to `textcontent.py`

---

### 3. `ImageContent`

**Line**: 24  
**Inherits**: ContentPart  
**Methods**: 1

Image content part.

[TIP] **Suggested split**: Move to `imagecontent.py`

---

### 4. `AudioContent`

**Line**: 39  
**Inherits**: ContentPart  
**Methods**: 1

Audio content part.

[TIP] **Suggested split**: Move to `audiocontent.py`

---

### 5. `RefusalContent`

**Line**: 48  
**Inherits**: ContentPart  
**Methods**: 1

Refusal content part.

[TIP] **Suggested split**: Move to `refusalcontent.py`

---

### 6. `ToolCallContent`

**Line**: 56  
**Inherits**: ContentPart  
**Methods**: 1

Tool call content part.

[TIP] **Suggested split**: Move to `toolcallcontent.py`

---

### 7. `Message`

**Line**: 70  
**Methods**: 2

Chat message.

[TIP] **Suggested split**: Move to `message.py`

---

### 8. `ToolDefinition`

**Line**: 121  
**Methods**: 1

Tool definition for function calling.

[TIP] **Suggested split**: Move to `tooldefinition.py`

---

### 9. `ResponseConfig`

**Line**: 137  
**Methods**: 1

Response configuration.

[TIP] **Suggested split**: Move to `responseconfig.py`

---

### 10. `ResponseUsage`

**Line**: 178  
**Methods**: 1

Token usage statistics.

[TIP] **Suggested split**: Move to `responseusage.py`

---

### 11. `ResponseOutput`

**Line**: 195  
**Methods**: 2

Single response output.

[TIP] **Suggested split**: Move to `responseoutput.py`

---

### 12. `Response`

**Line**: 212  
**Methods**: 4

Complete response object.

[TIP] **Suggested split**: Move to `response.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
