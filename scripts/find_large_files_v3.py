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
                if count > 300: # Lowered threshold to see more agents
                    results.append((count, filepath))

results.sort(key=lambda x: x[0], reverse=True)

print("TOP 20 LARGE FILES (>300 lines):")
for count, path in results[:20]:
    print(f"{count}: {path}")

# Check for keywords in file contents if names don't match
keywords = ["SynthesizedReasoningAgent", "IntegratedMemoryManagementAgent"]
found_keywords = []

print("\nSEARCHING FOR KEYWORDS IN CONTENT...")
for root_path in search_roots:
    if not os.path.exists(root_path):
        continue
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for kw in keywords:
                            if kw in content:
                                found_keywords.append((kw, filepath))
                except Exception:
                    pass

if found_keywords:
    for kw, path in found_keywords:
        print(f"Keyword '{kw}' found in: {path}")
else:
    print("Keywords not found in any .py file content in src or data/agents.")
