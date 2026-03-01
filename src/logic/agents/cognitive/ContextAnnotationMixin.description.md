# ContextAnnotationMixin

**File**: `src\logic\agents\cognitive\ContextAnnotationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 53  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ContextAnnotationMixin.

## Classes (1)

### `ContextAnnotationMixin`

Annotation methods for ContextAgent.

**Methods** (5):
- `add_annotation(self, line_number, content, author)`
- `get_annotations(self)`
- `get_annotations_for_line(self, line_number)`
- `resolve_annotation(self, annotation_id)`
- `remove_annotation(self, annotation_id)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `datetime.datetime`
- `hashlib`
- `src.logic.agents.cognitive.context.models.ContextAnnotation.ContextAnnotation`

---
*Auto-generated documentation*
