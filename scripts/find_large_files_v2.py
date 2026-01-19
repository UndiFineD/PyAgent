import os
from pathlib import Path

def get_line_count(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            return content.count(b'\n') + (1 if content and not content.endswith(b'\n') else 0)
    except Exception:
        return 0

search_roots = [
    r"c:\DEV\PyAgent\src",
    r"c:\DEV\PyAgent\data\agents"
]

results = []
special_names = ["SynthesizedReasoningAgent.py", "IntegratedMemoryManagementAgent.py"]
found_special = []

# Specific name search across entire repo
for root, dirs, files in os.walk(r"c:\DEV\PyAgent"):
    if ".git" in dirs: dirs.remove(".git")
    if "node_modules" in dirs: dirs.remove("node_modules")
    if "__pycache__" in dirs: dirs.remove("__pycache__")
    
    for filename in files:
        if filename in special_names:
            found_special.append(os.path.join(root, filename))

# Large file search in specified roots
for root_path in search_roots:
    if not os.path.exists(root_path):
        continue
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "__pycache__" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                count = get_line_count(filepath)
                if count > 500:
                    results.append((count, filepath))

results.sort(key=lambda x: x[0], reverse=True)

print("TOP 10 LARGE FILES (>500 lines):")
for count, path in results[:10]:
    print(f"{count}: {path}")

if found_special:
    print("\nSPECIAL FILES FOUND:")
    for path in found_special:
        print(f"{get_line_count(path)}: {path}")
else:
    print("\nNo files exactly matching 'SynthesizedReasoningAgent.py' or 'IntegratedMemoryManagementAgent.py' found.")
