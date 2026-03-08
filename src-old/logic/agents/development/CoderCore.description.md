# CoderCore

**File**: `src\logic\agents\development\CoderCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 155  
**Complexity**: 3 (simple)

## Overview

Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.

## Classes (1)

### `CoderCore`

**Inherits from**: LogicCore, CoderMetricsMixin, CoderStyleMixin, CoderSmellMixin, CoderDuplicationMixin, CoderQualityMixin, CoderDocMixin, CoderValidationMixin

Core logic for CoderAgent, target for Rust conversion.

**Methods** (3):
- `__init__(self, language, workspace_root)`
- `calculate_metrics(self, content)`
- `_calculate_cyclomatic_complexity(self, node)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `ast`
- `rust_core`
- `src.core.base.AgentCore.LogicCore`
- `src.core.base.Version.VERSION`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.StyleRule.StyleRule`
- `src.core.base.types.StyleRuleSeverity.StyleRuleSeverity`
- `src.core.rust_bridge.RustBridge`
- `src.logic.agents.development.mixins.CoderDocMixin.CoderDocMixin`
- `src.logic.agents.development.mixins.CoderDuplicationMixin.CoderDuplicationMixin`
- `src.logic.agents.development.mixins.CoderMetricsMixin.CoderMetricsMixin`
- `src.logic.agents.development.mixins.CoderQualityMixin.CoderQualityMixin`
- `src.logic.agents.development.mixins.CoderSmellMixin.CoderSmellMixin`
- ... and 2 more

---
*Auto-generated documentation*
