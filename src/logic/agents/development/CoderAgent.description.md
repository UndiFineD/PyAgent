# CoderAgent

**File**: `src\logic\agents\development\CoderAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 145  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `CoderAgent`

**Inherits from**: BaseAgent, AgentLanguageMixin, AgentStyleMixin, AgentMetricsMixin, AgentRefactorMixin

Updates code files using AI assistance.

Invariants:
- self.file_path must point to a valid file path.

- Supports Python files (.py) with syntax validation.
- Supports multi - language code improvements.

**Methods** (6):
- `__init__(self, file_path)`
- `_detect_language(self)`
- `detect_language(self)`
- `generate_documentation(self, content)`
- `_get_default_content(self)`
- `_get_fallback_response(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.CodeSmell.CodeSmell`
- `src.core.base.types.QualityScore.QualityScore`
- `src.core.base.types.RefactoringPattern.RefactoringPattern`
- `src.core.base.types.StyleRule.StyleRule`
- `src.logic.agents.development.CoderCore.CoderCore`
- `src.logic.agents.development.CoderCore.DEFAULT_PYTHON_STYLE_RULES`
- `src.logic.agents.development.mixins.agent.AgentLanguageMixin.AgentLanguageMixin`
- `src.logic.agents.development.mixins.agent.AgentMetricsMixin.AgentMetricsMixin`
- ... and 2 more

---
*Auto-generated documentation*
