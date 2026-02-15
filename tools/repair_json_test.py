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

import json
import re

path = r'c:\Dev\PyAgent\lint_results.json'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove trailing commas like ,} or ,]
content = re.sub(r',\s*\}', '}', content)
content = re.sub(r',\s*\]', ']', content)

# Also fix the weird whitespace/formatting if any
# content = re.sub(r'\}\s*,\s*\{', '},\n  {', content)

try:
    data = json.loads(content)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Successfully repaired and reformatted lint_results.json")
except json.JSONDecodeError as e:
    print(f"Failed to repair: {e}")
    # Show context around error
    start = max(0, e.pos - 50)
    end = min(len(content), e.pos + 50)
    print("Context around error:")
    print(content[start:end])
