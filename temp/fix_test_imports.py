
import re

file_path = r'c:\DEV\PyAgent\tests\unit\logic\test_coder_CORE_UNIT.py'

imports_to_add = """
from src.core.base.types.AccessibilityIssue import AccessibilityIssue
from src.core.base.types.AccessibilityIssueType import AccessibilityIssueType
from src.core.base.types.AccessibilityReport import AccessibilityReport
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.ARIAAttribute import ARIAAttribute
from src.core.base.types.ColorContrastResult import ColorContrastResult
from src.core.base.types.WCAGLevel import WCAGLevel
from src.logic.agents.development.AccessibilityAgent import AccessibilityAgent
"""

replacements = {
    r'mod\.AccessibilityIssueType': 'AccessibilityIssueType',
    r'mod\.AccessibilitySeverity': 'AccessibilitySeverity',
    r'mod\.WCAGLevel': 'WCAGLevel',
    r'mod\.AccessibilityIssue': 'AccessibilityIssue',
    r'mod\.ColorContrastResult': 'ColorContrastResult',
    r'mod\.AccessibilityReport': 'AccessibilityReport',
    r'mod\.ARIAAttribute': 'ARIAAttribute',
    r'mod\.AccessibilityAnalyzer': 'AccessibilityAgent',
}

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports after "from __future__ import annotations" or at the top
if "from __future__ import annotations" in content:
    content = content.replace("from __future__ import annotations", "from __future__ import annotations" + imports_to_add)
else:
    content = imports_to_add + content

# Apply replacements
for pattern, replacement in replacements.items():
    content = re.sub(pattern, replacement, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path}")
