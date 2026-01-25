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
Fix Extension Logging module.
"""

import re
import os

def fix_logging(content):
    # Match logger.level(f"...") or logger.level(\nf"...")
    # This is a bit complex for a regex, let's use a simpler one for common cases
    pattern = r'(logger\.(?:debug|info|warning|error|critical|log)\(\s*)f"([^"]*)"([^)]*)\)'

    def replace_fstring(match):
        prefix = match.group(1)
        fstring_content = match.group(2)
        suffix = match.group(3)

        # Extract variables from f-string {...}
        vars = re.findall(r'\{([^}:!]*)[^}]*\}', fstring_content)
        if not vars:
            return match.group(0) # Not a real f-string with variables

        # Replace {var} with %s
        new_format = re.sub(r'\{[^}]*\}', '%s', fstring_content)

        # Build new logging call
        # We need to handle the case where suffix already contains commas or other stuff
        # but usually it's just the closing paren
        return f'{prefix}"{new_format}", {", ".join(vars)}{suffix})'

    return re.sub(pattern, replace_fstring, content, flags=re.MULTILINE)

file_path = r"c:\DEV\PyAgent\src\core\base\registry\extension_registry.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = fix_logging(content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)