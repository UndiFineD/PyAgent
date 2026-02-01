#!/usr/bin/env python3
"""Fix duplicate headers, docstrings, and __future__ import ordering."""

import re
from pathlib import Path

def clean_file_headers(content: str) -> str:
    """Remove duplicate license headers and docstrings, fix __future__ positioning."""
    lines = content.split('\n')
    result = []
    in_first_docstring = False
    docstring_count = 0
    seen_copyright = False
    first_docstring_end = -1
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Keep shebang and copyright header
        if line.startswith('#!') or (line.startswith('#') and 'Copyright' in line):
            result.append(line)
            if 'Copyright' in line:
                seen_copyright = True
            i += 1
            continue
        
        # Skip other header comments for now, keep actual content
        if line.startswith('#') and not 'pylint' in line and not 'noqa' in line:
            if seen_copyright and 'Without' not in line and 'See the' not in line and 'limitations' not in line:
                result.append(line)
            elif not seen_copyright:
                result.append(line)
            i += 1
            continue
        
        # Handle docstrings - keep only the first one
        if line.strip().startswith('"""') or line.strip().startswith("'''"):
            if docstring_count == 0:
                in_first_docstring = True
                docstring_count += 1
                result.append(line)
            elif in_first_docstring:
                result.append(line)
                if (line.strip().endswith('"""') or line.strip().endswith("'''")) and len(line.strip()) > 3:
                    in_first_docstring = False
                    first_docstring_end = len(result) - 1
            i += 1
            continue
        
        # Add non-duplicate content
        if not in_first_docstring or docstring_count == 0:
            result.append(line)
        
        i += 1
    
    # Ensure __future__ imports come after docstring
    final_lines = []
    future_imports = []
    docstring_done = False
    
    for line in result:
        if line.strip().startswith('"""') or line.strip().startswith("'''"):
            final_lines.append(line)
            if '"""' in line or "'''" in line:
                if len(line.strip()) > 6 or line.count('"""') > 1 or line.count("'''") > 1:
                    docstring_done = True
        elif line.strip().startswith('from __future__'):
            if not docstring_done:
                future_imports.append(line)
            else:
                final_lines.append(line)
        else:
            if future_imports and not line.strip().startswith('from __future__'):
                final_lines.extend(future_imports)
                future_imports = []
                docstring_done = True
            final_lines.append(line)
    
    if future_imports:
        final_lines.extend(future_imports)
    
    return '\n'.join(final_lines)

files_fixed = []
for py_file in Path('src').rglob('*.py'):
    try:
        content = py_file.read_text(encoding='utf-8')
        cleaned = clean_file_headers(content)
        if cleaned != content:
            py_file.write_text(cleaned, encoding='utf-8')
            files_fixed.append(str(py_file))
    except Exception as e:
        pass

print(f"Fixed {len(files_fixed)} files")
