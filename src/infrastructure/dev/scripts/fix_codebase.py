#!/usr/bin/env python3

"""
Utility to repair corrupted source files by uncommenting essential system imports.
Part of the Fleet Healer autonomous recovery pattern.
"""

import os
import re

def uncomment_lines(root_dir: str) -> None:
    # Regex to catch commented-out essential imports
    p_from = re.compile(r'^\s*#\s*(from\s+(?:typing|dataclasses|__future__|pathlib|datetime|abc|functools|enum|typing_extensions)\s+import\s+)', re.M)
    p_import = re.compile(r'^\s*#\s*(import\s+(?:os|json|logging|re|sys|time|math|hashlib|shutil|subprocess|tempfile|glob|uuid|collections|random|inspect|threading|queue|socket|urllib|traceback|ast|argparse|pathlib))\b', re.M)
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = p_from.sub(r'\1', content)
                    new_content = p_import.sub(r'\1', new_content)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed: {filepath}")
                except Exception as e:
                    print(f"Error fixing {filepath}: {e}")

if __name__ == "__main__":
    uncomment_lines('src/classes')
