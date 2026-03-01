# Class Breakdown: Streaming

**File**: `src\infrastructure\openai_api\responses\Streaming.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SSEEvent`

**Line**: 11  
**Methods**: 1

Server-Sent Event.

[TIP] **Suggested split**: Move to `sseevent.py`

---

### 2. `SSEStream`

**Line**: 28  
**Methods**: 1

SSE streaming handler.

[TIP] **Suggested split**: Move to `ssestream.py`

---

### 3. `StreamingHandler`

**Line**: 48  
**Methods**: 1

Handles streaming response generation.

[TIP] **Suggested split**: Move to `streaminghandler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
