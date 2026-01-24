#!/usr/bin/env python3
import os
import re

def fix_improve_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match def improve_content(self, ...) with any variable name and any async/sync
    pattern = r'(async\s+)?def\s+improve_content\s*\(self,\s*([^,)]+)(\s*:[^,)]+)?\s*\)(\s*->\s*[^:]+)?\s*:'
    
    match = re.search(pattern, content)
    if match:
        is_async = match.group(1) or ""
        var_name = match.group(2).strip()
        print(f"Standardizing improve_content in {filepath} (var: {var_name}, async: {bool(is_async)})")
        
        new_def = 'async def improve_content(self, prompt: str, target_file: str | None = None) -> str:'
        
        # Replace the definition
        content = content.replace(match.group(0), new_def)
        
        # If the variable name wasn't 'prompt', we need to add a line to map it or replace occurrences
        if var_name != 'prompt' and var_name != '_':
             # Add mapping line after docstring or as first line of body
             # Find end of docstring or start of body
             def_start = content.find(new_def)
             body_start = content.find(':', def_start) + 1
             # Check if there's a docstring
             docstring_match = re.search(r'^\s*(""".*?"""|\'\'\'.*?\'\'\')', content[body_start:], re.DOTALL | re.MULTILINE)
             if docstring_match:
                 insert_pos = body_start + docstring_match.end()
                 content = content[:insert_pos] + f"\n        {var_name} = prompt\n        _ = target_file" + content[insert_pos:]
             else:
                 content = content[:body_start] + f"\n        {var_name} = prompt\n        _ = target_file" + content[body_start:]
        else:
             # Just add target_file suppression
             def_start = content.find(new_def)
             body_start = content.find(':', def_start) + 1
             docstring_match = re.search(r'^\s*(""".*?"""|\'\'\'.*?\'\'\')', content[body_start:], re.DOTALL | re.MULTILINE)
             if docstring_match:
                 insert_pos = body_start + docstring_match.end()
                 content = content[:insert_pos] + "\n        _ = target_file" + content[insert_pos:]
             else:
                 content = content[:body_start] + "\n        _ = target_file" + content[body_start:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

base_dir = r"c:\DEV\PyAgent\src\logic\agents\cognitive"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py'):
            fix_improve_content(os.path.join(root, file))
