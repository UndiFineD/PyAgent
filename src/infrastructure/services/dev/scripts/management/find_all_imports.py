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

"""Script for finding all legacy import patterns across the workspace."""

from __future__ import annotations
from src.core.base.version import VERSION
import os

__version__ = VERSION
results = []
for root_dir in ['src', 'tests']:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f):
                            if 'from agent_' in line or 'import agent_' in line or 'from classes.' in line:
                                results.append(f"{path}:{i+1}:{line.strip()}")
                except:
                    pass
with open('find_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print(f"Found {len(results)} matches")