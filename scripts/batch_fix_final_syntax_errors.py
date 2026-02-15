#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# distributed under the License is distributed on an "AS IS" BASIS,
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Batch fixer for final syntax errors:
- Fix unterminated string literals (add missing quote or comment out line)
- Comment out lines that are clearly metadata or non-Python (e.g., [Brief Summary])
- Fix unmatched parentheses on lines that are not valid Python
- Insert 'pass' after class definitions with no body (IndentationError)
"""
import os
import re

TARGET_DIRS = [
    'src/logic/agents/security',
    'src/observability/errors',
]

STRING_LITERAL_RE = re.compile(r'(["\"]).*[^"\
]$')
METADATA_RE = re.compile(r'\[.*?\]|^\s*summary:|^\s*DATE:|^\s*detail:|^\s*main\(\)|^\s*AUTHOR:|^\s*Brief Summary|^\s*Ported logic from|^\s*USAGE:|^\s*Ported from')
CLOSE_PAREN_RE = re.compile(r'^\s*\)\s*$')
TRY_RE = re.compile(r'^\s*try:\s*$')
            while i < len(lines):
                line = lines[i]
                # Fix unterminated string literals
                if (line.count('"') % 2 == 1 or line.count("'") % 2 == 1) and not line.strip().endswith(('"', "'")):
                    # Try to close the string, or comment out if ambiguous
                    if line.strip().startswith(('"', "'")):
                        new_lines.append('# [BATCHFIX] Commented unterminated string\n# ' + line)
                    else:
                        new_lines.append(line.rstrip() + '"  # [BATCHFIX] closed string\n')
                    i += 1
                    continue
                # Comment out metadata/non-Python lines
                if METADATA_RE.search(line):
                    new_lines.append('# [BATCHFIX] Commented metadata/non-Python\n# ' + line)
                    i += 1
                    continue
                # Fix unmatched parenthesis or lines starting with a number and unmatched parenthesis
                if (UNMATCHED_PAREN_RE.match(line) or NUM_UNMATCHED_PAREN_RE.match(line)) and not line.strip().startswith('#'):
                    new_lines.append('# [BATCHFIX] Commented unmatched parenthesis/numbered line\n# ' + line)
                    i += 1
                    continue
                # Comment out unmatched closing parenthesis on its own line
                if CLOSE_PAREN_RE.match(line):
                    new_lines.append('# [BATCHFIX] Commented unmatched closing parenthesis\n# ' + line)
                    i += 1
                    continue
                # Insert pass after class or def if next line is not indented
                if CLASS_DEF_RE.match(line) or DEF_RE.match(line):
                    new_lines.append(line)
                    if i+1 >= len(lines) or (lines[i+1].strip() == '' or not lines[i+1].startswith((' ', '\t'))):
                        new_lines.append('    pass  # [BATCHFIX] inserted for empty block\n')
                    i += 1
                    continue
                # Insert pass after try: if next line is not indented
                if TRY_RE.match(line):
                    new_lines.append(line)
                    if i+1 >= len(lines) or (lines[i+1].strip() == '' or not lines[i+1].startswith((' ', '\t'))):
                        new_lines.append('    pass  # [BATCHFIX] inserted for empty try block\n')
                    i += 1
                    continue
                new_lines.append(line)
                i += 1


for target_dir in TARGET_DIRS:
    for root, _, files in os.walk(target_dir):
        for fname in files:
            if not fname.endswith('.py'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Fix unterminated string literals
                if (line.count('"') % 2 == 1 or line.count("'") % 2 == 1) and not line.strip().endswith(('"', "'")):
                    # Try to close the string, or comment out if ambiguous
                    if line.strip().startswith(('"', "'")):
                        new_lines.append('# [BATCHFIX] Commented unterminated string\n# ' + line)
                    else:
                        new_lines.append(line.rstrip() + '"  # [BATCHFIX] closed string\n')
                    i += 1
                    continue
                # Comment out metadata/non-Python lines
                if METADATA_RE.search(line):
                    new_lines.append('# [BATCHFIX] Commented metadata/non-Python\n# ' + line)
                    i += 1
                    continue
                # Fix unmatched parenthesis or lines starting with a number and unmatched parenthesis
                if (UNMATCHED_PAREN_RE.match(line) or NUM_UNMATCHED_PAREN_RE.match(line)) and not line.strip().startswith('#'):
                    new_lines.append('# [BATCHFIX] Commented unmatched parenthesis/numbered line\n# ' + line)
                    i += 1
                    continue
                # Comment out unmatched closing parenthesis on its own line
                if CLOSE_PAREN_RE.match(line):
                    new_lines.append('# [BATCHFIX] Commented unmatched closing parenthesis\n# ' + line)
                    i += 1
                    continue
                # Insert pass after class or def if next line is not indented
                if CLASS_DEF_RE.match(line) or DEF_RE.match(line):
                    new_lines.append(line)
                    if i+1 >= len(lines) or (lines[i+1].strip() == '' or not lines[i+1].startswith((' ', '\t'))):
                        new_lines.append('    pass  # [BATCHFIX] inserted for empty block\n')
                    i += 1
                    continue
                # Insert pass after try: if next line is not indented
                if TRY_RE.match(line):
                    new_lines.append(line)
                    if i+1 >= len(lines) or (lines[i+1].strip() == '' or not lines[i+1].startswith((' ', '\t'))):
                        new_lines.append('    pass  # [BATCHFIX] inserted for empty try block\n')
                    i += 1
                    continue
                new_lines.append(line)
                i += 1
            with open(fpath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
print('Batch fix complete.')
