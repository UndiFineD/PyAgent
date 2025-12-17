#!/usr/bin/env python3
"""Fix any -> Any type annotations in test files."""

import os
from pathlib import Path

# Files to fix
files_to_fix = [
    'src/test_agent_backend.py',
]

for filepath in files_to_fix:
    full_path = Path(filepath)
    if full_path.exists():
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_count = content.count(': any')
        if original_count > 0:
            content = content.replace(': any', ': Any')
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'{filepath}: Replaced {original_count} instances of ": any" with ": Any"')
        else:
            print(f'{filepath}: No instances found')
    else:
        print(f'{filepath}: File not found')
