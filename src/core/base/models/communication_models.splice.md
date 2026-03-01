# Class Breakdown: communication_models

**File**: `src\core\base\models\communication_models.py`  
**Classes**: 15

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CascadeContext`

**Line**: 38  
**Methods**: 2

Context for recursive agent delegation (Phase 259/275).
Tracks depth and lineage to prevent infinite loops and provide tracing.

[TIP] **Suggested split**: Move to `cascadecontext.py`

---

### 2. `PromptTemplate`

**Line**: 66  
**Methods**: 1

reusable prompt template. 

[TIP] **Suggested split**: Move to `prompttemplate.py`

---

### 3. `ConversationMessage`

**Line**: 80  
**Methods**: 0

A message in conversation history.

[TIP] **Suggested split**: Move to `conversationmessage.py`

---

### 4. `ConversationHistory`

**Line**: 86  
**Methods**: 4

Manages a conversation history with message storage and retrieval.

[TIP] **Suggested split**: Move to `conversationhistory.py`

---

### 5. `PromptTemplateManager`

**Line**: 105  
**Methods**: 3

Manages a collection of prompt templates.

[TIP] **Suggested split**: Move to `prompttemplatemanager.py`

---

### 6. `ResponsePostProcessor`

**Line**: 118  
**Methods**: 3

Manages post-processing hooks for agent responses.

[TIP] **Suggested split**: Move to `responsepostprocessor.py`

---

### 7. `PromptVersion`

**Line**: 134  
**Methods**: 1

Versioned prompt for A/B testing.

[TIP] **Suggested split**: Move to `promptversion.py`

---

### 8. `BatchRequest`

**Line**: 174  
**Methods**: 4

Request in a batch processing queue.

[TIP] **Suggested split**: Move to `batchrequest.py`

---

### 9. `BatchResult`

**Line**: 205  
**Methods**: 0

Result of a batch processing request.

[TIP] **Suggested split**: Move to `batchresult.py`

---

### 10. `MultimodalInput`

**Line**: 214  
**Methods**: 0

Multimodal input for agents.

[TIP] **Suggested split**: Move to `multimodalinput.py`

---

### 11. `ContextWindow`

**Line**: 222  
**Methods**: 4

Manages token-based context window.

[TIP] **Suggested split**: Move to `contextwindow.py`

---

### 12. `MultimodalBuilder`

**Line**: 248  
**Methods**: 4

Builds multimodal input sets.

[TIP] **Suggested split**: Move to `multimodalbuilder.py`

---

### 13. `CachedResult`

**Line**: 265  
**Methods**: 0

A cached agent result.

[TIP] **Suggested split**: Move to `cachedresult.py`

---

### 14. `TelemetrySpan`

**Line**: 275  
**Methods**: 0

A telemetry span for tracing.

[TIP] **Suggested split**: Move to `telemetryspan.py`

---

### 15. `SpanContext`

**Line**: 286  
**Methods**: 3

Context for a telemetry span.

[TIP] **Suggested split**: Move to `spancontext.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
