# AccessibilityAgent

**File**: `src\logic\agents\development\AccessibilityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 95  
**Complexity**: 1 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `AccessibilityAgent`

**Inherits from**: BaseAgent, HtmlAccessibilityMixin, PythonAccessibilityMixin, JavascriptAccessibilityMixin, AccessibilityReportMixin, AccessibilityCoreMixin, AccessibilityLogicMixin

Analyzer for accessibility issues in UI code.

Detects accessibility problems and suggests improvements
for web and GUI applications.

Attributes:
    target_level: Target WCAG conformance level.
    issues: Detected issues.
    rules: Enabled accessibility rules.

Example:
    analyzer=AccessibilityAgent(file_path="...", target_level=WCAGLevel.AA)
    report=analyzer.analyze_file("component.py")
    for issue in report.issues:
        print(f"{issue.severity.name}: {issue.description}")

**Methods** (1):
- `__init__(self, target_level, file_path)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.core.base.types.AccessibilityIssue.AccessibilityIssue`
- `src.core.base.types.AccessibilityIssueType.AccessibilityIssueType`
- `src.core.base.types.WCAGLevel.WCAGLevel`
- `src.logic.agents.development.AccessibilityReportMixin.AccessibilityReportMixin`
- `src.logic.agents.development.HtmlAccessibilityMixin.HtmlAccessibilityMixin`
- `src.logic.agents.development.JavascriptAccessibilityMixin.JavascriptAccessibilityMixin`
- `src.logic.agents.development.PythonAccessibilityMixin.PythonAccessibilityMixin`
- `src.logic.agents.development.mixins.AccessibilityCoreMixin.AccessibilityCoreMixin`
- `src.logic.agents.development.mixins.AccessibilityLogicMixin.AccessibilityLogicMixin`

---
*Auto-generated documentation*
