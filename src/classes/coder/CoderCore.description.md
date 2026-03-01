# CoderCore

**File**: `src\classes\coder\CoderCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 341  
**Complexity**: 8 (moderate)

## Overview

Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.

## Classes (1)

### `CoderCore`

**Inherits from**: LogicCore

Core logic for CoderAgent, target for Rust conversion.

**Methods** (8):
- `__init__(self, language)`
- `calculate_metrics(self, content)`
- `_analyze_python_ast(self, tree, metrics)`
- `check_style(self, content, rules)`
- `auto_fix_style(self, content, rules)`
- `detect_code_smells(self, content)`
- `find_duplicate_code(self, content, min_lines)`
- `calculate_quality_score(self, metrics, violations, smells, coverage)`

## Dependencies

**Imports** (16):
- `CodeLanguage.CodeLanguage`
- `CodeMetrics.CodeMetrics`
- `CodeSmell.CodeSmell`
- `QualityScore.QualityScore`
- `StyleRule.StyleRule`
- `StyleRuleSeverity.StyleRuleSeverity`
- `ast`
- `hashlib`
- `math`
- `re`
- `src.classes.base_agent.core.LogicCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
