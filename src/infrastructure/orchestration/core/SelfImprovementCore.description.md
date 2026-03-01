# SelfImprovementCore

**File**: `src\infrastructure\orchestration\core\SelfImprovementCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 131  
**Complexity**: 4 (simple)

## Overview

SelfImprovementCore: Pure logic for fleet self-improvement analysis.
Extracted from SelfImprovementOrchestrator for Rust-readiness.

## Classes (1)

### `SelfImprovementCore`

**Inherits from**: SelfImprovementSecurityMixin, SelfImprovementQualityMixin

Pure logic core for identifying tech debt, security risks, and quality issues.
This class contains no I/O and is suitable for Rust oxidation.

**Methods** (4):
- `__init__(self, workspace_root)`
- `analyze_content(self, content, file_path_rel)`
- `_analyze_via_rust(self, content, file_path_rel)`
- `generate_simple_fix(self, issue_type, content)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `mixins.SelfImprovementQualityMixin.SelfImprovementQualityMixin`
- `mixins.SelfImprovementSecurityMixin.SelfImprovementSecurityMixin`
- `re`
- `rust_core`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
