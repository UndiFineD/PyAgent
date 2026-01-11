"""Script for finding all legacy import patterns across the workspace."""

import os
results = []
for root_dir in ['src', 'tests']:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f):
                            if 'from agent_' in line or 'import agent_' in line or 'from classes.' in line:
                                results.append(f"{path}:{i+1}:{line.strip()}")
                except: pass
with open('find_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print(f"Found {len(results)} matches")
