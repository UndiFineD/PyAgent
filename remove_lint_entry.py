import json
import re
import os
import sys

path = r'c:\Dev\PyAgent\lint_results.json'
if len(sys.argv) < 2:
    print("Usage: python remove_lint_entry.py <file_path>")
    exit(1)

target_file = sys.argv[1].replace('/', '\\')
# If the path starts with c:\Dev\PyAgent\, strip it to match the json format
if target_file.lower().startswith(r'c:\dev\pyagent\\'):
    target_file = target_file[16:]

if not os.path.exists(path):
    print(f"Error: {path} not found")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)
filtered_data = [entry for entry in data if entry['file'].lower() != target_file.lower()]
new_count = len(filtered_data)

if original_count == new_count:
    print(f"Entry for {target_file} not found or already removed.")
else:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)
    print(f"Removed entry for {target_file}. {original_count} -> {new_count}")

total_issues = 0
for entry in filtered_data:
    # Count flake8 issues
    f8 = entry.get('flake8', {}).get('stdout', '').strip()
    if f8:
        total_issues += len(f8.splitlines())
    
    # Count ruff issues
    ruff = entry.get('ruff', {}).get('stdout', '').strip()
    if ruff and "All checks passed!" not in ruff:
        # Filter out summary lines if any
        lines = [l for l in ruff.splitlines() if not l.startswith('Found ') and not l.startswith('Checked ')]
        total_issues += len(lines)
        
    # Count mypy issues
    mypy = entry.get('mypy', {}).get('stdout', '').strip()
    if mypy and "Success: no issues found" not in mypy:
        match = re.search(r'Found (\d+) error', mypy)
        if match:
            total_issues += int(match.group(1))

with open(path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2)

print(f"New file count: {new_count}")
print(f"Total issues remaining: {total_issues}")
