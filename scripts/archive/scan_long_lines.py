#!/usr/bin/env python3
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
Scan Long Lines module.
"""

import os

def find_long_lines(root_dir, max_len=120):
    ignore_dirs = {'.venv', '.git', '__pycache__', 'node_modules', 'dist', 'build', 'rust_core', 'data'}
    results = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            clean_line = line.rstrip('\r\n')
                            if len(clean_line) > max_len:
                                results.append(f"{path}:{i}:{len(clean_line)}")
                except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                    print(f"Error reading {path}: {e}")
    return results

if __name__ == "__main__":
    long_lines = find_long_lines('.')
    with open('long_lines_report.txt', 'w', encoding='utf-8') as f:
        for line in long_lines:
            f.write(line + '\n')
    print(f"Found {len(long_lines)} lines longer than 120 chars. Report saved to long_lines_report.txt")
