import os
from pathlib import Path

def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

search_paths = [
    Path(r'c:\DEV\PyAgent\src'),
    Path(r'c:\DEV\PyAgent\data\agents')
]

large_files = []
special_files = [
    "SynthesizedReasoningAgent.py",
    "IntegratedMemoryManagementAgent.py"
]
found_special = []

for path in search_paths:
    if not path.exists():
        continue
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = Path(root) / file
                lines = count_lines(full_path)
                if lines > 500:
                    large_files.append((full_path.absolute(), lines))
                
                if file in special_files:
                    found_special.append((full_path.absolute(), lines))

# Also search whole project for special files in case they were moved outside those dirs
all_root = Path(r'c:\DEV\PyAgent')
for root, dirs, files in os.walk(all_root):
    # Skip some heavy dirs if needed, but let's be thorough for special files
    if 'node_modules' in dirs: dirs.remove('node_modules')
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file in special_files:
            full_path = Path(root) / file
            if not any(f[0] == full_path.absolute() for f in found_special):
                found_special.append((full_path.absolute(), count_lines(full_path)))

large_files.sort(key=lambda x: x[1], reverse=True)

print("--- TOP 10 LARGE FILES (>500 lines) ---")
for p, l in large_files[:10]:
    print(f"{p}: {l} lines")

if found_special:
    print("\n--- SPECIAL FILES FOUND ---")
    for p, l in found_special:
        print(f"{p}: {l} lines")
else:
    print("\nNo special files (SynthesizedReasoningAgent.py or IntegratedMemoryManagementAgent.py) found.")
