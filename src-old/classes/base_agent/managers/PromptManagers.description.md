# PromptManagers

**File**: `src\classes\base_agent\managers\PromptManagers.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 9 imports  
**Lines**: 222  
**Complexity**: 15 (moderate)

## Overview

Python module containing implementation for PromptManagers.

## Classes (3)

### `PromptTemplateManager`

Manages a collection of prompt templates.

**Methods** (3):
- `__init__(self)`
- `register(self, template)`
- `render(self, template_name)`

### `PromptVersion`

Versioned prompt for A/B testing.

**Methods** (1):
- `__init__(self, version, content, description, active, version_id, template_id, variant, prompt_text, weight)`

### `PromptVersionManager`

Manager for prompt versioning and A/B testing.

**Methods** (11):
- `__init__(self)`
- `register_version(self, version)`
- `add_version(self, version)`
- `set_active(self, version)`
- `get_active(self)`
- `get_versions(self, template_id)`
- `select_version(self, template_id)`
- `record_metric(self, version_id, metric_name, value)`
- `get_best_version(self, template_id, metric)`
- `generate_report(self, template_id)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `random`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.core.base.models.PromptTemplate`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
