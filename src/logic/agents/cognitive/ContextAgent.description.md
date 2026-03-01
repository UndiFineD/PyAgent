# ContextAgent

**File**: `src\logic\agents\cognitive\ContextAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 169  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextAgent`

**Inherits from**: BaseAgent, ContextTemplateMixin, ContextTaggingMixin, ContextVersioningMixin, ContextValidationMixin, ContextAnnotationMixin, ContextCategorizationMixin, ContextRAGMixin

Updates code file context descriptions using AI assistance.

**Methods** (7):
- `__init__(self, file_path)`
- `route_query(self, query)`
- `_validate_file_extension(self)`
- `_derive_source_path(self)`
- `_get_default_content(self)`
- `_get_fallback_response(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.ContextAnnotationMixin.ContextAnnotationMixin`
- `src.logic.agents.cognitive.ContextCategorizationMixin.ContextCategorizationMixin`
- `src.logic.agents.cognitive.ContextRAGMixin.ContextRAGMixin`
- `src.logic.agents.cognitive.ContextTaggingMixin.ContextTaggingMixin`
- `src.logic.agents.cognitive.ContextTemplateMixin.ContextTemplateMixin`
- `src.logic.agents.cognitive.ContextTemplateMixin.DEFAULT_TEMPLATES`
- `src.logic.agents.cognitive.ContextValidationMixin.ContextValidationMixin`
- `src.logic.agents.cognitive.ContextValidationMixin.DEFAULT_VALIDATION_RULES`
- `src.logic.agents.cognitive.ContextVersioningMixin.ContextVersioningMixin`
- `src.logic.agents.cognitive.context.models.ContextPriority.ContextPriority`
- ... and 3 more

---
*Auto-generated documentation*
