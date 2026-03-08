# ChangesEntryMixin

**File**: `src\logic\agents\swarm\mixins\ChangesEntryMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 146  
**Complexity**: 6 (moderate)

## Overview

Entry management logic for ChangesAgent.

## Classes (1)

### `ChangesEntryMixin`

Mixin for managing changelog entries.

**Methods** (6):
- `add_validation_rule(self, rule)`
- `add_entry(self, category, description, priority, severity, tags, linked_issues)`
- `get_entries_by_category(self, category)`
- `get_entries_by_priority(self, min_priority)`
- `deduplicate_entries(self)`
- `format_entries_as_markdown(self)`

## Dependencies

**Imports** (7):
- `ChangelogEntry.ChangelogEntry`
- `ValidationRule.ValidationRule`
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
