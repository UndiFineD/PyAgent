#!/usr/bin/env python3
import os
import re

HEADER = """#!/usr/bin/env python3
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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if header already exists
    if "Copyright 2026 PyAgent Authors" in content and "Licensed under the Apache License" in content:
        return False
    
    # Remove existing shebang/header
    content = re.sub(r'^#!.*?\n', '', content)
    content = re.sub(r'^# Copyright.*?\n', '', content, flags=re.MULTILINE)
    content = content.lstrip()
    
    # Add new header
    new_content = HEADER + "\n" + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

root_dir = "src/logic/agents"
count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            if process_file(full_path):
                count += 1
                print(f"Updated {full_path}")

print(f"Total files updated: {count}")
