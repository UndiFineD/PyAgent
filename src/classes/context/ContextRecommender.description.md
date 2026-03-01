# ContextRecommender

**File**: `src\classes\context\ContextRecommender.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 90  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextRecommender`

Recommends context improvements based on similar files.

Analyzes similar files to suggest context improvements.

Example:
    >>> recommender=ContextRecommender()
    >>> recommendations=recommender.recommend("auth.py", similar_contexts)

**Methods** (4):
- `__init__(self)`
- `add_reference(self, file_name, content)`
- `find_similar(self, query)`
- `recommend(self, content_or_target_file, similar_contexts)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.ContextRecommendation.ContextRecommendation`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
