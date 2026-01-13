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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Script for migrating hardcoded version strings to use the central VERSION import."""

from __future__ import annotations
import os

src_path = r"c:\DEV\PyAgent\src"
version_import = "from src.core.base.version import VERSION"
target_version = 'VERSION = "2.1.2-stable"'

print(f"Starting version migration in: {src_path}")

files_processed = 0
files_modified = 0

for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py") and file != "version.py":
            files_processed += 1
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if target_version in content:
                    # Replace the hardcoded version with an import
                    # We look for the line and replace it
                    lines = content.splitlines()
                    new_lines = []
                    modified = False
                    for line in lines:
                        if line.strip() == target_version:
                            new_lines.append(version_import)
                            modified = True
                        else:
                            new_lines.append(line)
                    
                    if modified:
                        new_content = "\n".join(new_lines) + ("\n" if content.endswith("\n") else "")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"  Migrated: {path}")
                        files_modified += 1
            except Exception as e:
                print(f"  Error processing {path}: {e}")

print(f"\nFinished. Processed {files_processed} files, modified {files_modified} files.")