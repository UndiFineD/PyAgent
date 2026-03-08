# data_parsing_mixin

**File**: `src\core\base\mixins\data_parsing_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 46  
**Complexity**: 4 (simple)

## Overview

Module: data_parsing_mixin
Data parsing mixin for BaseAgent, implementing XML and HTML parsing patterns.
Inspired by ADSyncDump-BOF XML parsing techniques.

## Classes (1)

### `DataParsingMixin`

Mixin providing data parsing features for structured data.

**Methods** (4):
- `__init__(self)`
- `html_unescape(self, text)`
- `extract_xml_value(self, xml, tag_pattern)`
- `find_pattern(self, haystack, needle)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `html`
- `re`
- `src.core.base.logic.processing.data_parsing_core.DataParsingCore`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
