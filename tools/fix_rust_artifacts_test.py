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

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python fix_rust_artifacts.py <file_path>")
    sys.exit(1)

def process_file(file_path):
    print(f"Processing: {file_path}")
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    modified = False
    for line in lines:
        # Look for the commit that cleans up artifacts "chore: cleanup git index - ignore Rust build artifacts"
        if "chore: cleanup git index - ignore Rust build artifacts" in line and line.startswith("pick"):
            print(f"  MATCHED in {file_path}! Changing to fixup")
            # Change pick to fixup
            new_lines.append(line.replace('pick', 'fixup', 1))
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w') as f:
            f.writelines(new_lines)

if os.path.isdir(sys.argv[1]):
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith(".rs"):
                process_file(os.path.join(root, file))
elif os.path.isfile(sys.argv[1]):
    process_file(sys.argv[1])
else:
    print(f"Error: '{sys.argv[1]}' is not a valid file or directory.")
    sys.exit(1)
