import os
import re
import ast

def fix_file(file_path):
    """Fix a single file by removing erroneous content and ensuring proper structure."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Remove the erroneous docstring
    content = re.sub(r'"""Auto-extracted class from generate_agent_reports\.py"""', '', content)

    # Split into lines
    lines = content.split('\n')

    # Find the first class or function definition
    first_class_line = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(('class ', 'def ', '@dataclass')):
            first_class_line = i
            break

    if first_class_line == -1:
        # No class found, this file is broken
        print(f"ERROR: No class found in {file_path}")
        return

    # Keep only content up to and including the first class/function
    # But we need to find where the class ends
    class_indent = None
    class_end_line = len(lines)

    for i in range(first_class_line, len(lines)):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith(('class ', '@dataclass')):
            if class_indent is None:
                class_indent = len(line) - len(line.lstrip())
        elif class_indent is not None:
            if line.strip() and len(line) - len(line.lstrip()) <= class_indent:
                # End of class
                class_end_line = i
                break

    # Keep content from start to class_end_line
    fixed_content = '\n'.join(lines[:class_end_line])

    # Ensure the file has proper structure
    # Check if it ends with a complete class
    try:
        ast.parse(fixed_content)
        with open(file_path, 'w') as f:
            f.write(fixed_content)
        print(f"Fixed {file_path}")
    except SyntaxError as e:
        print(f"Still broken {file_path}: {e}")
        # Try a more aggressive fix - just keep the basic structure
        header = '''#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Basic module docstring.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION
'''
        with open(file_path, 'w') as f:
            f.write(header)

# List of files to fix
files_to_fix = [
    'src/observability/reports/export_format.py',
    'src/observability/reports/compile_result.py',
    'src/observability/reports/audit_entry.py',
    'src/observability/reports/audit_action.py',
    'src/observability/reports/annotation_manager.py',
    'src/observability/reports/aggregated_report.py',
    'src/observability/reports/access_controller.py',
    'src/observability/reports/validation_result.py',
    'src/observability/reports/subscription_manager.py',
    'src/observability/reports/subscription_frequency.py',
    'src/observability/reports/report_subscription.py',
    'src/observability/reports/report_search_result.py',
    'src/observability/reports/report_search_engine.py',
    'src/observability/reports/archived_report.py',
    'src/observability/reports/report_permission.py',
    'src/observability/reports/report_metric.py',
    'src/observability/reports/report_localizer.py'
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        fix_file(file_path)

print('All files processed')