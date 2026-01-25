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


"""Script to remove hardcoded VERSION strings from files, preparing for dynamic versioning."""

from __future__ import annotations

import os
import re

root_dirs = ['src', '.', 'gui', 'tests'] # Scan these top-level dirs
skip_files = ['version.py', 'cleanup_version.py']
version_pattern = re.compile(r'VERSION\s*=\s*[\"\']2\.1\.2-stable[\"\']')

count = 0
for r_dir in root_dirs:
    for root, dirs, files in os.walk(r_dir):
        # Skip some common hidden/vendor dirs
        if any(x in root for x in ['.git', '__pycache__', '.venv', 'node_modules']):
            continue
            
        for file in files:
            if file.endswith('.py') and file not in skip_files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    changed = False
                    for line in lines:
                        if version_pattern.search(line):
                            # Only remove if it's a direct assignment, not part of a larger string or import
                            if line.strip().startswith('VERSION ='):
                                changed = True
                                continue
                        new_lines.append(line)
                    
                    if changed:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f'Cleaned up VERSION in {file_path}')
                        count += 1
<<<<<<< HEAD
                except Exception as e:
                    print(f'Error processing {file_path}: {e}')
=======
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    print(f"Error processing {file_path}: {e}")
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)

print(f'Finished. Total files cleaned: {count}')