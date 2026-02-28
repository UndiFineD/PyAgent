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
Batch fixer for invalid DATE: ... lines and unterminated triple-quoted strings.
- Converts DATE: ... to # DATE: ...
- Closes any remaining unterminated triple-quoted strings
- Reports all changes
"""
import os
import re

TARGET_DIRS = [
    os.path.join("src", "logic", "agents"),
    os.path.join("src", "observability"),
]

DATE_PATTERN = re.compile(r"^\s*DATE:\s*\d{4}-\d{2}-\d{2}", re.MULTILINE)
TRIPLE_QUOTE_PATTERN = re.compile(r'(["\']{3})([\s\S]*?)(?<!["\']{3})$', re.MULTILINE)

# Helper to find all .py files recursively
def find_py_files(base_dirs):
    py_files = []
    for base in base_dirs:
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith(".py"):
                    py_files.append(os.path.join(root, f))
    return py_files

def fix_date_lines(text):
    new_text, n = DATE_PATTERN.subn(lambda m: "# " + m.group(0).lstrip(), text)
    return new_text, n > 0

def fix_triple_quotes(text):
    fixed = text
    changes = False
    matches = list(re.finditer(r'(["\']{3})([\s\S]*?)(?<!["\']{3})$', text, re.MULTILINE))
    for m in matches:
        start, end = m.span()
        quote = m.group(1)
        if not text[end-len(quote):end] == quote:
            fixed = fixed[:end] + quote + fixed[end:]
            changes = True
    return fixed, changes

def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        orig = f.read()
    fixed, changed1 = fix_date_lines(orig)
    fixed, changed2 = fix_triple_quotes(fixed)
    if changed1 or changed2:
        with open(path, "w", encoding="utf-8") as f:
            f.write(fixed)
        print(f"[FIXED] {path} (DATE: {changed1}, triple quotes: {changed2})")
        return True
    return False

def main():
    py_files = find_py_files(TARGET_DIRS)
    print(f"Scanning {len(py_files)} Python files...")
    changed = 0
    for path in py_files:
        try:
            if process_file(path):
                changed += 1
        except Exception as e:
            print(f"[ERROR] {path}: {e}")
    print(f"Done. {changed} files fixed.")

if __name__ == "__main__":
    main()
