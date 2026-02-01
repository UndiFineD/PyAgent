#!/usr/bin/env python3
"""Fix for loop syntax errors: 'for x: Type in' -> 'for x in'"""

import re
from pathlib import Path

# Pattern to find: for VAR: TYPE in (handles more complex types)
# Matches: for var: type in, for var: dict[str, Any] in, for var: List[Something] in, etc.
pattern = r'for\s+(\w+):\s*[^i]*?\s+in\s+'

files_fixed = []
for py_file in Path('src').rglob('*.py'):
    try:
        content = py_file.read_text(encoding='utf-8')
        if re.search(pattern, content):
            fixed = re.sub(pattern, r'for \1 in ', content)
            py_file.write_text(fixed, encoding='utf-8')
            files_fixed.append(str(py_file))
    except Exception as e:
        pass

print(f"Fixed {len(files_fixed)} files:")
for f in sorted(files_fixed)[:30]:
    print(f"  {f}")
if len(files_fixed) > 30:
    print(f"  ... and {len(files_fixed) - 30} more")
