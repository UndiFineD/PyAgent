#!/usr/bin/env python3
"""Find files with duplicate headers or __future__ import issues."""

import re
from pathlib import Path

problem_files = []
for py_file in Path('src').rglob('*.py'):
    try:
        content = py_file.read_text(encoding='utf-8')
        # Check for multiple copyright headers
        copyright_count = len(re.findall(r'# Copyright', content))
        if copyright_count > 1:
            problem_files.append((str(py_file), 'duplicate_headers'))
        # Check for __future__ import not at start
        lines = content.split('\n')
        future_line = -1
        for i, line in enumerate(lines):
            if 'from __future__' in line:
                future_line = i
                break
        if future_line > 0:
            # Check if there's a docstring before it
            for j in range(future_line):
                if '"""' in lines[j] or "'''" in lines[j]:
                    problem_files.append((str(py_file), '__future___after_docstring'))
                    break
    except:
        pass

print(f'Found {len(problem_files)} files with issues:')
for path, issue in problem_files[:30]:
    print(f'  {path}: {issue}')
if len(problem_files) > 30:
    print(f'  ... and {len(problem_files)-30} more')
