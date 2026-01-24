import os
import re
from pathlib import Path

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-0])([A-Z])', r'\1_\2', s1).lower()

def fix_path_string(match):
    path_str = match.group(1)
    # Check if it looks like a dot-ified path
    if '.' in path_str and not '/' in path_str and path_str.endswith('.py'):
        parts = path_str.split('.')
        # The last one is 'py', the one before is the filename
        if len(parts) >= 2 and parts[-1] == 'py':
            filename = parts[-2]
            folders = parts[:-2]

            # Convert filename to snake_case
            filename_snake = to_snake_case(filename)

            # Reconstruct with slashes
            new_path_str = '/'.join(folders + [filename_snake + '.py'])

            # Add 'src/' if it doesn't start with it and it's logic/observability/infrastructure/core
            prefixes = [
                'logic', 'observability', 'infrastructure', 'core',
                'tools', 'interface', 'maintenance'
            ]
            if not new_path_str.startswith('src/') and any(new_path_str.startswith(p) for p in prefixes):
                new_path_str = 'src/' + new_path_str

            return f'load_agent_module("{new_path_str}")'
    return match.group(0)

# Regex to find load_agent_module("...")
regex = re.compile(r'load_agent_module\(\s*"([^"]+)"\s*\)')

tests_dir = Path('tests')
for py_file in tests_dir.rglob('*.py'):
    content = py_file.read_text(encoding='utf-8')
    if 'load_agent_module(' in content:
        new_content = regex.sub(fix_path_string, content)
        if new_content != content:
            print(f"Fixing {py_file}")
            py_file.write_text(new_content, encoding='utf-8')

print("Done fixing load_agent_module paths.")
