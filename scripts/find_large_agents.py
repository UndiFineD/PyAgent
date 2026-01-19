import os
from pathlib import Path

root = Path('src/logic/agents')
large_files = []
for f in root.rglob('*.py'):
    if f.is_file():
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                lines = sum(1 for _ in file)
                if lines > 500:
                    large_files.append((f.as_posix(), lines))
        except Exception:
            pass

large_files.sort(key=lambda x: x[1], reverse=True)
for f, l in large_files:
    print(f"{f}: {l}")
