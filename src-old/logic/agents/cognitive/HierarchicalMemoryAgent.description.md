# HierarchicalMemoryAgent

**File**: `src\logic\agents\cognitive\HierarchicalMemoryAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 62  
**Complexity**: 1 (simple)

## Overview

Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.

## Classes (1)

### `HierarchicalMemoryAgent`

**Inherits from**: BaseAgent, MemoryStorageMixin, MemoryQueryMixin

Manages memory across multiple temporal and semantic resolutions.
Phase 290: Integrated with 3-layer system (ShortTerm, Working, LongTerm).

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `mixins.MemoryQueryMixin.MemoryQueryMixin`
- `mixins.MemoryStorageMixin.MemoryStorageMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.create_main_function`
- `src.core.base.Version.VERSION`

---
*Auto-generated documentation*
