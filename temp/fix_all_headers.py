#!/usr/bin/env python3
"""Comprehensive fix for all files with duplicate headers and __future__ import issues."""

import re
from pathlib import Path

def fix_file(file_path: Path) -> bool:
    """Fix a single file. Returns True if modified."""
    content = file_path.read_text(encoding='utf-8')
    original = content
    
    lines = content.split('\n')
    output_lines = []
    seen_copyright = False
    seen_first_docstring = False
    future_imports = []
    skip_until_blank = False
    
    for i, line in enumerate(lines):
        # Handle shebang
        if line.startswith('#!'):
            output_lines.append(line)
            continue
        
        # Handle license header - keep only first occurrence
        if line.startswith('# Copyright') or (seen_copyright and line.startswith('#')):
            if not seen_copyright:
                output_lines.append(line)
                seen_copyright = True
            elif seen_copyright and line.startswith('#') and i > 0:
                # Check if we already have a docstring
                if any('"""' in l or "'''" in l for l in output_lines):
                    skip_until_blank = True
                    continue
                else:
                    output_lines.append(line)
            continue
        
        # Skip duplicate license header lines after we've seen a docstring
        if skip_until_blank:
            if not line.strip():
                skip_until_blank = False
            continue
        
        # Handle docstrings - keep first one only
        if ('"""' in line or "'''" in line) and not seen_first_docstring:
            if not any('from __future__' in l for l in output_lines):
                output_lines.append(line)
                seen_first_docstring = True
            continue
        
        # Skip duplicate docstrings
        if ('"""' in line or "'''" in line) and seen_first_docstring:
            if any('from __future__' in l for l in lines[i:]):
                continue
        
        # Collect __future__ imports to place them after docstring
        if line.strip().startswith('from __future__'):
            future_imports.append(line)
            continue
        
        # Add __future__ imports after first docstring
        if seen_first_docstring and not future_imports and 'from __future__' not in line:
            if line.strip() and not line.startswith('#'):
                for fut in future_imports:
                    output_lines.append(fut)
                future_imports = []
        
        output_lines.append(line)
    
    # Add any remaining __future__ imports
    if future_imports:
        for fut in future_imports:
            if fut not in output_lines:
                # Insert after docstring
                for j, line in enumerate(output_lines):
                    if '"""' in line or "'''" in line:
                        output_lines.insert(j+1, fut)
                        break
    
    result = '\n'.join(output_lines)
    
    if result != original:
        file_path.write_text(result, encoding='utf-8')
        return True
    return False

fixed_count = 0
problem_count = 0
for py_file in Path('src').rglob('*.py'):
    try:
        # Quick check if file has the problem
        content = py_file.read_text(encoding='utf-8')
        if content.count('# Copyright') > 1 or (content.find('from __future__') > 0 and '"""' in content[:content.find('from __future__')]):
            problem_count += 1
            if fix_file(py_file):
                fixed_count += 1
    except Exception as e:
        pass

print(f"Fixed {fixed_count} out of {problem_count} problem files")
