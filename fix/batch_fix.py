#!/usr/bin/env python3
"""Fix any -> Any type annotations in test_agent_backend.py"""

import sys
from pathlib import Path

# Read and fix the file
test_backend_file = Path('src/test_agent_backend.py')
content = test_backend_file.read_text(encoding='utf-8')

# Count before
before_count = content.count(': any')

# Replace all instances
fixed_content = content.replace(': any', ': Any')

# Write back
test_backend_file.write_text(fixed_content, encoding='utf-8')

print(f"Fixed {before_count} instances of ': any' -> ': Any' in test_agent_backend.py")
print("File successfully updated!")
