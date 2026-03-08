# LocalizationCore

**File**: `src\logic\agents\intelligence\core\LocalizationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 53  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LocalizationCore.

## Classes (1)

### `LocalizationCore`

LocalizationCore handles translation logic (placeholder) and Cultural Guardrails.
It identifies problematic idioms or metaphors in multi-agent communication.

**Methods** (4):
- `__init__(self)`
- `detect_cultural_issues(self, text)`
- `get_supported_locales(self)`
- `format_translation_request(self, text, target_lang)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
