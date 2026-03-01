# Class Breakdown: models

**File**: `src\infrastructure\services\openai_api\responses\models.py`  
**Classes**: 13

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ContentPart`

**Line**: 33  
**Inherits**: ABC  
**Methods**: 0

Base class regarding content parts.

[TIP] **Suggested split**: Move to `contentpart.py`

---

### 2. `TextContent`

**Line**: 40  
**Inherits**: ContentPart  
**Methods**: 1

Text content part.

[TIP] **Suggested split**: Move to `textcontent.py`

---

### 3. `ImageContent`

**Line**: 51  
**Inherits**: ContentPart  
**Methods**: 1

Image content part.

[TIP] **Suggested split**: Move to `imagecontent.py`

---

### 4. `AudioContent`

**Line**: 69  
**Inherits**: ContentPart  
**Methods**: 1

Audio content part.

[TIP] **Suggested split**: Move to `audiocontent.py`

---

### 5. `RefusalContent`

**Line**: 81  
**Inherits**: ContentPart  
**Methods**: 1

Refusal content part.

[TIP] **Suggested split**: Move to `refusalcontent.py`

---

### 6. `ToolCallContent`

**Line**: 92  
**Inherits**: ContentPart  
**Methods**: 1

Tool call content part.

[TIP] **Suggested split**: Move to `toolcallcontent.py`

---

### 7. `Message`

**Line**: 109  
**Methods**: 2

Chat message.

[TIP] **Suggested split**: Move to `message.py`

---

### 8. `ToolDefinition`

**Line**: 184  
**Methods**: 1

Tool definition regarding function calling.

[TIP] **Suggested split**: Move to `tooldefinition.py`

---

### 9. `ResponseConfig`

**Line**: 208  
**Methods**: 1

Response configuration.

[TIP] **Suggested split**: Move to `responseconfig.py`

---

### 10. `ResponseUsage`

**Line**: 273  
**Methods**: 1

Token usage statistics.

[TIP] **Suggested split**: Move to `responseusage.py`

---

### 11. `ResponseOutput`

**Line**: 293  
**Methods**: 2

Single response output.

[TIP] **Suggested split**: Move to `responseoutput.py`

---

### 12. `ResponseContent`

**Line**: 322  
**Methods**: 0

Response content regarding generation.

[TIP] **Suggested split**: Move to `responsecontent.py`

---

### 13. `Response`

**Line**: 329  
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
