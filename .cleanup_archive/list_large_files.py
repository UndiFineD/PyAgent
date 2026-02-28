import os

def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f)
    except Exception:
        return 0

src_dir = r'C:\DEV\PyAgent\src'
large_files = []

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            lines = count_lines(path)
            if lines > 500:
                rel_path = os.path.relpath(path, r'C:\DEV\PyAgent')
                large_files.append((rel_path, lines))

large_files.sort(key=lambda x: x[1], reverse=True)

for path, lines in large_files:
    print(f"{path}: {lines} lines")
