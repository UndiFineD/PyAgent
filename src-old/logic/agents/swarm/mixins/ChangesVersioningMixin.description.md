# ChangesVersioningMixin

**File**: `src\logic\agents\swarm\mixins\ChangesVersioningMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 68  
**Complexity**: 3 (simple)

## Overview

Versioning logic for ChangesAgent.

## Classes (1)

### `ChangesVersioningMixin`

Mixin for managing versioning strategies.

**Methods** (3):
- `set_versioning_strategy(self, strategy)`
- `generate_next_version(self, bump_type)`
- `_extract_latest_version(self)`

## Dependencies

**Imports** (5):
- `VersioningStrategy.VersioningStrategy`
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `re`

---
*Auto-generated documentation*
