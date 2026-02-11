import json
import os

path = r'c:\Dev\PyAgent\lint_results.json'

if not os.path.exists(path):
    print(f"Error: {path} not found")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)

def is_clean(entry):
    f8 = entry.get('flake8', {})
    ruff = entry.get('ruff', {})
    mypy = entry.get('mypy', {})
    
    f8_clean = f8.get('exit_code') == 0 and not f8.get('stdout', '').strip()
    ruff_clean = ruff.get('exit_code') == 0 and ("All checks passed!" in ruff.get('stdout', '') or not ruff.get('stdout', '').strip())
    mypy_clean = mypy.get('exit_code') == 0 and ("no issues found" in mypy.get('stdout', '').lower() or not mypy.get('stdout', '').strip())
    
    return f8_clean and ruff_clean and mypy_clean

filtered_data = [entry for entry in data if not is_clean(entry)]
new_count = len(filtered_data)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2)

print(f"Cleaned up {original_count - new_count} clean entries. {new_count} entries with potential issues remaining.")
